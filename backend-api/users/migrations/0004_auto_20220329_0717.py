# Generated by Django 3.2.12 on 2022-03-29 07:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20220329_0447'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='settings',
            name='id',
        ),
        migrations.AlterField(
            model_name='settings',
            name='user',
            field=models.OneToOneField(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='settings', related_query_name='settings', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
