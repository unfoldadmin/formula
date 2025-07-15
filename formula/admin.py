import json
import random
from functools import lru_cache

from constance.admin import Config, ConstanceAdmin
from django import forms
from django.contrib import admin, messages
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.core.validators import EMPTY_VALUES
from django.db import models
from django.db.models import OuterRef, Q, Sum
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.urls import path, reverse_lazy
from django.utils.html import format_html
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
from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin
from modeltranslation.admin import TabbedTranslationAdmin
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import GenericTabularInline, ModelAdmin, StackedInline, TabularInline
from unfold.components import BaseComponent, register_component
from unfold.contrib.filters.admin import (
    AllValuesCheckboxFilter,
    AutocompleteSelectMultipleFilter,
    BooleanRadioFilter,
    CheckboxFilter,
    ChoicesCheckboxFilter,
    RangeDateFilter,
    RangeDateTimeFilter,
    RangeNumericFilter,
    RelatedCheckboxFilter,
    RelatedDropdownFilter,
    SingleNumericFilter,
    SliderNumericFilter,
    TextFilter,
)
from unfold.contrib.forms.widgets import WysiwygWidget
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from unfold.contrib.inlines.admin import NonrelatedStackedInline
from unfold.decorators import action, display
from unfold.enums import ActionVariant
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.paginator import InfinitePaginator
from unfold.sections import TableSection, TemplateSection
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
    DriverWithFilters,
    Profile,
    Race,
    Standing,
    Tag,
    User,
)
from formula.resources import AnotherConstructorResource, ConstructorResource
from formula.sites import formula_admin_site
from formula.views import CrispyFormsetView, CrispyFormView

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
    per_page = 10

    def get_form_queryset(self, obj):
        return self.model.objects.all().distinct()

    def save_new_instance(self, parent, instance):
        pass


class TagGenericTabularInline(GenericTabularInline):
    model = Tag


class UserDriverTabularInline(TabularInline):
    model = Driver
    fk_name = "author"
    autocomplete_fields = ["standing"]
    fields = ["first_name", "last_name", "code", "status", "salary", "category"]


class UserProfileTabularInline(TabularInline):
    model = Profile


@admin.register(User, site=formula_admin_site)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_fullwidth = True
    list_filter = [
        ("is_staff", BooleanRadioFilter),
        ("is_superuser", BooleanRadioFilter),
        ("is_active", BooleanRadioFilter),
        ("groups", RelatedCheckboxFilter),
    ]
    list_filter_submit = True
    list_filter_sheet = False
    inlines = [
        CircuitNonrelatedStackedInline,
        TagGenericTabularInline,
        UserDriverTabularInline,
        UserProfileTabularInline,
    ]
    compressed_fields = True
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
    show_full_result_count = False

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


class DriverTableSection(TableSection):
    related_name = "driver_set"
    fields = ["first_name", "last_name", "code"]


