# Generated by Django 3.2.12 on 2022-04-02 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0015_auto_20220331_0421'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='device',
            name='browser_session_key_and_user_id_not_both_unset',
        ),
        migrations.AddConstraint(
            model_name='device',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('browser_session_key', ''), _negated=True), ('user__isnull', False), _connector='OR'), name='browser_session_key_and_user_id_not_both_unset'),
        ),
    ]