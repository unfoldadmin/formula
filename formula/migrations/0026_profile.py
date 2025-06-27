import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formula', '0025_driver_is_retired_historicaldriver_is_retired_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified at')),
                ('picture', models.ImageField(blank=True, default=None, null=True, upload_to='', verbose_name='picture')),
                ('resume', models.FileField(blank=True, default=None, null=True, upload_to='', verbose_name='resume')),
                ('link', models.URLField(blank=True, null=True, verbose_name='link')),
                ('data', models.JSONField(blank=True, null=True, verbose_name='data')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'profile',
                'verbose_name_plural': 'profiles',
                'db_table': 'profiles',
            },
        ),
    ]
