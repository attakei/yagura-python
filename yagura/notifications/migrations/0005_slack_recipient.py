# Generated by Django 2.0.7 on 2018-08-06 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_site_ok_http_status'),
        ('notifications', '0004_rename_models'),
    ]

    operations = [
        migrations.CreateModel(
            name='SlackRecipient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(verbose_name='Webhook URL')),
                ('channel', models.CharField(blank=True, max_length=22, null=True, verbose_name='Channel name(optional)')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slack_recipients', to='sites.Site')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='slackrecipient',
            unique_together={('site', 'url', 'channel')},
        ),
    ]