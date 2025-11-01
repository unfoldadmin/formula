from django.contrib import messages
from django.forms import modelformset_factory
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView, RedirectView
from unfold.views import UnfoldModelAdminViewMixin

from formula.forms import (
    CustomForm,
    CustomHorizontalForm,
    DriverForm,
    DriverFormHelper,
    DriverFormSet,
)
from formula.models import Driver


class HomeView(RedirectView):
    pattern_name = "admin:index"


class CrispyFormView(UnfoldModelAdminViewMixin, FormView):
    title = _("Crispy form")  # required: custom page header title
    form_class = CustomForm
    success_url = reverse_lazy("admin:index")
    # required: tuple of permissions
    permission_required = (
        "formula.view_driver",
        "formula.add_driver",
        "formula.change_driver",
        "formula.delete_driver",
    )
    template_name = "formula/driver_crispy_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["horizontal_form"] = CustomHorizontalForm()
        return context


class CrispyFormsetView(UnfoldModelAdminViewMixin, FormView):
    title = _("Crispy form with formset")  # required: custom page header title
    success_url = reverse_lazy("admin:crispy_formset")
    # required: tuple of permissions
    permission_required = (
        "formula.view_driver",
        "formula.add_driver",
        "formula.change_driver",
        "formula.delete_driver",
    )
    template_name = "formula/driver_crispy_formset.html"

    def get_form_class(self):
        return modelformset_factory(
            Driver, DriverForm, formset=DriverFormSet, extra=1, can_delete=True
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {
                "queryset": Driver.objects.filter(code__in=["VER", "HAM"]),
            }
        )
        return kwargs

    def form_invalid(self, form):
        messages.error(self.request, _("Formset submitted with errors"))
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, _("Formset submitted successfully"))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            {
                "driver_formset_helper": DriverFormHelper(),
            }
        )
        return context


def dashboard_callback(request, context):
    """
    Here you can pass additional variables to the dashboard
    """

    # context.update(
    #     {
    #         "sample_variable": "sample_value",
    #     }
    # )

    return context
