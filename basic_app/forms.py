from django import forms
from django.contrib.auth.models import User
from basic_app.models import UserProfileInfo

class UserForm(forms.ModelForm):
    username = forms.CharField(label='Username:', widget=forms.TextInput(attrs={'placeholder': 'Username', 'required': 'true'}))
    email = forms.CharField(label='Email:', widget=forms.TextInput(attrs={'placeholder': 'example@domain.com', 'required': 'true'}))
    password = forms.CharField(label='Password:', widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'required': 'true'}))

    class Meta():
        model = User
        fields = ('username','password','email')

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('profile_pic',)