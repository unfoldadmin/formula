from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("formula", "0002_driver_salary"),
    ]

    operations = [
        migrations.AddField(
            model_name="driver",
            name="constructors",
            field=models.ManyToManyField(
                blank=True, to="formula.constructor", verbose_name="constructors"
            ),
        ),
    ]
