# Generated by Django 2.2 on 2020-08-12 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0012_auto_20200812_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepost',
            name='is_in_garbage',
            field=models.BooleanField(default=False),
        ),
    ]