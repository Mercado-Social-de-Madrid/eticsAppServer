# coding=utf-8
from django import forms
from django.contrib.auth.models import User
from django.db.models import BLANK_CHOICE_DASH
from django.utils.decorators import method_decorator

from currency.models import Person
from helpers import superuser_required
from helpers.forms.BootstrapForm import BootstrapForm
from wallets.models import Transaction


class TransactionForm(forms.ModelForm, BootstrapForm):

    class Meta:
        model = Transaction
        exclude = ['user']
        widgets = {
            'wallet_from': forms.HiddenInput(),
            'wallet_to': forms.HiddenInput(),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'concept': forms.TextInput(attrs={'class': 'form-control', }),
            'is_bonification': forms.CheckboxInput(attrs={'class':'custom-control-input', 'checked':False})
        }



class BulkTransactionForm(forms.ModelForm, BootstrapForm):

    bulk_wallets = forms.CharField(widget=forms.HiddenInput(), required=True)

    class Meta:
        model = Transaction
        exclude = ['user', 'wallet_to']
        widgets = {
            'wallet_from': forms.HiddenInput(),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'concept': forms.TextInput(attrs={'class': 'form-control', }),
            'is_bonification': forms.CheckboxInput(attrs={'class':'custom-control-input', 'checked':False})
        }
