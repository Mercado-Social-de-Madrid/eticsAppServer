# coding=utf-8
from django import forms
from django.db.models import BLANK_CHOICE_DASH

from currency.models import Entity


class EntityForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        form = super(EntityForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Entity
        exclude = ['owner','email','user']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'readonly':True}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'readonly':True}),
            'max_percent_payment': forms.NumberInput(attrs={'class': 'form-control'}),
            'bonification_percent': forms.NumberInput(attrs={'class': 'form-control'}),
            'num_workers': forms.NumberInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'facebook_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Página de Facebook'}),
            'twitter_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Perfil de Twitter'}),
            'webpage_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Página web'}),
            'telegram_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Canal de Telegram'}),
            'instagram_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Perfil de Instagram'}),
            'profile_image': forms.FileInput(attrs={}),
            'image': forms.FileInput(attrs={}),
        }

