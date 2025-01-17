# Generated by Django 5.1.3 on 2024-11-26 06:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounts',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='accounts.userregistrationmodel'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.userregistrationmodel'),
        ),
        migrations.AlterField(
            model_name='userregistrationmodel',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='custom_user_group', to='auth.group'),
        ),
        migrations.AlterField(
            model_name='userregistrationmodel',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, related_name='custom_user_permissions', to='auth.group'),
        ),
    ]
