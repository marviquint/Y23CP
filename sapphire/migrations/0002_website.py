# Generated by Django 4.2 on 2023-04-19 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sapphire', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ctrl_num', models.IntegerField()),
                ('rule_set', models.CharField(max_length=255)),
                ('content_class', models.CharField(max_length=255)),
                ('doc_type', models.CharField(max_length=255)),
                ('al_name', models.CharField(max_length=255)),
                ('src_url', models.CharField(max_length=255)),
                ('freq_updates', models.CharField(max_length=255)),
                ('freq_crawl', models.CharField(max_length=255)),
                ('prio_comm', models.CharField(max_length=255)),
            ],
        ),
    ]
