# Generated by Django 2.2 on 2020-08-13 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0015_articlepost_permission'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepost',
            name='is_updating',
            field=models.IntegerField(default=0),
        ),
    ]
