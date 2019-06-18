from django import forms
from django.contrib.auth import get_user_model
User=get_user_model()
class Form_page(forms.Form):
	fullname=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your fullname'}))
	email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter your Email-ID'}))
	Content=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Enter your Content here'}))

	def clean_email(self):
		email=self.cleaned_data.get('email')
		if not 'gmail.com' in email:
			raise forms.ValidationError('Email should end with gmail.com')
		return email

class login_form(forms.Form):
	username=forms.CharField()
	password=forms.CharField(widget=forms.PasswordInput())

class register_form(forms.Form):
	username=forms.CharField()
	password=forms.CharField(widget=forms.PasswordInput())
	email=forms.EmailField()
	confirmpassword=forms.CharField(widget=forms.PasswordInput())

	def clean_username(self):
		username=self.cleaned_data.get('username')
		qs=User.objects.filter(username=username)
		if qs.exists():
			raise forms.ValidationError('Username already there')
		return username

	def clean_email(self):
		email=self.cleaned_data.get('email')
		qs=User.objects.filter(email=email)
		if qs.exists():
			raise forms.ValidationError('email already there')
		return email

	def clean(self):
		data=self.cleaned_data
		password1=self.cleaned_data.get('password')
		password2=self.cleaned_data.get('confirmpassword')
		if password2!=password1:
			raise forms.ValidationError('Password must Match')
		return data
