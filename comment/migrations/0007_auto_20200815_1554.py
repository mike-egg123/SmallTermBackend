# Generated by Django 2.2 on 2020-08-15 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0006_auto_20200815_1548'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['created']},
        ),
    ]
