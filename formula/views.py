import json
import random
from functools import lru_cache

from django.contrib import messages
from django.contrib.humanize.templatetags.humanize import intcomma
from django.forms import modelformset_factory
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
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
    context.update(random_data())
    return context


@lru_cache
def random_data():
    WEEKDAYS = [
        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Sat",
        "Sun",
    ]

    positive = [[1, random.randrange(8, 28)] for i in range(1, 28)]
    negative = [[-1, -random.randrange(8, 28)] for i in range(1, 28)]
    average = [r[1] - random.randint(3, 5) for r in positive]
    performance_positive = [[1, random.randrange(8, 28)] for i in range(1, 28)]
    performance_negative = [[-1, -random.randrange(8, 28)] for i in range(1, 28)]

    return {
        "navigation": [
            {"title": _("Dashboard"), "link": "/", "active": True},
            {"title": _("Analytics"), "link": "#"},
            {"title": _("Settings"), "link": "#"},
        ],
        "filters": [
            {"title": _("All"), "link": "#", "active": True},
            {
                "title": _("New"),
                "link": "#",
            },
        ],
        "kpi": [
            {
                "title": "Product A Performance",
                "metric": f"${intcomma(f'{random.uniform(1000, 9999):.02f}')}",
                "footer": mark_safe(
                    f'<strong class="text-green-700 font-semibold dark:text-green-400">+{intcomma(f"{random.uniform(1, 9):.02f}")}%</strong>&nbsp;progress from last week'
                ),
                "chart": json.dumps(
                    {
                        "labels": [WEEKDAYS[day % 7] for day in range(1, 28)],
                        "datasets": [{"data": average, "borderColor": "#9333ea"}],
                    }
                ),
            },
            {
                "title": "Product B Performance",
                "metric": f"${intcomma(f'{random.uniform(1000, 9999):.02f}')}",
                "footer": mark_safe(
                    f'<strong class="text-green-700 font-semibold dark:text-green-400">+{intcomma(f"{random.uniform(1, 9):.02f}")}%</strong>&nbsp;progress from last week'
                ),
            },
            {
                "title": "Product C Performance",
                "metric": f"${intcomma(f'{random.uniform(1000, 9999):.02f}')}",
                "footer": mark_safe(
                    f'<strong class="text-green-700 font-semibold dark:text-green-400">+{intcomma(f"{random.uniform(1, 9):.02f}")}%</strong>&nbsp;progress from last week'
                ),
            },
        ],
        "progress": [
            {
                "title": "Social marketing e-book",
                "description": f"${intcomma(f'{random.uniform(1000, 9999):.02f}')}",
                "value": random.randint(10, 90),
            },
            {
                "title": "Freelancing tasks",
                "description": f"${intcomma(f'{random.uniform(1000, 9999):.02f}')}",
                "value": random.randint(10, 90),
            },
            {
                "title": "Development coaching",
                "description": f"${intcomma(f'{random.uniform(1000, 9999):.02f}')}",
                "value": random.randint(10, 90),
            },
            {
                "title": "Product consulting",
                "description": f"${intcomma(f'{random.uniform(1000, 9999):.02f}')}",
                "value": random.randint(10, 90),
            },
            {
                "title": "Other income",
                "description": f"${intcomma(f'{random.uniform(1000, 9999):.02f}')}",
                "value": random.randint(10, 90),
            },
            {
                "title": "Course sales",
                "description": f"${intcomma(f'{random.uniform(1000, 9999):.02f}')}",
                "value": random.randint(10, 90),
            },
            {
                "title": "Ads revenue",
                "description": f"${intcomma(f'{random.uniform(1000, 9999):.02f}')}",
                "value": random.randint(10, 90),
            },
            {
                "title": "Customer Retention Rate",
                "description": f"${intcomma(f'{random.uniform(1000, 9999):.02f}')}",
                "value": random.randint(10, 90),
            },
        ],
        "chart": json.dumps(
            {
                "labels": [WEEKDAYS[day % 7] for day in range(1, 28)],
                "datasets": [
                    {
                        "label": "Example 1",
                        "type": "line",
                        "data": average,
                        "borderColor": "var(--color-primary-500)",
                    },
                    {
                        "label": "Example 2",
                        "data": positive,
                        "backgroundColor": "var(--color-primary-700)",
                    },
                    {
                        "label": "Example 3",
                        "data": negative,
                        "backgroundColor": "var(--color-primary-300)",
                    },
                ],
            }
        ),
        "performance": [
            {
                "title": _("Last week revenue"),
                "metric": "$1,234.56",
                "footer": mark_safe(
                    '<strong class="text-green-600 font-medium">+3.14%</strong>&nbsp;progress from last week'
                ),
                "chart": json.dumps(
                    {
                        "labels": [WEEKDAYS[day % 7] for day in range(1, 28)],
                        "datasets": [
                            {
                                "data": performance_positive,
                                "borderColor": "var(--color-primary-700)",
                            }
                        ],
                    }
                ),
            },
            {
                "title": _("Last week expenses"),
                "metric": "$1,234.56",
                "footer": mark_safe(
                    '<strong class="text-green-600 font-medium">+3.14%</strong>&nbsp;progress from last week'
                ),
                "chart": json.dumps(
                    {
                        "labels": [WEEKDAYS[day % 7] for day in range(1, 28)],
                        "datasets": [
                            {
                                "data": performance_negative,
                                "borderColor": "var(--color-primary-300)",
                            }
                        ],
                    }
                ),
            },
        ],
        "table_data": {
            "headers": [_("Day"), _("Income"), _("Expenses")],
            "rows": [
                ["22-10-2025", "$2,341.89", "$1,876.45"],
                ["23-10-2025", "$1,987.23", "$2,109.67"],
                ["24-10-2025", "$3,456.78", "$1,543.21"],
                ["25-10-2025", "$1,765.43", "$2,987.65"],
                ["26-10-2025", "$2,876.54", "$1,234.56"],
                ["27-10-2025", "$1,543.21", "$2,765.43"],
                ["28-10-2025", "$3,210.98", "$1,987.65"],
            ],
        },
    }
