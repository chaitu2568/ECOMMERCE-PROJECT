from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import Form_page, login_form, register_form
from django.contrib.auth import get_user_model,login,authenticate

# def home_page(request):
# 	return HttpResponse("<h1>Hello Guys!!!!!!</h1>")

def home_page(request):
	context={'first':'Hello World','matter':'This is the homepage'}
	if request.user.is_authenticated():
		context['premiumcontent']='i am chaitu'
	return render(request,'homepage.html',context)

def about_page(request):
	context={'first':'About Yourself','matter':'This is the Aboutpage'}
	return render(request,'homepage.html',context)

def contact_page(request):
	contact_form=Form_page(request.POST or None)
	context={'first':'Contact Information','matter':'This is the Contactpage','form':contact_form}
	if contact_form.is_valid():
		print(contact_form.cleaned_data)

	return render(request,'contact/form.html',context)

def login_page(request):
	form=login_form(request.POST or None)
	context={'form':form}
	print(request.user.is_authenticated())
	if form.is_valid():
		print(form.cleaned_data)
		username=form.cleaned_data.get('username')
		password=form.cleaned_data.get('password')
		user=authenticate(request,username=username,password=password)
		if user is not None:
			login(request,user)
			# context['form']=login_form()
			return redirect('/login')
		else:
			print('login error')
	return render(request,'auth/login.html', context)

User=get_user_model()
def register_page(request):
	form=register_form(request.POST or None)
	context={'form':form}
	if form.is_valid():
		print(form.cleaned_data)
		username=form.cleaned_data.get('username')
		email=form.cleaned_data.get('email')
		password=form.cleaned_data.get('password')
		new_user=User.objects.create_user(username,email,password)
	return render(request,'auth/register.html',context)
