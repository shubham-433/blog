from django import forms
from .models import Comment,Post
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField
from django.contrib.auth.models import User
from django.db.models import fields
from taggit.forms import TagField
from taggit_labels.widgets import LabelWidget
from froala_editor.fields import FroalaField
from froala_editor.widgets import FroalaEditor

class EmailPostForm(forms.Form):
    to= forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    comments=forms.CharField(required=False,widget=forms.Textarea(attrs={'class':'form-control'}))

    
    
class CommentForm(forms.ModelForm):
    class Meta:
        model =Comment
        fields =['name','email','body']   
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}), 'email': forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter your email'}), 'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write comment'})}
        

class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email Address'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'email': 'Email'}
        widgets = {'username': forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Username'})}
        

class LoginForm(AuthenticationForm):
    username=UsernameField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password =forms.CharField(label='password',widget= forms.PasswordInput(attrs={'class':'form-control'}))

class AddBlogForm(forms.ModelForm):
    # Alltags = TagField(required=False, widget=LabelWidget)
    body=forms.CharField(widget=FroalaEditor)
    class Meta:
        model=Post
        fields=["title","body","image","tags"]
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Title'}), 'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write Tags'})        }
