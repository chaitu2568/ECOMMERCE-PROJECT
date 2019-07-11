from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import LoginForm,register_form,GuestForm
from django.utils.http import is_safe_url
from django.contrib.auth import get_user_model,login,authenticate
from .models import GuestEmail
from django.views.generic import CreateView,FormView
# Create your views here.
def guest_register_page(request):
    form=GuestForm(request.POST or None)
    context={'form':form}
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path=next_ or next_post or None
    if form.is_valid():
        Email=form.cleaned_data.get('Email')
        new_guest_email=GuestEmail.objects.create(Email=Email)
        request.session['guest_email_id']=new_guest_email.id
        if is_safe_url(redirect_path,request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect('/register/')
    return redirect('/register/')

class LoginView(FormView):
    form_class=LoginForm
    success_url='/'
    template_name='accounts/login.html'

    def form_valid(self,form):
        request=self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path=next_ or next_post or None
        email=form.cleaned_data.get('email')
        password=form.cleaned_data.get('password')
        user=authenticate(request,username=email,password=password)
        if user is not None:
            login(request,user)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path,request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('/')
        return super(LoginView,self).form_invalid(form)

# def login_page(request):
#     form=LoginForm(request.POST or None)
#     context={'form':form}
#     next_ = request.GET.get('next')
#     next_post = request.POST.get('next')
#     redirect_path=next_ or next_post or None
#     if form.is_valid():
#         print(form.cleaned_data)
#         username=form.cleaned_data.get('username')
#         password=form.cleaned_data.get('password')
#         user=authenticate(request,username=username,password=password)
#         if user is not None:
#             login(request,user)
#             try:
#                 del request.session['guest_email_id']
#             except:
#                 pass
#             if is_safe_url(redirect_path,request.get_host()):
#                 return redirect(redirect_path)
#             else:
#                 return redirect('/')
#         else:
#             print('login error')
#     return render(request,'accounts/login.html', context)

class RegisterView(CreateView):
    form_class=register_form
    template_name='accounts/register.html'
    success_url='/login/'

# User=get_user_model()
# def register_page(request):
#     form=register_form(request.POST or None)
#     context={'form':form}
#     if form.is_valid():
#         form.save()
#     return render(request,'accounts/register.html',context)
