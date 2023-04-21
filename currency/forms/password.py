# coding=utf-8

from django.contrib.auth.forms import PasswordChangeForm
from helpers.forms.BootstrapForm import BootstrapForm

class PasswordForm(BootstrapForm, PasswordChangeForm):
    pass

