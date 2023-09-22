from django.contrib import admin, messages
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.db import models
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
    SolarSchedule,
)
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin, StackedInline, TabularInline
from unfold.contrib.filters.admin import RangeDateFilter, RangeNumericFilter
from unfold.contrib.forms.widgets import WysiwygWidget
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from unfold.decorators import action, display
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from formula.models import Circuit, Constructor, Driver, Race, Standing, User
from formula.resources import ConstructorResource

admin.site.unregister(PeriodicTask)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(Group)


@admin.register(PeriodicTask)
class PeriodicTaskAdmin(ModelAdmin):
    pass


@admin.register(IntervalSchedule)
class IntervalScheduleAdmin(ModelAdmin):
    pass


@admin.register(CrontabSchedule)
class CrontabScheduleAdmin(ModelAdmin):
    pass


@admin.register(SolarSchedule)
class SolarScheduleAdmin(ModelAdmin):
    pass


@admin.register(ClockedSchedule)
class ClockedScheduleAdmin(ModelAdmin):
    pass


@admin.register(User)
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


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


class CircuitRaceInline(StackedInline):
    model = Race


@admin.register(Circuit)
class CircuitAdmin(ModelAdmin):
    search_fields = ["name", "city", "country"]
    list_display = ["name", "city", "country"]
    list_filter = ["country"]
    inlines = [CircuitRaceInline]


@admin.register(Constructor)
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
    fields = ["race", "position", "number", "laps"]


@admin.register(Driver)
class DriverAdmin(ModelAdmin):
    search_fields = ["last_name", "first_name", "code"]
    list_filter_submit = True
    list_display = ["last_name", "first_name", "code"]
    inlines = [DriverStandingInline]
    autocomplete_fields = ["constructors"]


@admin.register(Race)
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
        ("laps", RangeNumericFilter),
        ("date", RangeDateFilter),
    ]
    list_filter_submit = True
    list_display = ["circuit", "winner", "year", "laps", "date"]
    autocomplete_fields = ["circuit", "winner"]


@admin.register(Standing)
class StandingAdmin(ModelAdmin):
    search_fields = [
        "race__circuit__name",
        "race__circuit__city",
        "race__circuit__country",
        "driver__first_name",
        "driver__last_name",
    ]
    list_display = ["race", "driver", "constructor", "position", "points"]
    autocomplete_fields = ["driver", "constructor", "race"]
