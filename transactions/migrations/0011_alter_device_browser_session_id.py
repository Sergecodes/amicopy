# Generated by Django 3.2.12 on 2022-03-16 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0010_alter_session_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='browser_session_id',
            field=models.CharField(blank=True, max_length=80),
        ),
    ]