@admin.register(Constructor, site=formula_admin_site)
class ConstructorAdmin(ModelAdmin, ImportExportModelAdmin, ExportActionModelAdmin):
    search_fields = ["name"]
    list_display = ["name"]
    list_sections = [DriverTableSection]
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

    @action(
        description="Custom list action",
        url_path="actions-list-custom-url",
        permissions=[
            "custom_actions_list",
            "another_custom_actions_list",
        ],
    )
    def custom_actions_list(self, request):
        messages.success(request, "List action has been successfully executed.")
        return redirect(request.headers["referer"])

    def has_custom_actions_list_permission(self, request):
        return request.user.is_superuser

    def has_another_custom_actions_list_permission(self, request):
        return request.user.is_staff

    @action(
        description=_("Rebuild Index"),
        url_path="actions-row-custom-url",
        permissions=[
            "custom_actions_row",
            "another_custom_actions_row",
        ],
    )
    def custom_actions_row(self, request, object_id):
        messages.success(
            request, f"Row action has been successfully executed. Object ID {object_id}"
        )
        return redirect(
            request.headers.get("referer")
            or reverse_lazy("admin:formula_constructor_changelist")
        )

    def has_custom_actions_row_permission(self, request, object_id=None):
        return request.user.is_superuser

    def has_another_custom_actions_row_permission(self, request, object_id=None):
        return request.user.is_staff

    @action(description=_("Reindex Cache"), url_path="actions-row-reindex-cache")
    def custom_actions_row2(self, request, object_id):
        messages.success(
            request, f"Row action has been successfully executed. Object ID {object_id}"
        )
        return redirect(
            request.headers.get("referer")
            or reverse_lazy("admin:formula_constructor_changelist")
        )

    @action(description=_("Deploy Hypervisor"), url_path="actions-row-hyperdrive")
    def custom_actions_row3(self, request, object_id):
        messages.success(
            request, f"Row action has been successfully executed. Object ID {object_id}"
        )
        return redirect(
            request.headers.get("referer")
            or reverse_lazy("admin:formula_constructor_changelist")
        )

    @action(description=_("Sync Containers"), url_path="actions-row-sync-containers")
    def custom_actions_row4(self, request, object_id):
        messages.success(
            request, f"Row action has been successfully executed. Object ID {object_id}"
        )
        return redirect(
            request.headers.get("referer")
            or reverse_lazy("admin:formula_constructor_changelist")
        )

    @action(
        description=_("Never visible"),
        url_path="actions-row-deploy-containers",
        permissions=["custom_row_action_false", "custom_row_action_true"],
    )
    def custom_actions_row5(self, request, object_id):
        messages.success(
            request, f"Row action has been successfully executed. Object ID {object_id}"
        )
        return redirect(
            request.headers.get("referer")
            or reverse_lazy("admin:formula_constructor_changelist")
        )

    def has_custom_row_action_false_permission(self, request):
        return False

    def has_custom_row_action_true_permission(self, request):
        return True

    @action(
        description="Custom detail action",
        url_path="actions-detail-custom-url",
        permissions=["custom_actions_detail", "another_custom_actions_detail"],
    )
    def custom_actions_detail(self, request, object_id):
        messages.success(
            request,
            f"Detail action has been successfully executed. Object ID {object_id}",
        )
        return redirect(request.headers["referer"])

    def has_custom_actions_detail_permission(self, request, object_id):
        return request.user.is_superuser

    def has_another_custom_actions_detail_permission(self, request, object_id):
        return request.user.is_staff

    @action(
        description="Custom submit line action",
        permissions=[
            "custom_actions_submit_line",
            "another_custom_actions_submit_line",
        ],
    )
    def custom_actions_submit_line(self, request, obj):
        messages.success(
            request,
            f"Detail action has been successfully executed. Object ID {obj.pk}",
        )

    def has_custom_actions_submit_line_permission(self, request, obj):
        return request.user.is_superuser

    def has_another_custom_actions_submit_line_permission(self, request, obj):
        return request.user.is_staff


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
    extra = 0
    per_page = 5
    tab = True

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("race", "driver")
            .prefetch_related("race__circuit")
        )


class RaceWinnerInline(StackedInline):
    model = Race
    fields = ["winner", "year", "laps", "picture", "weight"]
    readonly_fields = ["winner", "year", "laps"]
    ordering_field = "weight"
    extra = 0
    per_page = 15
    tab = True


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
    first_name = forms.CharField(
        label=_("First name"),
        widget=UnfoldAdminTextInputWidget,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["first_name"].widget.attrs.update(
            {
                "prefix_icon": "search",
                "suffix_icon": "euro",
            }
        )


class ContructorTableSection(TableSection):
    # verbose_name = _("Constructors - Many to many relationship")
    related_name = "constructors"
    height = 380
    fields = [
        "name",
        "custom_field",
    ]

    @admin.display(description=_("Points"))
    def custom_field(self, instance):
        return random.randint(0, 50)


class ChartSection(TemplateSection):
    template_name = "formula/driver_section.html"


class DriverAdminMixin(ModelAdmin):
    list_sections = [ContructorTableSection, ChartSection]
    list_sections_classes = "lg:grid-cols-2"
    form = DriverAdminForm
    history_list_per_page = 10
    search_fields = ["last_name", "first_name", "code"]
    warn_unsaved_form = True
    compressed_fields = True
    list_display = [
        "display_header",
        "display_constructor",
        "display_total_points",
        "display_total_wins",
        "category",
        "display_status",
        "display_code",
    ]
    inlines = [
        DriverStandingInline,
        RaceWinnerInline,
    ]
    conditional_fields = {
        "conditional_field_active": "status == 'ACTIVE'",
        "conditional_field_inactive": "status == 'INACTIVE'",
    }
    autocomplete_fields = [
        "constructors",
        "editor",
        "standing",
    ]
    radio_fields = {
        "status": admin.VERTICAL,
    }
    readonly_fields = [
        # "author",
        "data",
    ]
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
            .prefetch_related(
                "constructors",
                "race_set",
                "race_set__circuit",
                "standings",
                "standings__race",
                "standings__race__circuit",
            )
        )

    @display(description=_("Driver"), header=True)
    def display_header(self, instance: Driver) -> list:
        standing = instance.standings.all().first()

        if not standing:
            return []

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

    @display(description=_("Constructor"), dropdown=True)
    def display_constructor(self, instance: Driver):
        total = instance.constructors.all().count()
        items = []

        for constructor in instance.constructors.all():
            title = format_html(
                """
                <div class="flex flex-row gap-2 items-center">
                    <span class="truncate">{}</span>
                    <a href="" class="leading-none ml-auto">
                        <span class="material-symbols-outlined leading-none text-base-500">ungroup</span>
                    </a>
                </div>
                """,
                constructor.name,
            )
            items.append(
                {
                    "title": title,
                    # "link": "#",  # Optional: Add a href attribute
                }
            )

        # Display custom string if no records found
        if total == 0:
            return "-"

        return {
            "title": f"{total} contructors",
            "items": items,
            "striped": True,
            # "height": 202,  # Optional, max line height 30px
            # "width": 320,  # Optional
        }

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


