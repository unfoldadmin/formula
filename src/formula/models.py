from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
from simple_history.models import HistoricalRecords

from formula.encoders import PrettyJSONEncoder


class User(AbstractUser):
    biography = models.TextField(_("biography"), null=True, blank=True, default=None)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    modified_at = models.DateTimeField(_("modified at"), auto_now=True)

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


class Circuit(models.Model):
    name = models.CharField(_("name"), max_length=255)
    city = models.CharField(_("city"), max_length=255)
    country = models.CharField(_("country"), max_length=255)

    class Meta:
        db_table = "circuits"
        verbose_name = _("circuit")
        verbose_name_plural = _("circuits")

    def __str__(self):
        return self.name


class DriverStatus(models.TextChoices):
    ACTIVE = "ACTIVE", _("Active")
    INACTIVE = "INACTIVE", _("Inactive")


class Driver(models.Model):
    first_name = models.CharField(_("first name"), max_length=255)
    last_name = models.CharField(_("last name"), max_length=255)
    picture = models.ImageField(_("picture"), null=True, blank=True, default=None)
    code = models.CharField(_("code"), max_length=3)
    color = models.CharField(_("color"), null=True, blank=True, max_length=255)
    salary = MoneyField(
        max_digits=14, decimal_places=2, null=True, blank=True, default_currency=None
    )
    status = models.CharField(
        _("status"), choices=DriverStatus.choices, null=True, blank=True, max_length=255
    )
    constructors = models.ManyToManyField(
        "Constructor", verbose_name=_("constructors"), blank=True
    )
    data = models.JSONField(_("data"), null=True, blank=True, encoder=PrettyJSONEncoder)
    objects = HistoricalRecords()

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


class Constructor(models.Model):
    name = models.CharField(_("name"), max_length=255)

    class Meta:
        db_table = "constructors"
        verbose_name = _("constructor")
        verbose_name_plural = _("constructors")

    def __str__(self):
        return self.name


class Race(models.Model):
    circuit = models.ForeignKey(
        Circuit, verbose_name=_("circuit"), on_delete=models.PROTECT
    )
    winner = models.ForeignKey(
        Driver, verbose_name=_("winner"), on_delete=models.PROTECT
    )
    year = models.PositiveIntegerField(_("year"))
    laps = models.PositiveIntegerField(_("laps"))
    date = models.DateField(_("date"))

    class Meta:
        db_table = "races"
        verbose_name = _("race")
        verbose_name_plural = _("races")

    def __str__(self):
        return f"{self.circuit.name}, {self.year}"


class Standing(models.Model):
    race = models.ForeignKey(Race, verbose_name=_("race"), on_delete=models.PROTECT)
    driver = models.ForeignKey(
        Driver, verbose_name=_("driver"), on_delete=models.PROTECT
    )
    constructor = models.ForeignKey(
        Constructor, verbose_name=_("constructor"), on_delete=models.PROTECT
    )
    position = models.PositiveIntegerField(_("position"))
    number = models.PositiveIntegerField(_("number"))
    laps = models.PositiveIntegerField(_("laps"))
    points = models.DecimalField(_("points"), decimal_places=2, max_digits=4)

    class Meta:
        db_table = "standings"
        verbose_name = _("standing")
        verbose_name_plural = _("standings")

    def __str__(self):
        return f"{self.driver.full_name}, {self.position}"
