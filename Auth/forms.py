from django import forms
from django.forms import ValidationError

from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from django.contrib.auth.models import User

from .models import SocialPerson
from friend.models import FriendList

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label='username', 
        min_length=4, 
        max_length=30, 
        widget=forms.TextInput(attrs={
            'class': "form-control", 
            'placeholder':"Username", 
            'required': True
        })
    ) 

    email = forms.EmailField(
        label='email',
        widget=forms.EmailInput(attrs={
            'class': "form-control", 
            'placeholder':"Email", 
            'required': True
        })
    )  

    first_name = forms.CharField(
        label='First Name',
        max_length='30',
        widget=forms.TextInput(attrs={
            'class': "form-control", 
            'placeholder':"First Name", 
            'required': True
        })
    )

    last_name = forms.CharField(
        label='Last Name',
        max_length='30',
        widget=forms.TextInput(attrs={
            'class': "form-control", 
            'placeholder':"Last Name", 
            'required': True
        })
    )

    age = forms.IntegerField(
        label='Age',
        widget=forms.TextInput(attrs={
            'class': "form-control", 
            'placeholder':"Age", 
            'required': True
        })
    )

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': "form-control", 
            'placeholder':"Password", 
            'required': True,
            'id': 'password-field'
        })
    )  
    password2 = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput(attrs={
            'class': "form-control", 
            'placeholder':"Confirm password", 
            'required': True,
            'id': 'password-field1'
        })
    ) 

  
    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        new = User.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("User Already Exist")  
        return username  

    def clean_email(self):  
        email = self.cleaned_data['email'].lower()  
        new = User.objects.filter(email=email)  
        if new.count():  
            raise ValidationError("Email Already Exist")  
        return email  

    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  

        if password1 and password2 and password1 != password2:  
            raise ValidationError("Passwords does not match")  
        return password2  

    def save(self, commit = True):  
        user = User.objects.create_user(  
            self.cleaned_data['username'].lower(),  
            email = self.cleaned_data['email'].lower(),  
            password = self.cleaned_data['password1'],
            first_name = self.cleaned_data['first_name'],
            last_name = self.cleaned_data['last_name']  
        )
        user = User.objects.get(username = self.cleaned_data['username'].lower())
        social = SocialPerson()
        social.user = user
        social.age = self.cleaned_data['age']
        social.slug = user.username
        social.save()
        friendList = FriendList()
        friendList.user = user
        friendList.save()
        return user  


class LoginUserForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'required': True,
        }
    ))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'required': True,
        }
    ))