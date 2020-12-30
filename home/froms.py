from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import profile , BlogComment


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    

    class Meta:
        model = User
        fields= ['username','email','password1','password2', ]
class NewCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['content']
class UserUpdateForm(forms.ModelForm):
    email=forms.EmailField()
    class Meta:
        model = User
        fields= ['username','email' ]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = profile
        fields = ['image']
