# Generated by Django 5.1.3 on 2024-11-26 07:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0004_transactionhistory_created_at_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['-amount']},
        ),
    ]