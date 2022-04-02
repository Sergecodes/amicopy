# Generated by Django 3.2.12 on 2022-03-12 13:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('transactions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='transactiondelete',
            name='user',
            field=models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='transactionbookmark',
            name='bookmarker',
            field=models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='transactionbookmark',
            name='transaction',
            field=models.ForeignKey(db_column='transaction_id', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='transactions.transaction'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='deleted_by',
            field=models.ManyToManyField(related_name='deleted_transactions', related_query_name='deleted_transaction', through='transactions.TransactionDelete', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='transaction',
            name='from_device',
            field=models.ForeignKey(db_column='from_device_id', on_delete=django.db.models.deletion.RESTRICT, related_name='sent_transactions', related_query_name='sent_transaction', to='transactions.device'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='session',
            field=models.ForeignKey(db_column='session_id', on_delete=django.db.models.deletion.CASCADE, related_name='transactions', related_query_name='transaction', to='transactions.session'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='to_devices',
            field=models.ManyToManyField(related_name='received_transactions', related_query_name='received_transaction', through='transactions.TransactionToDevices', to='transactions.Device'),
        ),
        migrations.AddField(
            model_name='sessiondevices',
            name='device',
            field=models.ForeignKey(db_column='device_id', on_delete=django.db.models.deletion.RESTRICT, related_name='+', to='transactions.device'),
        ),
        migrations.AddField(
            model_name='sessiondevices',
            name='session',
            field=models.ForeignKey(db_column='session_id', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='transactions.session'),
        ),
        migrations.AddField(
            model_name='sessiondelete',
            name='session',
            field=models.ForeignKey(db_column='session_id', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='transactions.session'),
        ),
        migrations.AddField(
            model_name='sessiondelete',
            name='user',
            field=models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='session',
            name='all_devices',
            field=models.ManyToManyField(related_name='sessions', related_query_name='session', through='transactions.SessionDevices', to='transactions.Device'),
        ),
        migrations.AddField(
            model_name='session',
            name='creator_device',
            field=models.ForeignKey(db_column='creator_device_id', on_delete=django.db.models.deletion.RESTRICT, related_name='created_sessions', related_query_name='created_session', to='transactions.device'),
        ),
        migrations.AddField(
            model_name='session',
            name='deleted_by',
            field=models.ManyToManyField(related_name='deleted_sessions', related_query_name='deleted_session', through='transactions.SessionDelete', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='device',
            name='user',
            field=models.ForeignKey(blank=True, db_column='user_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='devices', related_query_name='device', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='transactionbookmark',
            constraint=models.UniqueConstraint(fields=('transaction', 'bookmarker'), name='unique_transaction_bookmark'),
        ),
        migrations.AddIndex(
            model_name='session',
            index=models.Index(fields=['title'], name='session_title_idx'),
        ),
        migrations.AddConstraint(
            model_name='session',
            constraint=models.UniqueConstraint(fields=('uuid',), name='unique_session_uuid'),
        ),
    ]