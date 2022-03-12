# Generated by Django 3.2.12 on 2022-03-12 13:49

import ckeditor.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import shortuuid.django_fields
import transactions.models.operations
import users.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField()),
                ('browser_session_id', models.CharField(blank=True, max_length=200)),
                ('display_name', models.CharField(help_text='Name used to identify you in this session, users in this session will be able to see this name.', max_length=50, validators=[users.validators.UsernameValidator()], verbose_name='display name')),
                ('deleted_on', models.DateTimeField(blank=True, editable=False, null=True)),
            ],
            options={
                'db_table': 'transactions"."device',
            },
            bases=(models.Model, transactions.models.operations.DeviceOperations),
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', shortuuid.django_fields.ShortUUIDField(alphabet=None, length=9, max_length=9, prefix='', verbose_name='session code')),
                ('title', models.CharField(help_text='Enter a name of at most 100 characters to identify this session', max_length=100, verbose_name='title')),
                ('creator_code', models.CharField(blank=True, help_text='Enter a code of at most 25 characters, other devices will need to enter this code to join the session', max_length=25, verbose_name='your code')),
                ('accepts_new_devices', models.BooleanField(default=True, verbose_name='accepts new devices')),
                ('last_transaction_on', models.DateTimeField(blank=True, editable=False, null=True)),
                ('started_on', models.DateTimeField(auto_now_add=True)),
                ('ended_on', models.DateTimeField(blank=True, editable=False, null=True)),
                ('expired_on', models.DateTimeField(blank=True, editable=False, null=True)),
            ],
            options={
                'db_table': 'transactions"."session',
            },
            bases=(models.Model, transactions.models.operations.SessionOperations),
        ),
        migrations.CreateModel(
            name='SessionDelete',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_on', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'transactions"."session_delete',
            },
        ),
        migrations.CreateModel(
            name='SessionDevices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joined_on', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'transactions"."session_with_devices',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, help_text='Enter a name of at most 100 characters to identify this transaction', max_length=100, verbose_name='title')),
                ('text_content', ckeditor.fields.RichTextField(blank=True, help_text='Enter the text to share', verbose_name='text')),
                ('files_archive', models.FileField(upload_to='', validators=[django.core.validators.FileExtensionValidator(['zip'])])),
                ('shared_on', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'transactions"."transaction',
            },
            bases=(models.Model, transactions.models.operations.TransactionOperations),
        ),
        migrations.CreateModel(
            name='TransactionBookmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookmarked_on', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'transactions"."transaction_bookmark',
            },
        ),
        migrations.CreateModel(
            name='TransactionToDevices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device', models.ForeignKey(db_column='device_id', on_delete=django.db.models.deletion.RESTRICT, related_name='+', to='transactions.device')),
                ('transaction', models.ForeignKey(db_column='transaction_id', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='transactions.transaction')),
            ],
            options={
                'db_table': 'transactions"."transaction_to_devices',
            },
        ),
        migrations.CreateModel(
            name='TransactionDelete',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_on', models.DateTimeField(auto_now_add=True)),
                ('transaction', models.ForeignKey(db_column='transaction_id', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='transactions.transaction')),
            ],
            options={
                'db_table': 'transactions"."transaction_delete',
            },
        ),
    ]
