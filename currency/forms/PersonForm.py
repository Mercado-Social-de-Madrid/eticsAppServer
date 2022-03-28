# coding=utf-8
from django import forms
from django.db.models import BLANK_CHOICE_DASH

from currency.models import Person


class PersonForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        form = super(PersonForm, self).__init__(*args, **kwargs)


    class Meta:
        model = Person
        exclude = ['fav_entities', 'user']
        widgets = {
            'nif': forms.TextInput(attrs={'class': 'form-control', 'readonly':True }),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', }),
            'surname': forms.TextInput(attrs={'class': 'form-control', }),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows':3,}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', }),
            'registered': forms.TextInput(attrs={'class': 'form-control', 'readonly':True}),
            'profile_image': forms.FileInput(attrs={}),
            'city': forms.HiddenInput(),
            'inactive': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),

        }

