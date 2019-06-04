# coding=utf-8
import re

from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        self.fields['username'].error_messages = {'required': "Introduce un usuario"}
        self.fields['username'].max_length = 30
        self.fields['password'].error_messages = {'required': 'Introduce una contraseña'}
        self.fields['password'].max_length = 30
        self.fields['repeat_password'].error_messages = {'required': 'Repite la contraseña'}
        self.fields['repeat_password'].max_length = 30

        self.fields['email'].required = False


    repeat_password = forms.CharField(max_length=30, widget=forms.PasswordInput, required=True, label="Repetir contraseña")
    pincode = forms.CharField(max_length=4, widget=forms.PasswordInput, required=True,
                                      label="Código PIN (cuatro dígitos)")


    def clean_pincode(self):

        pincode = self.cleaned_data.get('pincode', '')
        if len(pincode)!=4:
            raise forms.ValidationError("El PIN debe tener 4 caracteres")
        if not re.compile('^\d+$').match(pincode):
            raise forms.ValidationError("El PIN solo puede contener dígitos")

        return pincode

    def clean_username(self):
        username = self.cleaned_data.get('username','')
        if len(username) < 4:
            raise forms.ValidationError("El usuario tiene que tener más de 4 caracteres")

        username_count = User.objects.filter(username=username).count()
        if username_count > 0:
            raise forms.ValidationError("El usuario ya existe...")

        return username

    def clean_password(self):
        password = self.cleaned_data.get('password','')

        if len(password) < 5:
            raise forms.ValidationError("La contraseña tiene que tener más de 5 caracteres")
        return password


    def clean(self):
        password = self.cleaned_data.get('password', '')
        password_repeat = self.cleaned_data.get('repeat_password','')

        if password != password_repeat:
            raise forms.ValidationError({'repeat_password': ["Las contraseñas no coinciden"]})



    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'repeat_password')