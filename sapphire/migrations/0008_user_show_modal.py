# Generated by Django 4.2 on 2023-04-07 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sapphire', '0007_remove_user_temporary_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='show_modal',
            field=models.BooleanField(default=False),
        ),
    ]