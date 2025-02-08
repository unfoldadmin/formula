from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("formula", "0015_tag"),
    ]

    operations = [
        migrations.AddField(
            model_name="race",
            name="weight",
            field=models.PositiveIntegerField(
                db_index=True, default=0, verbose_name="weight"
            ),
        ),
    ]
