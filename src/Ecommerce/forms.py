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
