# Generated by Django 5.0.1 on 2024-02-03 12:19

import apps.core.db.custom_db_functions
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(db_index=True, max_length=255, unique=True)),
                ('username', models.CharField(blank=True, max_length=30, null=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/', verbose_name='Avatar')),
                ('first_name', models.CharField(max_length=24, null=True, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=24, null=True, verbose_name='Last Name')),
                ('full_name', models.GeneratedField(db_persist=True, expression=apps.core.db.custom_db_functions.ConcatOp('first_name', models.Value(' '), 'last_name'), output_field=models.CharField(max_length=511), verbose_name='Full Name')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('user', 'User')], default='user', max_length=256, verbose_name='Role')),
                ('date_joined', models.DateField(auto_now_add=True, db_index=True, verbose_name='Date Joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'indexes': [models.Index(fields=['email'], name='user_user_email_5f6a77_idx'), models.Index(fields=['date_joined'], name='user_user_date_jo_e21b8f_idx')],
            },
        ),
    ]
