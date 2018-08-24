from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password','last_name']
        labels = {
            'username' : '아이디',
            'email' : '이메일',
            'password' : '패스워드',
            'last_name' : '주소',
        }
        
class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','password']
