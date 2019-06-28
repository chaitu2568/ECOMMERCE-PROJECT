from django import forms
from django.contrib.auth import get_user_model


class GuestForm(forms.Form):
	Email=forms.EmailField()

class LoginForm(forms.Form):
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
