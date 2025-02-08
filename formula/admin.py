import random
from functools import lru_cache

from django import forms
from django.contrib import admin, messages
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib.contenttypes.admin import GenericTabularInline
from django.core.validators import EMPTY_VALUES
from django.db import models
from django.db.models import OuterRef, Q, Sum
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.templatetags.static import static
from django.urls import path, reverse_lazy
from django.utils.timezone import now, timedelta
from django.utils.translation import gettext_lazy as _
from django_celery_beat.admin import ClockedScheduleAdmin as BaseClockedScheduleAdmin
from django_celery_beat.admin import CrontabScheduleAdmin as BaseCrontabScheduleAdmin
from django_celery_beat.admin import PeriodicTaskAdmin as BasePeriodicTaskAdmin
from django_celery_beat.admin import PeriodicTaskForm, TaskSelectWidget
from django_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
    SolarSchedule,
)
from guardian.admin import GuardedModelAdmin
from import_export.admin import (
    ExportActionModelAdmin,
    ImportExportModelAdmin,
)
from modeltranslation.admin import TabbedTranslationAdmin
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin, StackedInline, TabularInline
from unfold.components import BaseComponent, register_component
from unfold.contrib.filters.admin import (
    AutocompleteSelectMultipleFilter,
    ChoicesDropdownFilter,
    MultipleRelatedDropdownFilter,
    RangeDateFilter,
    RangeDateTimeFilter,
    RangeNumericFilter,
    SingleNumericFilter,
    TextFilter,
)
from unfold.contrib.forms.widgets import WysiwygWidget
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from unfold.contrib.inlines.admin import NonrelatedStackedInline
from unfold.decorators import action, display
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.widgets import (
    UnfoldAdminCheckboxSelectMultiple,
    UnfoldAdminColorInputWidget,
    UnfoldAdminSelectWidget,
    UnfoldAdminSplitDateTimeWidget,
    UnfoldAdminTextInputWidget,
)

from formula.models import (
    Circuit,
    Constructor,
    Driver,
    DriverStatus,
    Race,
    Standing,
    Tag,
    User,
)
from formula.resources import AnotherConstructorResource, ConstructorResource
from formula.sites import formula_admin_site
from formula.views import MyClassBasedView

admin.site.unregister(PeriodicTask)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(Group)


class UnfoldTaskSelectWidget(UnfoldAdminSelectWidget, TaskSelectWidget):
    pass


class UnfoldPeriodicTaskForm(PeriodicTaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["task"].widget = UnfoldAdminTextInputWidget()
        self.fields["regtask"].widget = UnfoldTaskSelectWidget()


@admin.register(PeriodicTask, site=formula_admin_site)
class PeriodicTaskAdmin(BasePeriodicTaskAdmin, ModelAdmin):
    form = UnfoldPeriodicTaskForm


@admin.register(IntervalSchedule, site=formula_admin_site)
class IntervalScheduleAdmin(ModelAdmin):
    pass


@admin.register(CrontabSchedule, site=formula_admin_site)
class CrontabScheduleAdmin(BaseCrontabScheduleAdmin, ModelAdmin):
    pass


@admin.register(SolarSchedule, site=formula_admin_site)
class SolarScheduleAdmin(ModelAdmin):
    pass


@admin.register(ClockedSchedule, site=formula_admin_site)
class ClockedScheduleAdmin(BaseClockedScheduleAdmin, ModelAdmin):
    pass


class CircuitNonrelatedStackedInline(NonrelatedStackedInline):
    model = Circuit
    fields = ["name", "city", "country"]
    extra = 1
    tab = True

    def get_form_queryset(self, obj):
        return self.model.objects.all().distinct()

    def save_new_instance(self, parent, instance):
        pass


class TagGenericTabularInline(TabularInline, GenericTabularInline):
    model = Tag


@admin.register(User, site=formula_admin_site)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    inlines = [CircuitNonrelatedStackedInline, TagGenericTabularInline]
    list_display = [
        "display_header",
        "is_active",
        "display_staff",
        "display_superuser",
        "display_created",
    ]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (("first_name", "last_name"), "email", "biography"),
                "classes": ["tab"],
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ["tab"],
            },
        ),
        (
            _("Important dates"),
            {
                "fields": ("last_login", "date_joined"),
                "classes": ["tab"],
            },
        ),
    )
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }
    readonly_fields = ["last_login", "date_joined"]

    @display(description=_("User"))
    def display_header(self, instance: User):
        return instance.username

    @display(description=_("Staff"), boolean=True)
    def display_staff(self, instance: User):
        return instance.is_staff

    @display(description=_("Superuser"), boolean=True)
    def display_superuser(self, instance: User):
        return instance.is_superuser

    @display(description=_("Created"))
    def display_created(self, instance: User):
        return instance.created_at


