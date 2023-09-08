from django import forms
from django.conf import settings
from unfold.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    password = forms.CharField(widget=forms.PasswordInput(render_value=True))

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)

        if settings.LOGIN_USERNAME and settings.LOGIN_PASSWORD:
            self.fields["username"].initial = settings.LOGIN_USERNAME
            self.fields["password"].initial = settings.LOGIN_PASSWORD
