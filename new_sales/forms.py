from django import forms
from .models import Report
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User



class FileUploadForm(forms.ModelForm):
	class Meta:
		model=Report
		fields='__all__'


class CreateUserForm(UserCreationForm):
	class Meta:
		model=User
		fields=['username','email','password1','password2']

class LoginForm(AuthenticationForm):
	class Meta:
		model=User
		fields=['username','password1','password2']