@admin.register(Group, site=formula_admin_site)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        messages.success(
            request,
            _(
                "Donec tristique risus ut lobortis consequat. Vestibulum ac volutpat magna. Quisque dictum mauris a rutrum tincidunt. "
            ),
        )
        messages.info(
            request,
            _(
                "Donec tristique risus ut lobortis consequat. Vestibulum ac volutpat magna. Quisque dictum mauris a rutrum tincidunt. "
            ),
        )
        messages.warning(
            request,
            _(
                "Donec tristique risus ut lobortis consequat. Vestibulum ac volutpat magna. Quisque dictum mauris a rutrum tincidunt. "
            ),
        )
        messages.error(
            request,
            _(
                "Donec tristique risus ut lobortis consequat. Vestibulum ac volutpat magna. Quisque dictum mauris a rutrum tincidunt. "
            ),
        )
        return super().changelist_view(request, extra_context=extra_context)


class CircuitRaceInline(StackedInline):
    model = Race
    autocomplete_fields = ["winner"]


@admin.register(Circuit, site=formula_admin_site)
class CircuitAdmin(ModelAdmin, TabbedTranslationAdmin):
    show_facets = admin.ShowFacets.ALLOW
    search_fields = ["name", "city", "country"]
    list_display = ["name", "city", "country"]
    list_filter = ["country"]
    inlines = [CircuitRaceInline]


@admin.register(Constructor, site=formula_admin_site)
class ConstructorAdmin(ModelAdmin, ImportExportModelAdmin, ExportActionModelAdmin):
    search_fields = ["name"]
    list_display = ["name"]
    resource_classes = [ConstructorResource, AnotherConstructorResource]
    save_as = True
    import_form_class = ImportForm
    export_form_class = ExportForm
    # export_form_class = SelectableFieldsExportForm

    actions_list = ["custom_actions_list"]
    actions_row = [
        "custom_actions_row",
        "custom_actions_row2",
        "custom_actions_row3",
        "custom_actions_row4",
        "custom_actions_row5",
    ]
    actions_detail = ["custom_actions_detail"]
    actions_submit_line = ["custom_actions_submit_line"]

    @action(description="Custom list action", url_path="actions-list-custom-url")
    def custom_actions_list(self, request):
        messages.success(request, "List action has been successfully executed.")
        return redirect(request.META["HTTP_REFERER"])

    @action(description="Custom row action", url_path="actions-row-custom-url")
    def custom_actions_row(self, request, object_id):
        messages.success(
            request, f"Row action has been successfully executed. Object ID {object_id}"
        )
        return redirect(request.META["HTTP_REFERER"])

    @action(description="Custom row action", url_path="actions-row-custom-url")
    def custom_actions_row2(self, request, object_id):
        messages.success(
            request, f"Row action has been successfully executed. Object ID {object_id}"
        )
        return redirect(request.META["HTTP_REFERER"])

    @action(description="Custom row action", url_path="actions-row-custom-url")
    def custom_actions_row3(self, request, object_id):
        messages.success(
            request, f"Row action has been successfully executed. Object ID {object_id}"
        )
        return redirect(request.META["HTTP_REFERER"])

    @action(description="Custom row action", url_path="actions-row-custom-url")
    def custom_actions_row4(self, request, object_id):
        messages.success(
            request, f"Row action has been successfully executed. Object ID {object_id}"
        )
        return redirect(request.META["HTTP_REFERER"])

    @action(description="Custom row action", url_path="actions-row-custom-url")
    def custom_actions_row5(self, request, object_id):
        messages.success(
            request, f"Row action has been successfully executed. Object ID {object_id}"
        )
        return redirect(request.META["HTTP_REFERER"])

    @action(
        description="Custom detail action",
        url_path="actions-detail-custom-url",
        permissions=["custom_actions_detail"],
    )
    def custom_actions_detail(self, request, object_id):
        messages.success(
            request,
            f"Detail action has been successfully executed. Object ID {object_id}",
        )
        return redirect(request.META["HTTP_REFERER"])

    def has_custom_actions_detail_permission(self, request, object_id):
        return True

    @action(description="Custom submit line action")
    def custom_actions_submit_line(self, request, obj):
        messages.success(
            request,
            f"Detail action has been successfully executed. Object ID {obj.pk}",
        )


class FullNameFilter(TextFilter):
    title = _("full name")
    parameter_name = "fullname"

    def queryset(self, request, queryset):
        if self.value() in EMPTY_VALUES:
            return queryset

        return queryset.filter(
            Q(first_name__icontains=self.value()) | Q(last_name__icontains=self.value())
        )


