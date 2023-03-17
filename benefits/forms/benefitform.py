# -*- coding: utf-8 -*-
from ckeditor.widgets import CKEditorWidget
from django import forms


from benefits.models import Benefit


class BenefitForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        form = super(BenefitForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Benefit
        exclude = ['published_date', 'last_updated']
        widgets = {
            'entity': forms.HiddenInput(),
            'benefit_for_entities': CKEditorWidget(attrs={'cols': 80, 'rows': 30}),
            'benefit_for_members': CKEditorWidget(attrs={'cols': 80, 'rows': 30}),
            'includes_intercoop_members': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
            'in_person': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
            'online': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
            'discount_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código de descuento'}),
            'discount_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Link del descuento'}),
            'discount_link_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Texto del botón del link de descuento'}),
            'active': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
        }

