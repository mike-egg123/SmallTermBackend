# Generated by Django 2.2 on 2020-08-11 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='userid',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