class DriverStandingInline(TabularInline):
    model = Standing
    fields = ["position", "points", "laps", "race", "weight"]
    readonly_fields = ["race"]
    ordering_field = "weight"
    show_change_link = True
    tab = True


class RaceWinnerInline(StackedInline):
    model = Race
    fields = ["winner", "year", "laps", "picture", "weight"]
    readonly_fields = ["winner", "year", "laps"]
    ordering_field = "weight"
    extra = 1
    classes = ["collapse"]


class DriverAdminForm(forms.ModelForm):
    flags = forms.MultipleChoiceField(
        label=_("Flags"),
        choices=[
            ("POPULAR", _("Popular")),
            ("FASTEST", _("Fastest")),
            ("TALENTED", _("Talented")),
        ],
        required=False,
        widget=UnfoldAdminCheckboxSelectMultiple,
    )


@admin.register(Driver, site=formula_admin_site)
class DriverAdmin(GuardedModelAdmin, SimpleHistoryAdmin, ModelAdmin):
    form = DriverAdminForm
    history_list_per_page = 10
    search_fields = ["last_name", "first_name", "code"]
    warn_unsaved_form = True
    compressed_fields = True
    list_filter = [
        FullNameFilter,
        ("constructors", AutocompleteSelectMultipleFilter),
        "is_active",
        "is_hidden",
        ("salary", RangeNumericFilter),
        ("status", ChoicesDropdownFilter),
        ("created_at", RangeDateTimeFilter),
    ]
    list_filter_submit = True
    list_display = [
        "display_header",
        "display_constructor",
        "display_total_points",
        "display_total_wins",
        "display_status",
        "display_code",
    ]
    inlines = [DriverStandingInline, RaceWinnerInline]
    autocomplete_fields = ["constructors"]
    radio_fields = {"status": admin.VERTICAL}
    readonly_fields = ["author", "data", "is_active", "is_hidden"]
    actions_list = [
        "changelist_action",
    ]
    # actions_list = [
    #     "changelist_action",
    #     {
    #         "title": "My Dropdown",
    #         "items": [
    #             "changelist_action",
    #         ],
    #     },
    #     "changelist_action",
    # ]
    actions_detail = ["change_detail_action"]
    list_before_template = "formula/driver_list_before.html"
    list_after_template = "formula/driver_list_after.html"
    change_form_show_cancel_button = True
    change_form_before_template = "formula/driver_change_form_before.html"
    change_form_after_template = "formula/driver_change_form_after.html"

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        form.base_fields["color"].widget = UnfoldAdminColorInputWidget()
        form.base_fields["first_name"].widget = UnfoldAdminTextInputWidget(
            attrs={"class": "first-name-input"}
        )
        return form

    def get_urls(self):
        return super().get_urls() + [
            path(
                "custom-url-path",
                MyClassBasedView.as_view(model_admin=self),
                name="custom_view",
            ),
        ]

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(total_points=Sum("standing__points"))
            .annotate(
                constructor_name=Constructor.objects.filter(
                    standing__driver_id=OuterRef("pk")
                ).values("name")[:1]
            )
            .prefetch_related("race_set", "standing_set")
        )

    @action(description=_("Changelist action"), url_path="changelist-action")
    def changelist_action(self, request):
        return redirect(reverse_lazy("admin:users_user_changelist"))

    @action(description=_("Change detail action"), url_path="change-detail-action")
    def change_detail_action(self, request, object_id):
        try:
            object_id = int(object_id)
        except (TypeError, ValueError) as e:
            raise Http404 from e

        object = get_object_or_404(Driver, pk=object_id)

        class SomeForm(forms.Form):
            # It is important to set a widget coming from Unfold
            from_date = forms.SplitDateTimeField(
                label="From Date", widget=UnfoldAdminSplitDateTimeWidget, required=False
            )
            to_date = forms.SplitDateTimeField(
                label="To Date", widget=UnfoldAdminSplitDateTimeWidget, required=False
            )
            note = forms.CharField(label=_("Note"), widget=UnfoldAdminTextInputWidget)

            class Media:
                js = [
                    "admin/js/vendor/jquery/jquery.js",
                    "admin/js/jquery.init.js",
                    "admin/js/calendar.js",
                    "admin/js/admin/DateTimeShortcuts.js",
                    "admin/js/core.js",
                ]

        form = SomeForm(request.POST or None)

        if request.method == "POST" and form.is_valid():
            # form.cleaned_data["note"]

            messages.success(request, _("Change detail action has been successful."))

            return redirect(
                reverse_lazy("admin:formula_driver_change", args=[object_id])
            )

        return render(
            request,
            "formula/driver_action.html",
            {
                "form": form,
                "object": object,
                "title": _("Change detail action for {}").format(object),
                **self.admin_site.each_context(request),
            },
        )

    @display(description=_("Driver"), header=True)
    def display_header(self, instance: Driver):
        standing = instance.standing_set.all().first()

        if standing:
            return [
                instance.full_name,
                None,
                instance.initials,
                {
                    "path": static("images/avatar.jpg"),
                    "height": 24,
                    "width": 24,
                    "borderless": True,
                    # "squared": True,
                },
            ]

    @display(description=_("Constructor"))
    def display_constructor(self, instance: Driver):
        return instance.constructor_name

    @display(description=_("Total points"), ordering="total_points")
    def display_total_points(self, instance: Driver):
        return instance.total_points

    @display(description=_("Total wins"))
    def display_total_wins(self, instance: Driver):
        return instance.race_set.count()

    @display(
        description=_("Status"),
        label={
            DriverStatus.INACTIVE: "danger",
            DriverStatus.ACTIVE: "success",
        },
    )
    def display_status(self, instance: Driver):
        if instance.status:
            return instance.status

        return None

    @display(description=_("Code"), label=True)
    def display_code(self, instance: Driver):
        return instance.code


