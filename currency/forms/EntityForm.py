# coding=utf-8
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth.models import User
from django.db.models import BLANK_CHOICE_DASH

from currency.models import Entity


class EntityForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        form = super(EntityForm, self).__init__(*args, **kwargs)

    owner_id = forms.CharField(max_length=100, widget=forms.HiddenInput, required=False)
    is_new_entity = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput())
    new_user_username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    new_user_first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    new_user_last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    new_user_email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), required=False)
    new_user_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Entity
        exclude = ['owner','user']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'description': CKEditorWidget(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'readonly':False}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'readonly':False}),
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
            'logo': forms.FileInput(attrs={}),
            'city': forms.HiddenInput(),
        }

    def clean_new_user_username(self):
        username = self.cleaned_data['new_user_username']
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            self.add_error('new_user_username', u'El nombre de usuario "%s" ya está en uso.' % username)
        return username


    def clean(self):
        cleaned_data = super(EntityForm, self).clean()

        is_new = cleaned_data.get('is_new_entity')
        if is_new:
            owner_id = cleaned_data.get("owner_id")
            new_user_username = cleaned_data.get("new_user_username")
            new_user_password = cleaned_data.get("new_user_password")

            if owner_id or (new_user_password and new_user_username):
                return cleaned_data
            else:
                if new_user_username and not new_user_password:
                    self.add_error('owner_id', 'Introduce una contraseña')
                else:
                    self.add_error('owner_id', 'Selecciona un usuario asociado a la entidad o crea uno nuevo')

