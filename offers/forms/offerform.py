# coding=utf-8
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.db.models import BLANK_CHOICE_DASH


from offers.models import Offer


class OfferForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        form = super(OfferForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Offer
        exclude = ['entity']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': CKEditorWidget(attrs={'cols': 80, 'rows': 30}),
            'active': forms.CheckboxInput(attrs={'class': 'form-control' }),
            'discount_percent': forms.NumberInput(attrs={'class': 'form-control'}),
            'discounted_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'begin_date': forms.DateInput(attrs={'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control'}),
            'banner_image': forms.FileInput(attrs={}),
        }

