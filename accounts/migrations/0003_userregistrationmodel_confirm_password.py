# Generated by Django 5.1.3 on 2024-11-26 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_accounts_user_alter_profile_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userregistrationmodel',
            name='confirm_password',
            field=models.CharField(blank=True, max_length=150, verbose_name='confirm_password'),
        ),
    ]