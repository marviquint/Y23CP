# Generated by Django 4.2 on 2023-04-06 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sapphire', '0005_remove_user_email_otp_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='temporary_password',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]