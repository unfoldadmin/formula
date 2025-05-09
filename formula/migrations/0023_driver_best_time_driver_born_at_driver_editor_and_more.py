import django.db.models.deletion
import djmoney.models.fields
import formula.encoders
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formula', '0022_driverwithfilters_driver_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='best_time',
            field=models.TimeField(blank=True, null=True, verbose_name='best time'),
        ),
        migrations.AddField(
            model_name='driver',
            name='born_at',
            field=models.DateField(blank=True, null=True, verbose_name='born'),
        ),
        migrations.AddField(
            model_name='driver',
            name='editor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='driver_editor', to=settings.AUTH_USER_MODEL, verbose_name='editor'),
        ),
        migrations.AddField(
            model_name='driver',
            name='first_race_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='first race'),
        ),
        migrations.AddField(
            model_name='driver',
            name='last_race_at',
            field=models.DateField(blank=True, null=True, verbose_name='last race'),
        ),
        migrations.AddField(
            model_name='historicaldriver',
            name='best_time',
            field=models.TimeField(blank=True, null=True, verbose_name='best time'),
        ),
        migrations.AddField(
            model_name='historicaldriver',
            name='born_at',
            field=models.DateField(blank=True, null=True, verbose_name='born'),
        ),
        migrations.AddField(
            model_name='historicaldriver',
            name='editor',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='editor'),
        ),
        migrations.AddField(
            model_name='historicaldriver',
            name='first_race_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='first race'),
        ),
        migrations.AddField(
            model_name='historicaldriver',
            name='last_race_at',
            field=models.DateField(blank=True, null=True, verbose_name='last race'),
        ),
        migrations.CreateModel(
            name='HistoricalDriverWithFilters',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='created at')),
                ('modified_at', models.DateTimeField(blank=True, editable=False, verbose_name='modified at')),
                ('first_name', models.CharField(max_length=255, verbose_name='first name')),
                ('last_name', models.CharField(max_length=255, verbose_name='last name')),
                ('salary_currency', djmoney.models.fields.CurrencyField(choices=[('EUR', 'Euro'), ('USD', 'US Dollar')], default=None, editable=False, max_length=3, null=True)),
                ('salary', djmoney.models.fields.MoneyField(blank=True, decimal_places=2, max_digits=14, null=True)),
                ('category', models.CharField(blank=True, choices=[('ROOKIE', 'Rookie'), ('EXPERIENCED', 'Experienced'), ('VETERAN', 'Veteran'), ('CHAMPION', 'Champion')], max_length=255, null=True, verbose_name='category')),
                ('picture', models.TextField(blank=True, default=None, max_length=100, null=True, verbose_name='picture')),
                ('born_at', models.DateField(blank=True, null=True, verbose_name='born')),
                ('last_race_at', models.DateField(blank=True, null=True, verbose_name='last race')),
                ('best_time', models.TimeField(blank=True, null=True, verbose_name='best time')),
                ('first_race_at', models.DateTimeField(blank=True, null=True, verbose_name='first race')),
                ('resume', models.TextField(blank=True, default=None, max_length=100, null=True, verbose_name='resume')),
                ('code', models.CharField(max_length=3, verbose_name='code')),
                ('color', models.CharField(blank=True, max_length=255, null=True, verbose_name='color')),
                ('link', models.URLField(blank=True, null=True, verbose_name='link')),
                ('status', models.CharField(blank=True, choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive')], max_length=255, null=True, verbose_name='status')),
                ('conditional_field_active', models.CharField(blank=True, help_text='This field is only visible if the status is ACTIVE', max_length=255, null=True, verbose_name='conditional field active')),
                ('conditional_field_inactive', models.CharField(blank=True, help_text='This field is only visible if the status is INACTIVE', max_length=255, null=True, verbose_name='conditional field inactive')),
                ('data', models.JSONField(blank=True, encoder=formula.encoders.PrettyJSONEncoder, null=True, verbose_name='data')),
                ('is_active', models.BooleanField(default=False, verbose_name='active')),
                ('is_hidden', models.BooleanField(default=False, verbose_name='hidden')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('author', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('editor', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='editor')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical driver with filters',
                'verbose_name_plural': 'historical driver with filterss',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
