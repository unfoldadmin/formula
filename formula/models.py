from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
from simple_history.models import HistoricalRecords

from formula.encoders import PrettyJSONEncoder


class DriverStatus(models.TextChoices):
    ACTIVE = "ACTIVE", _("Active")
    INACTIVE = "INACTIVE", _("Inactive")


class DriverCategory(models.TextChoices):
    ROOKIE = "ROOKIE", _("Rookie")
    EXPERIENCED = "EXPERIENCED", _("Experienced")
    VETERAN = "VETERAN", _("Veteran")
    CHAMPION = "CHAMPION", _("Champion")


class AuditedModel(models.Model):
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    modified_at = models.DateTimeField(_("modified at"), auto_now=True)

    class Meta:
        abstract = True


class Tag(AuditedModel):
    title = models.CharField(_("title"), max_length=255)
    slug = models.CharField(_("slug"), max_length=255)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, verbose_name=_("content type")
    )
    object_id = models.PositiveIntegerField(_("object id"))
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return self.tag

    class Meta:
        db_table = "tags"
        verbose_name = _("tag")
        verbose_name_plural = _("tags")
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]


class User(AbstractUser, AuditedModel):
    biography = models.TextField(_("biography"), null=True, blank=True, default=None)
    tags = GenericRelation(Tag)

    class Meta:
        db_table = "users"
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.email if self.email else self.username

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.last_name}, {self.first_name}"

        return None


class Profile(AuditedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(_("picture"), null=True, blank=True, default=None)
    resume = models.FileField(_("resume"), null=True, blank=True, default=None)
    link = models.URLField(_("link"), null=True, blank=True)
    data = models.JSONField(_("data"), null=True, blank=True)

    class Meta:
        db_table = "profiles"
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")


class Circuit(AuditedModel):
    name = models.CharField(_("name"), max_length=255)
    city = models.CharField(_("city"), max_length=255)
    country = models.CharField(_("country"), max_length=255)
    data = models.JSONField(_("data"), null=True, blank=True)

    class Meta:
        db_table = "circuits"
        verbose_name = _("circuit")
        verbose_name_plural = _("circuits")

    def __str__(self):
        return self.name


class Driver(AuditedModel):
    first_name = models.CharField(_("first name"), max_length=255)
    last_name = models.CharField(_("last name"), max_length=255)
    salary = MoneyField(
        max_digits=14, decimal_places=2, null=True, blank=True, default_currency=None
    )
    category = models.CharField(
        _("category"),
        choices=DriverCategory.choices,
        null=True,
        blank=True,
        max_length=255,
    )
    picture = models.ImageField(_("picture"), null=True, blank=True, default=None)
    born_at = models.DateField(_("born"), null=True, blank=True)
    last_race_at = models.DateField(_("last race"), null=True, blank=True)
    best_time = models.TimeField(_("best time"), null=True, blank=True)
    first_race_at = models.DateTimeField(_("first race"), null=True, blank=True)
    resume = models.FileField(_("resume"), null=True, blank=True, default=None)
    author = models.ForeignKey(
        "User",
        verbose_name=_("author"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    editor = models.ForeignKey(
        "User",
        verbose_name=_("editor"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="driver_editor",
    )
    standing = models.ForeignKey(
        "Standing",
        verbose_name=_("standing"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="standing",
    )
    constructors = models.ManyToManyField(
        "Constructor", verbose_name=_("constructors"), blank=True
    )
    code = models.CharField(_("code"), max_length=3)
    color = models.CharField(_("color"), null=True, blank=True, max_length=255)
    link = models.URLField(_("link"), null=True, blank=True)
    status = models.CharField(
        _("status"),
        choices=DriverStatus.choices,
        null=True,
        blank=True,
        max_length=255,
    )
    conditional_field_active = models.CharField(
        _("conditional field active"),
        null=True,
        blank=True,
        max_length=255,
        help_text="This field is only visible if the status is ACTIVE",
    )
    conditional_field_inactive = models.CharField(
        _("conditional field inactive"),
        null=True,
        blank=True,
        max_length=255,
        help_text="This field is only visible if the status is INACTIVE",
    )
    data = models.JSONField(_("data"), null=True, blank=True, encoder=PrettyJSONEncoder)
    history = HistoricalRecords()
    is_active = models.BooleanField(_("active"), default=False)
    is_retired = models.BooleanField(
        _("retired"),
        choices=(
            (None, ""),
            (True, _("Active")),
            (False, _("Inactive")),
        ),
        null=True,
    )
    is_hidden = models.BooleanField(_("hidden"), default=False)

    class Meta:
        db_table = "drivers"
        verbose_name = _("driver")
        verbose_name_plural = _("drivers")
        permissions = (("update_statistics", _("Update statistics")),)

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.last_name}, {self.first_name}"

        return None

    @property
    def initials(self):
        if self.first_name and self.last_name:
            return f"{self.first_name[0]}{self.last_name[0]}"

        return None


class DriverWithFilters(Driver):
    history = HistoricalRecords()

    class Meta:
        proxy = True


class Constructor(AuditedModel):
    name = models.CharField(_("name"), max_length=255)

    class Meta:
        db_table = "constructors"
        verbose_name = _("constructor")
        verbose_name_plural = _("constructors")

    def __str__(self):
        return self.name


class Race(AuditedModel):
    circuit = models.ForeignKey(
        Circuit, verbose_name=_("circuit"), on_delete=models.PROTECT
    )
    winner = models.ForeignKey(
        Driver, verbose_name=_("winner"), on_delete=models.PROTECT
    )
    picture = models.ImageField(_("picture"), null=True, blank=True, default=None)
    year = models.PositiveIntegerField(_("year"))
    laps = models.PositiveIntegerField(_("laps"))
    date = models.DateField(_("date"))
    weight = models.PositiveIntegerField(_("weight"), default=0, db_index=True)

    class Meta:
        db_table = "races"
        verbose_name = _("race")
        verbose_name_plural = _("races")
        ordering = ["weight"]

    def __str__(self):
        return f"{self.circuit.name}, {self.year}"


class Standing(AuditedModel):
    race = models.ForeignKey(Race, verbose_name=_("race"), on_delete=models.PROTECT)
    driver = models.ForeignKey(
        Driver,
        verbose_name=_("driver"),
        on_delete=models.PROTECT,
        related_name="standings",
    )
    constructor = models.ForeignKey(
        Constructor, verbose_name=_("constructor"), on_delete=models.PROTECT
    )
    position = models.PositiveIntegerField(_("position"))
    number = models.PositiveIntegerField(_("number"))
    laps = models.PositiveIntegerField(_("laps"))
    points = models.DecimalField(_("points"), decimal_places=2, max_digits=4)
    weight = models.PositiveIntegerField(_("weight"), default=0, db_index=True)

    class Meta:
        db_table = "standings"
        verbose_name = _("standing")
        verbose_name_plural = _("standings")
        ordering = ["weight"]

    def __str__(self):
        return f"{self.driver.full_name}, {self.position}"
