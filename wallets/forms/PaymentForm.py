# coding=utf-8
from django import forms
from django.db.models import BLANK_CHOICE_DASH

from currency.models import Person
from wallets.models import Payment


class PaymentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        form = super(PaymentForm, self).__init__(*args, **kwargs)

    pincode = forms.CharField(max_length=30, widget=forms.PasswordInput, required=True,
                              label="Código PIN (cuatro dígitos)")

    class Meta:
        model = Payment
        exclude = ['timestamp', 'status', 'processed']
        widgets = {
            'sender': forms.HiddenInput(),
            'receiver': forms.HiddenInput() ,
            'total_amount': forms.NumberInput(attrs={'class': 'form-control', }),
            'currency_amount': forms.NumberInput(attrs={'class': 'form-control', }),
            'concept': forms.Textarea(attrs={'class': 'form-control', 'rows':3 }),
        }

    def clean_total_amount(self):
        total_amount = self.cleaned_data['total_amount']
        if total_amount <= 0:
            raise forms.ValidationError("El importe total tiene que ser positivo")

        return total_amount

    def save(self, commit=True):
        if not commit:
            return None

        total_amount = self.cleaned_data.get('total_amount')
        currency_amount = self.cleaned_data.get('currency_amount')
        type, receiver = self.cleaned_data.get('receiver').get_related_entity()
        sender = self.cleaned_data.get('sender')
        concept = self.cleaned_data.get('concept')
        pincode = self.cleaned_data.get('pincode', None)

        payment = Payment.objects.new_payment(sender=sender, receiver_uuid=receiver.pk,
                                              total_amount=total_amount, currency_amount=currency_amount,concept=concept, pin_code=pincode )

