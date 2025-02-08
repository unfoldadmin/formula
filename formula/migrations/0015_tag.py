import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("formula", "0014_driver_author_historicaldriver_author"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="title")),
                ("slug", models.CharField(max_length=255, verbose_name="slug")),
                ("object_id", models.PositiveIntegerField(verbose_name="object id")),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                        verbose_name="content type",
                    ),
                ),
            ],
            options={
                "verbose_name": "tag",
                "verbose_name_plural": "tags",
                "db_table": "tags",
                "indexes": [
                    models.Index(
                        fields=["content_type", "object_id"],
                        name="tags_content_609291_idx",
                    )
                ],
            },
        ),
    ]
