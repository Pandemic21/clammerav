# Generated by Django 3.2 on 2021-04-25 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('endpoints', '0016_auto_20210423_0448'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawlog',
            name='log_name',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='rawlog',
            name='log_path',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='last_heartbeat',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='ingest',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='rawlog',
            name='date_received',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='date_issued',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='dated_complmeted',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]