from django import forms
from django.contrib.auth.models import User
from basic_app.models import UserProfileInfo
from django.core import validators

class UserForm(forms.ModelForm):
    username = forms.CharField(label='Username:', max_length=25,widget=forms.TextInput(attrs={'placeholder': 'Username', 'required': 'true'}))
    email = forms.CharField(label='Email:', max_length=50, widget=forms.TextInput(attrs={'placeholder': 'example@gmail.com', 'required': 'true'}))
    password = forms.CharField(label='Password:', max_length=50, widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'required': 'true'}))
    confirm_password=forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'placeholder': 'Verify Password', 'required': 'true'}))
    botcatcher = forms.CharField(required=False, widget=forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])

    class Meta():
        model = User
        fields = ('username','password','email')

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Passwords to not match, please try again"
            ) 

        if len(password) < 9 or any(char.isdigit() for char in password) != True:
            raise forms.ValidationError(
                'Passwords must be longer than 9 characters & include digit(s)'
            )
        
    def clean_botcatcher(self):
        botcatcher = self.cleaned_data['botcatcher']
        if len(botcatcher) > 0:
            raise forms.ValidationError("This action is not permitted")
        return botcatcher

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('profile_pic',)

class ContactForm(forms.Form):
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)