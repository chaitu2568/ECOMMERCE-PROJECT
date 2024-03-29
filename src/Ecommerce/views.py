from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .forms import Form_page
from django.contrib.auth import get_user_model,login,authenticate

# def home_page(request):
# 	return HttpResponse("<h1>Hello Guys!!!!!!</h1>")

def home_page(request):
	context={'first':'Hello World','matter':'This is the homepage'}
	if request.user.is_authenticated:
		context['premiumcontent']='i am chaitu'
	return render(request,'homepage.html',context)

def about_page(request):
	context={'first':'About Yourself','matter':'This is the Aboutpage'}
	return render(request,'homepage.html',context)

def contact_page(request):
	contact_form=Form_page(request.POST or None)
	context={'first':'Contact Information','matter':'This is the Contactpage','form':contact_form}
	if contact_form.is_valid():
		# print(contact_form.cleaned_data)
		if request.is_ajax():
			return JsonResponse({'message':'Thank You for Providing Your Details'})
	if contact_form.errors:
		# print(contact_form.cleaned_data)
		 
		errors=contact_form.errors.as_json()
		if request.is_ajax():
			return HttpResponse(errors,status=400,content_type='application/json')

	return render(request,'contact/form.html',context)
