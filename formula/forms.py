from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Fieldset, Layout
from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView
from unfold.forms import AuthenticationForm
from unfold.layout import Submit
from unfold.widgets import (
    UnfoldAdminCheckboxSelectMultiple,
    UnfoldAdminDateWidget,
    UnfoldAdminEmailInputWidget,
    UnfoldAdminFileFieldWidget,
    UnfoldAdminImageFieldWidget,
    UnfoldAdminIntegerFieldWidget,
    UnfoldAdminRadioSelectWidget,
    UnfoldAdminSelectWidget,
    UnfoldAdminSplitDateTimeWidget,
    UnfoldAdminTextareaWidget,
    UnfoldAdminTextInputWidget,
    UnfoldAdminTimeWidget,
    UnfoldBooleanSwitchWidget,
)


class HomeView(RedirectView):
    pattern_name = "admin:index"


class CustomForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label=_("Name"),
        required=True,
        help_text=_("Enter your full name"),
        widget=UnfoldAdminTextInputWidget(),
    )
    email = forms.EmailField(
        label=_("Email"),
        required=True,
        help_text=_("Enter your email address"),
        widget=UnfoldAdminEmailInputWidget(),
    )
    age = forms.IntegerField(
        label=_("Age"),
        required=True,
        min_value=18,
        max_value=120,
        help_text=_("Enter your age"),
        widget=UnfoldAdminIntegerFieldWidget(),
    )
    message = forms.CharField(
        label=_("Message"),
        required=True,
        help_text=_("Enter your message"),
        widget=UnfoldAdminTextareaWidget(),
    )
    subscribe = forms.BooleanField(
        label=_("Subscribe to newsletter"),
        required=True,
        initial=True,
        help_text=_("Toggle to receive our newsletter with updates and offers"),
        widget=UnfoldBooleanSwitchWidget,
    )
    notifications = forms.BooleanField(
        label=_("Receive notifications"),
        required=True,
        initial=False,
        help_text=_("Toggle to receive notifications about your inquiry status"),
        widget=UnfoldBooleanSwitchWidget,
    )
    department = forms.ChoiceField(
        label=_("Department"),
        choices=[
            ("sales", _("Sales")),
            ("marketing", _("Marketing")),
            ("development", _("Development")),
            ("hr", _("Human Resources")),
            ("other", _("Other")),
        ],
        required=True,
        help_text=_("Select the department to contact"),
        widget=UnfoldAdminRadioSelectWidget,
    )
    category = forms.ChoiceField(
        label=_("Category"),
        choices=[
            ("general", _("General Inquiry")),
            ("support", _("Technical Support")),
            ("feedback", _("Feedback")),
            ("other", _("Other")),
        ],
        required=True,
        help_text=_("Select the category of your message"),
        widget=UnfoldAdminCheckboxSelectMultiple,
    )
    priority = forms.TypedChoiceField(
        label=_("Priority"),
        choices=[
            (1, _("Low")),
            (2, _("Medium")),
            (3, _("High")),
        ],
        coerce=int,
        required=True,
        initial=2,
        help_text=_("Select the priority of your message"),
        widget=UnfoldAdminSelectWidget,
    )
    date = forms.DateField(
        label=_("Date"),
        required=True,
        help_text=_("Select a date"),
        widget=UnfoldAdminDateWidget,
    )
    time = forms.TimeField(
        label=_("Time"),
        required=True,
        help_text=_("Select a time"),
        widget=UnfoldAdminTimeWidget,
    )
    datetime = forms.SplitDateTimeField(
        label=_("Date and Time"),
        required=True,
        help_text=_("Select a date and time"),
        widget=UnfoldAdminSplitDateTimeWidget,
    )
    file = forms.FileField(
        label=_("File"),
        required=True,
        help_text=_("Upload a file if needed"),
        widget=UnfoldAdminFileFieldWidget,
    )
    image = forms.ImageField(
        label=_("Image"),
        required=True,
        help_text=_("Upload a image if needed"),
        widget=UnfoldAdminImageFieldWidget,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", _("Submit")))
        self.helper.add_input(Submit("submit", _("Submit 2")))
        self.helper.add_input(Submit("submit", _("Submit 3")))
        self.helper.attrs = {
            "novalidate": "novalidate",
        }
        self.helper.layout = Layout(
            Fieldset(
                _("Custom form"),
                Column(
                    "name",
                    "email",
                    "age",
                    "message",
                    "subscribe",
                    "notifications",
                    "department",
                    "category",
                    "file",
                    "image",
                    "date",
                    "time",
                    "datetime",
                    css_class="flex flex-col gap-5",
                ),
            )
        )


class LoginForm(AuthenticationForm):
    password = forms.CharField(widget=forms.PasswordInput(render_value=True))

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)

        if settings.LOGIN_USERNAME and settings.LOGIN_PASSWORD:
            self.fields["username"].initial = settings.LOGIN_USERNAME
            self.fields["password"].initial = settings.LOGIN_PASSWORD
