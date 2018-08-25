from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password','first_name','last_name',]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'15자 이내로 입력 가능합니다.'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password' : forms.PasswordInput(attrs={'class': 'form-control'}),
            'first_name' : forms.TextInput(attrs={'class':'form-control','placeholder':'주소',}),
            'last_name' : forms.TextInput(attrs={'class':'form-control','placeholder':'상세주소',}),
        }
        labels = {
            'username' : '아이디',
            'email' : '이메일',
            'password' : '패스워드',
            'first_name' : '주소',
            'last_name' : '상세주소',
        }
        
class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password':forms.PasswordInput(attrs={'class':'form-control'}),
        }
