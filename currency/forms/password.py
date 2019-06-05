




# coding=utf-8
import datetime

from dateutil.relativedelta import relativedelta
from django.contrib.auth.forms import PasswordChangeForm
from django import forms

from helpers.forms.BootstrapForm import BootstrapForm


class PasswordForm(BootstrapForm, PasswordChangeForm):
    pass