@admin.register(Race, site=formula_admin_site)
class RaceAdmin(ModelAdmin):
    date_hierarchy = "date"
    search_fields = [
        "circuit__name",
        "circuit__city",
        "circuit__country",
        "winner__first_name",
        "winner__last_name",
    ]
    list_filter = [
        ("circuit", MultipleRelatedDropdownFilter),
        ("year", RangeNumericFilter),
        ("laps", SingleNumericFilter),
        ("date", RangeDateFilter),
        ("created_at", RangeDateTimeFilter),
    ]
    list_filter_sheet = False
    list_filter_submit = True
    raw_id_fields = ["circuit", "winner"]
    list_display = ["circuit", "winner", "year", "laps", "date"]
    list_fullwidth = True
    autocomplete_fields = ["circuit", "winner"]


@admin.register(Standing, site=formula_admin_site)
class StandingAdmin(ModelAdmin):
    list_disable_select_all = True
    search_fields = [
        "race__circuit__name",
        "race__circuit__city",
        "race__circuit__country",
        "driver__first_name",
        "driver__last_name",
    ]
    list_display = ["race", "driver", "constructor", "position", "points"]
    list_filter = ["driver"]
    autocomplete_fields = ["driver", "constructor", "race"]


try:
    from unfold_studio.admin import StudioOptionAdmin
    from unfold_studio.models import StudioOption

    @admin.register(StudioOption, site=formula_admin_site)
    class StudioOptionAdmin(StudioOptionAdmin, ModelAdmin):
        pass
except (ImportError, RuntimeError):
    # unfold_studio is not installed
    pass


@lru_cache
def tracker_random_data():
    data = []

    for _i in range(1, 64):
        has_value = random.choice([True, True, True, True, False])
        color = None
        tooltip = None

        if has_value:
            value = random.randint(2, 6)
            color = "bg-primary-500"
            tooltip = f"Value {value}"

        data.append(
            {
                "color": color,
                "tooltip": tooltip,
            }
        )

    return data


@register_component
class TrackerComponent(BaseComponent):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["data"] = tracker_random_data()
        return context


@lru_cache
def cohort_random_data():
    rows = []
    headers = []
    cols = []

    dates = reversed(
        [(now() - timedelta(days=x)).strftime("%B %d, %Y") for x in range(8)]
    )
    groups = range(1, 10)

    for row_index, date in enumerate(dates):
        cols = []

        for col_index, _col in enumerate(groups):
            color_index = 8 - row_index - col_index
            col_classes = []

            if color_index > 0:
                col_classes.append(
                    f"bg-primary-{color_index}00 dark:bg-primary-{9 - color_index}00"
                )

            if color_index >= 4:
                col_classes.append("text-white dark:text-base-600")

            value = random.randint(
                4000 - (col_index * row_index * 225),
                5000 - (col_index * row_index * 225),
            )

            subtitle = f"{random.randint(10, 100)}%"

            if value <= 0:
                value = 0
                subtitle = None

            cols.append(
                {
                    "value": value,
                    "color": " ".join(col_classes),
                    "subtitle": subtitle,
                }
            )

        rows.append(
            {
                "header": {
                    "title": date,
                    "subtitle": f"Total {sum(col['value'] for col in cols):,}",
                },
                "cols": cols,
            }
        )

    for index, group in enumerate(groups):
        total = sum(row["cols"][index]["value"] for row in rows)

        headers.append(
            {
                "title": f"Group #{group}",
                "subtitle": f"Total {total:,}",
            }
        )

    return {
        "headers": headers,
        "rows": rows,
    }


@register_component
class CohortComponent(BaseComponent):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["data"] = cohort_random_data()
        return context
