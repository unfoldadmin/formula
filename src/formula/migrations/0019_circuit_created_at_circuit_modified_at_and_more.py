import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("formula", "0018_alter_standing_options_driver_is_active_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="circuit",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="created at",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="circuit",
            name="modified_at",
            field=models.DateTimeField(auto_now=True, verbose_name="modified at"),
        ),
        migrations.AddField(
            model_name="constructor",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="created at",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="constructor",
            name="modified_at",
            field=models.DateTimeField(auto_now=True, verbose_name="modified at"),
        ),
        migrations.AddField(
            model_name="driver",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="created at",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="driver",
            name="modified_at",
            field=models.DateTimeField(auto_now=True, verbose_name="modified at"),
        ),
        migrations.AddField(
            model_name="historicaldriver",
            name="created_at",
            field=models.DateTimeField(
                blank=True,
                default=django.utils.timezone.now,
                editable=False,
                verbose_name="created at",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="historicaldriver",
            name="modified_at",
            field=models.DateTimeField(
                blank=True,
                default=django.utils.timezone.now,
                editable=False,
                verbose_name="modified at",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="race",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="created at",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="race",
            name="modified_at",
            field=models.DateTimeField(auto_now=True, verbose_name="modified at"),
        ),
        migrations.AddField(
            model_name="standing",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="created at",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="standing",
            name="modified_at",
            field=models.DateTimeField(auto_now=True, verbose_name="modified at"),
        ),
        migrations.AddField(
            model_name="tag",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="created at",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="tag",
            name="modified_at",
            field=models.DateTimeField(auto_now=True, verbose_name="modified at"),
        ),
    ]
