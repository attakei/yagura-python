# Generated by Django 2.0.7 on 2018-08-02 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='ok_status_code',
            field=models.PositiveSmallIntegerField(default=200, verbose_name='Excepted HTTP status code'),
        ),
    ]