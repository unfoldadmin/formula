from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("formula", "0012_driver_resume_historicaldriver_resume"),
    ]

    operations = [
        migrations.AddField(
            model_name="driver",
            name="link",
            field=models.URLField(blank=True, null=True, verbose_name="link"),
        ),
        migrations.AddField(
            model_name="historicaldriver",
            name="link",
            field=models.URLField(blank=True, null=True, verbose_name="link"),
        ),
    ]
