from typing import Any, Dict
from django import forms
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField
from .models import Users
import re

class RegistrationForm(forms.ModelForm):
    captcha = CaptchaField()
    confirm_password= forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model=Users
        fields = ['first_name','last_name','username','email','phone', 'password', 'confirm_password', 'captcha']

    def clean_first_name(self):
        first_name=self.cleaned_data.get('first_name')
        if first_name is not None:
            if not first_name.isalpha():
                raise forms.ValidationError('Please enter alphabets only')
        return first_name
    
    def clean_last_name(self):
        last_name=self.cleaned_data.get('last_name')
        if last_name is not None:
            if not last_name.isalpha():
                raise forms.ValidationError('Please enter alphabets only')
        return last_name
    
    def clean_username(self):
        username=self.cleaned_data.get('username')
        
        if username is None:
            raise forms.ValidationError('User Name is a Mandatory Field')
        elif not username.isalnum():
            raise forms.ValidationError('User Name must contain alphabet and number')
        else:
            try:
                user=Users.objects.get(username=username)
            except Users.DoesNotExist:
                user=None
            
            if user is not None:
                raise forms.ValidationError('User is already exist')
        return username
    

    def clean_email(self):
        email=self.cleaned_data.get('email')
        
        Exp = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if email is None:
            raise forms.ValidationError('Email is a Mandatory Field')
        elif not re.fullmatch(Exp,email):
            raise forms.ValidationError('Please enter valid email address')
        else:
            try:
                user=Users.objects.get(email=email)
            except Users.DoesNotExist:
                user=None
            
            if user is not None:
                raise forms.ValidationError('User is already exist')
        return email
    
    def clean_phone(self):        
        phone=self.cleaned_data.get('phone')
        phExp=re.compile(r'^\d{10}$')
        if not re.match(phExp,phone):
            raise forms.ValidationError('Please enter vaild Phone No')
        else:
            if len(phone) != 10:
                raise forms.ValidationError('Phone No. must have 10 digits')
        return phone
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        pwd_reg = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\W).{8,}$')
        if not pwd_reg.match(password):
            raise forms.ValidationError('Must contain at least one number and one uppercase and lowercase letter and one special charater, and at least 8 or more characters')
        return password
    
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')        
        if confirm_password is None:
            raise forms.ValidationError('confirm_password is required')
        else:
            if password != confirm_password:
                raise forms.ValidationError('password and confirm Password must be same')
        
        return confirm_password
   
        
class ChangeemailForm(forms.ModelForm):
    class Meta:
       model=Users
       fields = ['email'] 

    def clean_email(self):
        email=self.cleaned_data.get('email')        
        Exp = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')        
        if not re.fullmatch(Exp,email):
            raise forms.ValidationError('Please enter valid email address')
        else:
            try:
                user=Users.objects.get(email=email)
            except Users.DoesNotExist:
                user=None
            
            if user is not None:
                print('*')
                raise forms.ValidationError('User is already exist')
        return email
    
class ResetpasswordFrom(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password= forms.CharField(widget=forms.PasswordInput)

    
    def clean_password(self):
        password = self.cleaned_data.get('password')        
        pwd_reg = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\W).{8,}$')
        if not pwd_reg.match(password):
            raise forms.ValidationError('Must contain at least one number and one uppercase and lowercase letter and one special charater, and at least 8 or more characters')
        return password
    
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')        
        if confirm_password is None:
            raise forms.ValidationError('confirm_password is required')
        else:
            if password != confirm_password:
                raise forms.ValidationError('password and confirm Password must be same')
        
        return confirm_password

class ResetpasswordemailForm(forms.Form):
    email=forms.EmailField(max_length=255)
    class Meta:
        fields=['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        Exp = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not re.fullmatch(Exp, email):
            raise ValidationError('please enter valid email address')
        else:
            try:
                users = Users.objects.filter(email=email).first()
            except Users.DoesNotExist:
                users= None
            if users is None:
                raise ValidationError('User is not found')
        print(email)
        return email