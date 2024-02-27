from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class Register(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            'required' : '',
            'name' : 'username',
            'id' : 'username',
            'type' : 'text',
            'class' : 'form-control',
            'placeholder' : 'username',
            'aria-label' : 'username',
            'minlength' : '6'
        })
        self.fields["first_name"].widget.attrs.update({
            'required' : '',
            'name' : 'first_name',
            'id' : 'first_name',
            'type' : 'text',
            'class' : 'col form-control',
            'placeholder' : 'Firstname',
            'aria-label' : 'first_name'
        })
        self.fields["last_name"].widget.attrs.update({
            'required' : '',
            'name' : 'last_name',
            'id' : 'last_name',
            'type' : 'text',
            'class' : 'col form-control',
            'placeholder' : 'Lastname',
            'aria-label' : 'last_name'
        })
        self.fields["email"].widget.attrs.update({
            'required' : '',
            'name' : 'email',
            'id' : 'email',
            'type' : 'email',
            'class' : 'form-control',
            'placeholder' : 'Email',
            'aria-label' : 'email'
        })
        self.fields["password1"].widget.attrs.update({
            'required' : '',
            'name' : 'password1',
            'id' : 'inputPassword5',
            'type' : 'password',
            'class' : 'form-control',
            'placeholder' : 'Create Password',
            'aria-describedby' : 'passwordHelpBlock'
        })
        self.fields["password2"].widget.attrs.update({
            'required' : '',
            'name' : 'password2',
            'id' : 'inputPassword5',
            'type' : 'password',
            'class' : 'form-control',
            'placeholder' : 'Confirm Password',
            'aria-describedby' : 'passwordHelpBlock'
        })


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',  'password1', 'password2' ]