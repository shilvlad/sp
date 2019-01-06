from django import forms

class LoginForm(forms.Form):
    login = forms.CharField(label='Your name', max_length=100)
