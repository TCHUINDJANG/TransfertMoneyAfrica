# Generated by Django 5.1.3 on 2024-11-26 08:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_alter_transaction_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transactionhistory',
            options={'ordering': ['-sender']},
        ),
        migrations.RenameField(
            model_name='transactionhistory',
            old_name='receiver_account_id',
            new_name='receiver',
        ),
        migrations.RenameField(
            model_name='transactionhistory',
            old_name='sender_account_id',
            new_name='sender',
        ),
    ]
