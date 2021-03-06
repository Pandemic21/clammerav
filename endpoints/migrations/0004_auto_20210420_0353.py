# Generated by Django 3.2 on 2021-04-20 03:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('endpoints', '0003_auto_20210420_0318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawlog',
            name='endpoint_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='endpoints.endpoint'),
        ),
        migrations.AlterField(
            model_name='task',
            name='endpoint_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='endpoints.endpoint'),
        ),
    ]
