# Generated by Django 2.0.6 on 2018-06-28 14:29

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(choices=[('OK', 'OK'), ('NG', 'NG')], max_length=10, verbose_name='State label')),
                ('begin_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_at', models.DateTimeField(null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='states', to='sites.Site')),
            ],
            options={
                'ordering': ['begin_at'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='sitestate',
            unique_together={('site', 'begin_at')},
        ),
    ]
