from django.contrib import admin, messages
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.db import models
from django.db.models import OuterRef, Sum
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
    SolarSchedule,
)
from django_svelte_jsoneditor.widgets import SvelteJSONEditorWidget
from guardian.admin import GuardedModelAdmin
from import_export.admin import ImportExportModelAdmin
from modeltranslation.admin import TabbedTranslationAdmin
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin, StackedInline, TabularInline
from unfold.contrib.filters.admin import (
    RangeDateFilter,
    RangeNumericFilter,
    SingleNumericFilter,
)
from unfold.contrib.forms.widgets import WysiwygWidget
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from unfold.decorators import action, display
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.widgets import UnfoldAdminColorInputWidget

from formula.models import (
    Circuit,
    Constructor,
    Driver,
    DriverStatus,
    Race,
    Standing,
    User,
)
from formula.resources import ConstructorResource
from formula.sites import formula_admin_site

admin.site.unregister(PeriodicTask)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(Group)


@admin.register(PeriodicTask, site=formula_admin_site)
class PeriodicTaskAdmin(ModelAdmin):
    pass


@admin.register(IntervalSchedule, site=formula_admin_site)
class IntervalScheduleAdmin(ModelAdmin):
    pass


@admin.register(CrontabSchedule, site=formula_admin_site)
class CrontabScheduleAdmin(ModelAdmin):
    pass


@admin.register(SolarSchedule, site=formula_admin_site)
class SolarScheduleAdmin(ModelAdmin):
    pass


@admin.register(ClockedSchedule, site=formula_admin_site)
class ClockedScheduleAdmin(ModelAdmin):
    pass


@admin.register(User, site=formula_admin_site)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
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
            {"fields": (("first_name", "last_name"), "email", "biography")},
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
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
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

    @display(description=_("User"), header=True)
    def display_header(self, instance: User):
        return instance.full_name, instance.email

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
    pass


class CircuitRaceInline(StackedInline):
    model = Race
    autocomplete_fields = ["winner"]


@admin.register(Circuit, site=formula_admin_site)
class CircuitAdmin(ModelAdmin, TabbedTranslationAdmin):
    search_fields = ["name", "city", "country"]
    list_display = ["name", "city", "country"]
    list_filter = ["country"]
    inlines = [CircuitRaceInline]
    formfield_overrides = {
        models.JSONField: {
            "widget": SvelteJSONEditorWidget,
        }
    }


@admin.register(Constructor, site=formula_admin_site)
class ConstructorAdmin(ModelAdmin, ImportExportModelAdmin):
    search_fields = ["name"]
    list_display = [
        "name",
    ]
    resource_classes = [ConstructorResource]

    import_form_class = ImportForm
    export_form_class = ExportForm

    actions_list = ["custom_actions_list"]
    actions_row = ["custom_actions_row"]
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

    @action(description="Custom detail action", url_path="actions-detail-custom-url")
    def custom_actions_detail(self, request, object_id):
        messages.success(
            request,
            f"Detail action has been successfully executed. Object ID {object_id}",
        )
        return redirect(request.META["HTTP_REFERER"])

    @action(description="Custom submit line action")
    def custom_actions_submit_line(self, request, obj):
        messages.success(
            request,
            f"Detail action has been successfully executed. Object ID {obj.pk}",
        )


class DriverStandingInline(TabularInline):
    model = Standing
    fields = ["race", "position", "points", "laps"]
    readonly_fields = ["race"]
    max_num = 0


@admin.register(Driver, site=formula_admin_site)
class DriverAdmin(GuardedModelAdmin, SimpleHistoryAdmin, ModelAdmin):
    search_fields = ["last_name", "first_name", "code"]
    list_filter_submit = True
    list_display = [
        "display_header",
        "display_total_points",
        "display_total_wins",
        "display_status",
        "display_code",
    ]
    inlines = [DriverStandingInline]
    autocomplete_fields = [
        "constructors",
    ]
    radio_fields = {"status": admin.VERTICAL}
    readonly_fields = ["data"]

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        form.base_fields["color"].widget = UnfoldAdminColorInputWidget()
        return form

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
            .prefetch_related("race_set")
        )

    @display(description=_("Driver"), header=True)
    def display_header(self, instance: Driver):
        standing = instance.standing_set.all().first()

        if standing:
            return [
                instance.full_name,
                instance.constructor_name,
                instance.initials,
            ]

    @display(description=_("Total points"), ordering="total_points")
    def display_total_points(self, instance: Driver):
        return instance.total_points

    @display(description=_("Total wins"), ordering="total_wins")
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
    search_fields = [
        "circuit__name",
        "circuit__city",
        "circuit__country",
        "winner__first_name",
        "winner__last_name",
    ]
    list_filter = [
        ("year", RangeNumericFilter),
        ("laps", SingleNumericFilter),
        ("date", RangeDateFilter),
    ]
    list_filter_submit = True
    list_display = ["circuit", "winner", "year", "laps", "date"]
    autocomplete_fields = ["circuit", "winner"]


@admin.register(Standing, site=formula_admin_site)
class StandingAdmin(ModelAdmin):
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