@admin.register(Driver, site=formula_admin_site)
class DriverAdmin(GuardedModelAdmin, SimpleHistoryAdmin, DriverAdminMixin):
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "first_name",
                    "last_name",
                    "salary",
                    "category",
                    "picture",
                    "born_at",
                    "last_race_at",
                    "best_time",
                    "first_race_at",
                    "resume",
                    "author",
                    "editor",
                    "standing",
                    "constructors",
                    "code",
                    "color",
                    "link",
                    "data",
                ]
            },
        ),
        (
            _("Conditional fields"),
            {
                "classes": ["tab"],
                "fields": [
                    "status",
                    "conditional_field_active",
                    "conditional_field_inactive",
                ],
            },
        ),
        (
            _("Boolean fields"),
            {
                "classes": ["tab"],
                "fields": [
                    "is_retired",
                    "is_active",
                    "is_hidden",
                ],
            },
        ),
    ]
    actions_list = [
        "changelist_action_should_not_be_visible",
        "changelist_action1",
        "changelist_action4",
        {
            "title": _("More"),
            "variant": ActionVariant.PRIMARY,
            "items": [
                "changelist_action3",
                "changelist_action4",
                "changelist_action5",
            ],
        },
    ]
    actions_detail = [
        "change_detail_action3",
        "change_detail_action",
        {
            "title": _("More"),
            "items": [
                "change_detail_action1",
                "change_detail_action2",
            ],
        },
    ]

    def get_urls(self):
        return super().get_urls() + [
            path(
                "crispy-with-formset",
                self.admin_site.admin_view(CrispyFormsetView.as_view(model_admin=self)),
                name="crispy_formset",
            ),
            path(
                "crispy-form",
                self.admin_site.admin_view(CrispyFormView.as_view(model_admin=self)),
                name="crispy_form",
            ),
        ]

    @action(description=_("Initialize nodes"), icon="hub")
    def changelist_action1(self, request):
        messages.success(
            request, _("Changelist action has been successfully executed.")
        )
        return redirect(reverse_lazy("admin:formula_driver_changelist"))

    @action(
        description=_("Sync DB replicas"),
        icon="sync",
    )
    def changelist_action3(self, request):
        messages.success(
            request, _("Changelist action has been successfully executed.")
        )
        return redirect(reverse_lazy("admin:formula_driver_changelist"))

    @action(description=_("Rebuild cache index"), icon="book_4")
    def changelist_action4(self, request):
        messages.success(
            request, _("Changelist action has been successfully executed.")
        )
        return redirect(reverse_lazy("admin:formula_driver_changelist"))

    @action(description=_("Optimize queries"), icon="database")
    def changelist_action5(self, request):
        messages.success(
            request, _("Changelist action has been successfully executed.")
        )
        return redirect(reverse_lazy("admin:formula_driver_changelist"))

    @action(
        description=_("Should not be visible"), permissions=["should_not_be_visible"]
    )
    def changelist_action_should_not_be_visible(self, request):
        messages.success(
            request, _("Changelist action has been successfully executed.")
        )
        return redirect(reverse_lazy("admin:formula_driver_changelist"))

    def has_should_not_be_visible_permission(self, request):
        return False

    @action(
        description=_("Action with form"),
        url_path="change-detail-action",
        permissions=["change_detail_action"],
    )
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

    def has_change_detail_action_permission(self, request, object_id=None):
        return request.user.is_superuser

    @action(description=_("Revalidate cache"), permissions=["revalidate_cache"])
    def change_detail_action1(self, request, object_id):
        messages.success(
            request, _("Change detail action has been successfully executed.")
        )
        return redirect(reverse_lazy("admin:formula_driver_change", args=[object_id]))

    def has_revalidate_cache_permission(self, request, object_id):
        return request.user.is_superuser

    @action(description=_("Deactivate object"))
    def change_detail_action2(self, request, object_id):
        messages.success(
            request, _("Change detail action has been successfully executed.")
        )
        return redirect(reverse_lazy("admin:formula_driver_change", args=[object_id]))

    @action(
        description=_("Never visible"),
        permissions=["change_detail_false"],
    )
    def change_detail_action3(self, request, object_id):
        messages.success(
            request, _("Change detail action has been successfully executed.")
        )
        return redirect(reverse_lazy("admin:formula_driver_change", args=[object_id]))

    def has_change_detail_false_permission(self, request, object_id=None):
        return False


