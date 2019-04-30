# coding=utf-8
from django import forms
from django.db.models import BLANK_CHOICE_DASH

from currency.models import Person
from wallets.models import Payment


class PaymentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        form = super(PaymentForm, self).__init__(*args, **kwargs)


    class Meta:
        model = Payment
        exclude = ['timestamp', 'status']
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
        }


    def clean_amount(self):
        username = self.cleaned_data['new_user_username']
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            self.add_error('new_user_username', u'El nombre de usuario "%s" ya está en uso.' % username)
        return username