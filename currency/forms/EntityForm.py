# coding=utf-8
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.db.models import BLANK_CHOICE_DASH

from currency.models import Entity


class EntityForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        form = super(EntityForm, self).__init__(*args, **kwargs)

    owner_id = forms.CharField(max_length=100, widget=forms.HiddenInput, required=False)
    new_user_username = forms.CharField(widget=forms.TextInput, required=False)
    new_user_first_name = forms.CharField(widget=forms.TextInput, required=False)
    new_user_last_name = forms.CharField(widget=forms.TextInput, required=False)
    new_user_email = forms.EmailField(required=False)
    new_user_password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = Entity
        exclude = ['owner','email','user']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': CKEditorWidget(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'readonly':True}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'readonly':True}),
            'max_percent_payment': forms.NumberInput(attrs={'class': 'form-control'}),
            'bonus_percent_general': forms.NumberInput(attrs={'class': 'form-control'}),
            'bonus_percent_entity': forms.NumberInput(attrs={'class': 'form-control'}),
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

