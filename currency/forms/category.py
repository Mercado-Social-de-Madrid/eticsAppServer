# coding=utf-8
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.db.models import BLANK_CHOICE_DASH

from currency.models import Entity, Category


class CategoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        form = super(CategoryForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Category
        exclude = []
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control color-widget'}),
        }

