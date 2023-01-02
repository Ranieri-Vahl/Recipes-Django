import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')
    
    if not regex.match(password):
        raise ValidationError('Must have 1 upper case letter, 1 lower case letter, 1 number and min 8 characters.', code='invalid') # noqa E501


def username_validation(username):
    regex = re.compile(r'^(.*[a-z0-9@/./+/-/_]).{5,20}$')

    if not regex.match(username):
        raise ValidationError('Min 5 and max 20 characters. Letters, numbers and @/./+/-/_ only', code='invalid') # noqa E501


def email_validation(email):
    regex = re.compile(r'^[^\s@<>\(\)[\]\.]+(?:\.[^\s@<>\(\)\[\]\.]+)*@\w+(?:[\.\-_]\w+)*$') # noqa E501

    if not regex.match(email):
        raise ValidationError('Invalid E-mail!, type again', code='invalid') # noqa E501


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        required=True,
        label='Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Type your password'
        }),
        validators=[strong_password]
        )
    
    password2 = forms.CharField(
        required=True,
        label='Confirm password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password'
        })
        )

    username = forms.CharField(
        required=True,
        label='Username',
        widget=forms.TextInput(attrs={
            'placeholder': 'Type your username'
        }),
        validators={username_validation},
        )

    email = forms.CharField(
        required=True,
        label='E-mail',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Type your E-mail'
        }),
        validators={email_validation},
        )
    
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
        
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Type your first name'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Type your last name'
            }),        
        }

    def clean(self):
        cleaned = super().clean()
        password = cleaned.get('password')
        password2 = cleaned.get('password2')
        if password != password2:
            raise ValidationError({
                'password': 'The passwords must be equal!',
                'password2': 'The passwords must be equal!'
            })