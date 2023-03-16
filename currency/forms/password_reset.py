from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

UserModel = get_user_model()


class CustomPasswordResetForm(PasswordResetForm):

    email = forms.CharField(label="Email", max_length=254)

    def get_users(self, email_or_username):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        active_users = UserModel._default_manager.filter(
            Q(email__iexact=email_or_username) | Q(username__iexact=email_or_username),
            is_active=True)

        return (u for u in active_users if u.has_usable_password())

    def clean(self):
        cleaned_data = super(PasswordResetForm, self).clean()
        email_or_username = cleaned_data.get('email')
        users = list(self.get_users(email_or_username))

        if len(users) == 0:
            self.add_error('email', "No existe un usuario asociado al email introducido.")
        else:
            user = users[0]
            cleaned_data['email'] = user.email
            return cleaned_data
