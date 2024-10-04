import json
import random

from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView, TemplateView
from unfold.views import UnfoldModelAdminViewMixin


class HomeView(RedirectView):
    pattern_name = "admin:index"


class MyClassBasedView(UnfoldModelAdminViewMixin, TemplateView):
    title = "Custom Title"  # required: custom page header title
    permission_required = ()  # required: tuple of permissions
    template_name = "formula/driver_custom_page.html"


def dashboard_callback(request, context):
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

    context.update(
        {
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
                    "metric": f"${intcomma(f"{random.uniform(1000, 9999):.02f}")}",
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
                    "metric": f"${intcomma(f"{random.uniform(1000, 9999):.02f}")}",
                    "footer": mark_safe(
                        f'<strong class="text-green-700 font-semibold dark:text-green-400">+{intcomma(f"{random.uniform(1, 9):.02f}")}%</strong>&nbsp;progress from last week'
                    ),
                },
                {
                    "title": "Product C Performance",
                    "metric": f"${intcomma(f"{random.uniform(1000, 9999):.02f}")}",
                    "footer": mark_safe(
                        f'<strong class="text-green-700 font-semibold dark:text-green-400">+{intcomma(f"{random.uniform(1, 9):.02f}")}%</strong>&nbsp;progress from last week'
                    ),
                },
            ],
            "progress": [
                {
                    "title": "🦆 Social marketing e-book",
                    "description": f"${intcomma(f"{random.uniform(1000, 9999):.02f}")}",
                    "value": random.randint(10, 90),
                },
                {
                    "title": "🦍 Freelancing tasks",
                    "description": f"${intcomma(f"{random.uniform(1000, 9999):.02f}")}",
                    "value": random.randint(10, 90),
                },
                {
                    "title": "🐋 Development coaching",
                    "description": f"${intcomma(f"{random.uniform(1000, 9999):.02f}")}",
                    "value": random.randint(10, 90),
                },
                {
                    "title": "🦑 Product consulting",
                    "description": f"${intcomma(f"{random.uniform(1000, 9999):.02f}")}",
                    "value": random.randint(10, 90),
                },
                {
                    "title": "🐨 Other income",
                    "description": f"${intcomma(f"{random.uniform(1000, 9999):.02f}")}",
                    "value": random.randint(10, 90),
                },
                {
                    "title": "🐶 Course sales",
                    "description": f"${intcomma(f"{random.uniform(1000, 9999):.02f}")}",
                    "value": random.randint(10, 90),
                },
                {
                    "title": "🐻‍❄️ Ads revenue",
                    "description": f"${intcomma(f"{random.uniform(1000, 9999):.02f}")}",
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
                            "backgroundColor": "#f0abfc",
                            "borderColor": "#f0abfc",
                        },
                        {
                            "label": "Example 2",
                            "data": positive,
                            "backgroundColor": "#9333ea",
                        },
                        {
                            "label": "Example 3",
                            "data": negative,
                            "backgroundColor": "#f43f5e",
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
                                {"data": performance_positive, "borderColor": "#9333ea"}
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
                                {"data": performance_negative, "borderColor": "#f43f5e"}
                            ],
                        }
                    ),
                },
            ],
        },
    )

    return context
