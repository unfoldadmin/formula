from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Div, Fieldset, Layout, Row
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView
from unfold.forms import AuthenticationForm
from unfold.layout import Submit
from unfold.widgets import (
    UnfoldAdminCheckboxSelectMultiple,
    UnfoldAdminDateWidget,
    UnfoldAdminEmailInputWidget,
    UnfoldAdminExpandableTextareaWidget,
    UnfoldAdminFileFieldWidget,
    UnfoldAdminImageFieldWidget,
    UnfoldAdminIntegerFieldWidget,
    UnfoldAdminMoneyWidget,
    UnfoldAdminRadioSelectWidget,
    UnfoldAdminSelect2Widget,
    UnfoldAdminSelectMultipleWidget,
    UnfoldAdminSplitDateTimeWidget,
    UnfoldAdminTextareaWidget,
    UnfoldAdminTextInputWidget,
    UnfoldAdminTimeWidget,
    UnfoldAdminURLInputWidget,
    UnfoldBooleanSwitchWidget,
    UnfoldBooleanWidget,
)

from formula.models import Driver


class HomeView(RedirectView):
    pattern_name = "admin:index"


class CustomFormMixin(forms.Form):
    name = forms.CharField(
        max_length=100,
        label=_("Name"),
        required=True,
        widget=UnfoldAdminTextInputWidget(),
    )
    email = forms.EmailField(
        label=_("Email"),
        required=True,
        widget=UnfoldAdminEmailInputWidget(),
    )
    age = forms.IntegerField(
        label=_("Age"),
        required=True,
        min_value=18,
        max_value=120,
        widget=UnfoldAdminIntegerFieldWidget(),
    )
    url = forms.URLField(
        label=_("URL"),
        required=True,
        widget=UnfoldAdminURLInputWidget(),
    )
    salary = forms.DecimalField(
        label=_("Salary"),
        required=True,
        help_text=_("Enter your salary"),
        widget=UnfoldAdminMoneyWidget(),
    )
    title = forms.CharField(
        label=_("Title"),
        required=True,
        widget=UnfoldAdminExpandableTextareaWidget(),
    )
    message = forms.CharField(
        label=_("Message"),
        required=True,
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
        widget=UnfoldBooleanWidget,
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
        widget=UnfoldAdminSelect2Widget,
    )
    multi_select = forms.MultipleChoiceField(
        label=_("Select Multiple Options"),
        choices=[
            (
                "option_a",
                _(
                    "Option A – Receive timely updates on race schedules, driver announcements, and changes in race venues throughout the season."
                ),
            ),
            (
                "option_b",
                _(
                    "Option B – Get exclusive insights into detailed team strategies, pit stop analytics, and pre-race analyses from experts."
                ),
            ),
            (
                "option_c",
                _(
                    "Option C – Access extensive behind-the-scenes footage, in-depth interviews with top drivers, and special team documentaries."
                ),
            ),
            (
                "option_d",
                _(
                    "Option D – Join VIP events and participate in interactive fan voting for awards with additional community activities."
                ),
            ),
            (
                "option_e",
                _(
                    "Option E – Subscribe to technical analysis, expert commentary, and comprehensive engineering breakdowns of the latest F1 cars."
                ),
            ),
            (
                "option_f",
                _(
                    "Option F – Be the first to know about special promotions, early bird ticket sales, and new official merchandise launches."
                ),
            ),
            (
                "option_g",
                _(
                    "Option G – Receive personalized notifications about your favorite teams, their race results, and tailored race-day summaries."
                ),
            ),
            (
                "option_h",
                _(
                    "Option H – Get early access to new platform features, closed beta program invitations, and direct feedback opportunities."
                ),
            ),
        ],
        required=False,
        help_text=_("You can select more than one option"),
        widget=UnfoldAdminSelectMultipleWidget,
    )
    date = forms.DateField(
        label=_("Date"),
        required=True,
        widget=UnfoldAdminDateWidget,
    )
    time = forms.TimeField(
        label=_("Time"),
        required=True,
        widget=UnfoldAdminTimeWidget,
    )
    datetime = forms.SplitDateTimeField(
        label=_("Date and Time"),
        required=True,
        widget=UnfoldAdminSplitDateTimeWidget,
    )
    file = forms.FileField(
        label=_("File"),
        required=True,
        widget=UnfoldAdminFileFieldWidget,
    )
    image = forms.ImageField(
        label=_("Image"),
        required=True,
        widget=UnfoldAdminImageFieldWidget,
    )


class CustomHorizontalForm(CustomFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.layout = Layout(
            Fieldset(
                _("Custom horizontal form"),
                "name",
                "email",
                "age",
                "url",
                "salary",
                "title",
                "message",
                "subscribe",
                "notifications",
                "department",
                "category",
                "date",
                "time",
                "datetime",
            ),
        )


class CustomForm(CustomFormMixin):
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
            Row(
                Column(
                    Fieldset(
                        _("Custom form"),
                        Column(
                            Row(
                                Div("name", css_class="w-1/2"),
                                Div("email", css_class="w-1/2"),
                            ),
                            Row(
                                Div("age", css_class="w-1/2"),
                                Div("url", css_class="w-1/2"),
                            ),
                            "salary",
                            "priority",
                            "multi_select",
                            css_class="gap-5",
                        ),
                    ),
                    Fieldset(
                        _("Textarea & expandable textarea widgets"),
                        "title",
                        "message",
                    ),
                    css_class="lg:w-1/2",
                ),
                Column(
                    Fieldset(
                        _("Radio & checkbox widgets"),
                        Column(
                            "subscribe",
                            "notifications",
                            Row(
                                Div("department", css_class="w-1/2"),
                                Div("category", css_class="w-1/2"),
                            ),
                            css_class="gap-5",
                        ),
                    ),
                    Fieldset(
                        _("File upload widgets"),
                        Column(
                            "file",
                            "image",
                            css_class="gap-5",
                        ),
                    ),
                    Fieldset(
                        _("Date & time widgets"),
                        Column(
                            "date",
                            "time",
                            "datetime",
                            css_class="gap-5",
                        ),
                    ),
                    css_class="lg:w-1/2",
                ),
                css_class="mb-8",
            ),
        )


class DriverFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.template = "unfold_crispy/layout/table_inline_formset.html"
        self.form_id = "driver-formset"
        self.form_add = True
        self.form_show_labels = False
        self.attrs = {
            "novalidate": "novalidate",
        }
        self.add_input(Submit("submit", _("Another submit")))
        self.add_input(Submit("submit", _("Submit")))


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = [
            "first_name",
            "last_name",
            "code",
        ]
        widgets = {
            "first_name": UnfoldAdminTextInputWidget(),
            "last_name": UnfoldAdminTextInputWidget(),
            "code": UnfoldAdminTextInputWidget(),
        }

    def clean(self):
        raise ValidationError("Testing form wide error messages.")


class DriverFormSet(forms.BaseModelFormSet):
    def clean(self):
        raise ValidationError("Testing formset wide error messages.")


class LoginForm(AuthenticationForm):
    password = forms.CharField(widget=forms.PasswordInput(render_value=True))

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)

        if settings.LOGIN_USERNAME and settings.LOGIN_PASSWORD:
            self.fields["username"].initial = settings.LOGIN_USERNAME
            self.fields["password"].initial = settings.LOGIN_PASSWORD