class DriverCustomCheckboxFilter(CheckboxFilter):
    title = _("Custom status")
    parameter_name = "custom_status"

    def lookups(self, request, model_admin):
        return DriverStatus.choices

    def queryset(self, request, queryset):
        if self.value() not in EMPTY_VALUES:
            return queryset.filter(status__in=self.value())
        elif self.parameter_name in self.used_parameters:
            return queryset.filter(status=self.used_parameters[self.parameter_name])

        return queryset


@admin.register(DriverWithFilters, site=formula_admin_site)
class DriverWithFiltersAdmin(DriverAdminMixin):
    list_fullwidth = True
    list_filter = [
        FullNameFilter,
        ("constructors", AutocompleteSelectMultipleFilter),
        ("race__circuit", RelatedDropdownFilter),
        ("salary", SliderNumericFilter),
        ("status", ChoicesCheckboxFilter),
        ("category", AllValuesCheckboxFilter),
        DriverCustomCheckboxFilter,
        ("is_hidden", BooleanRadioFilter),
        ("is_active", BooleanRadioFilter),
    ]
    list_filter_sheet = False
    list_filter_submit = True


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
        ("circuit", RelatedCheckboxFilter),
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
    # list_disable_select_all = True
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
    readonly_fields = ["laps"]
    paginator = InfinitePaginator
    show_full_result_count = False
    list_disable_select_all = True
    list_per_page = 10


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
                col_classes.append("text-white")

            if color_index >= 6:
                col_classes.append("dark:text-base-800")

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


@register_component
class DriverActiveComponent(BaseComponent):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["children"] = render_to_string(
            "formula/helpers/kpi_progress.html",
            {
                "total": Driver.objects.filter(status=DriverStatus.ACTIVE).count(),
                "progress": "positive",
                "percentage": "2.8%",
            },
        )
        return context


@register_component
class DriverInactiveComponent(BaseComponent):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["children"] = render_to_string(
            "formula/helpers/kpi_progress.html",
            {
                "total": Driver.objects.filter(status=DriverStatus.INACTIVE).count(),
                "progress": "negative",
                "percentage": "-12.8%",
            },
        )
        return context


@register_component
class DriverTotalPointsComponent(BaseComponent):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["children"] = render_to_string(
            "formula/helpers/kpi_progress.html",
            {
                "total": Standing.objects.aggregate(total_points=Sum("points"))[
                    "total_points"
                ],
                "progress": "positive",
                "percentage": "24.2%",
            },
        )
        return context


@register_component
class DriverRacesComponent(BaseComponent):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["children"] = render_to_string(
            "formula/helpers/kpi_progress.html",
            {
                "total": Race.objects.count(),
                "progress": "negative",
                "percentage": "-10.0%",
            },
        )
        return context


@register_component
class DriverSectionChangeComponent(BaseComponent):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        WEEKDAYS = [
            "Mon",
            "Tue",
            "Wed",
            "Thu",
            "Fri",
            "Sat",
            "Sun",
        ]
        OF_DAYS = 21

        context["data"] = json.dumps(
            {
                "labels": [WEEKDAYS[day % 7] for day in range(1, OF_DAYS)],
                "datasets": [
                    {
                        "data": [
                            [1, random.randrange(8, OF_DAYS)] for i in range(1, OF_DAYS)
                        ],
                        "backgroundColor": "var(--color-primary-600)",
                    }
                ],
            }
        )
        return context


@admin.register(Config, site=formula_admin_site)
class ConstanceConfigAdmin(ConstanceAdmin):
    pass
