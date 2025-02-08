from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("formula", "0017_alter_race_options_standing_weight"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="standing",
            options={
                "ordering": ["weight"],
                "verbose_name": "standing",
                "verbose_name_plural": "standings",
            },
        ),
        migrations.AddField(
            model_name="driver",
            name="is_active",
            field=models.BooleanField(default=False, verbose_name="active"),
        ),
        migrations.AddField(
            model_name="driver",
            name="is_hidden",
            field=models.BooleanField(default=False, verbose_name="hidden"),
        ),
        migrations.AddField(
            model_name="historicaldriver",
            name="is_active",
            field=models.BooleanField(default=False, verbose_name="active"),
        ),
        migrations.AddField(
            model_name="historicaldriver",
            name="is_hidden",
            field=models.BooleanField(default=False, verbose_name="hidden"),
        ),
    ]
