# Generated by Django 2.0.7 on 2018-07-14 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_activation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deactivation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.UUIDField()),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notifications.Recipient')),
            ],
        ),
    ]
