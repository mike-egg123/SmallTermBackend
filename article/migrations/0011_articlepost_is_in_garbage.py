# Generated by Django 2.2 on 2020-08-12 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0010_auto_20200811_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepost',
            name='is_in_garbage',
            field=models.IntegerField(default=0),
        ),
    ]