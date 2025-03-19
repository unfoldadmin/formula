from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formula', '0020_race_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='conditional_field_active',
            field=models.CharField(blank=True, help_text='This field is only visible if the status is ACTIVE', max_length=255, null=True, verbose_name='conditional field active'),
        ),
        migrations.AddField(
            model_name='driver',
            name='conditional_field_inactive',
            field=models.CharField(blank=True, help_text='This field is only visible if the status is INACTIVE', max_length=255, null=True, verbose_name='conditional field inactive'),
        ),
        migrations.AddField(
            model_name='historicaldriver',
            name='conditional_field_active',
            field=models.CharField(blank=True, help_text='This field is only visible if the status is ACTIVE', max_length=255, null=True, verbose_name='conditional field active'),
        ),
        migrations.AddField(
            model_name='historicaldriver',
            name='conditional_field_inactive',
            field=models.CharField(blank=True, help_text='This field is only visible if the status is INACTIVE', max_length=255, null=True, verbose_name='conditional field inactive'),
        ),
    ]
