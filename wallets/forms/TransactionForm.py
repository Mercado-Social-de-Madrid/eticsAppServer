# coding=utf-8
from django import forms
from django.contrib.auth.models import User
from django.db.models import BLANK_CHOICE_DASH

from currency.models import Person
from wallets.models import Transaction


class TransactionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(TransactionForm, self).__init__(*args, **kwargs)


    class Meta:
        model = Transaction
        exclude = ['fav_entities', 'user']
        widgets = {
            'wallet_from': forms.HiddenInput(),
            'wallet_to': forms.HiddenInput(),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'concept': forms.TextInput(attrs={'class': 'form-control', }),
            'is_bonification': forms.CheckboxInput(attrs={'class':'custom-control-input', 'checked':False})
        }
