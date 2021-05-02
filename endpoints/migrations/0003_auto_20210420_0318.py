# Generated by Django 3.2 on 2021-04-20 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('endpoints', '0002_auto_20210420_0316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='endpoint',
            name='ext_ipv4',
            field=models.GenericIPAddressField(blank=True, null=True, protocol='ipv4'),
        ),
        migrations.AlterField(
            model_name='endpoint',
            name='ext_ipv6',
            field=models.GenericIPAddressField(blank=True, null=True, protocol='ipv6'),
        ),
        migrations.AlterField(
            model_name='endpoint',
            name='hostname',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='endpoint',
            name='int_ipv4',
            field=models.GenericIPAddressField(blank=True, null=True, protocol='ipv4'),
        ),
        migrations.AlterField(
            model_name='endpoint',
            name='int_ipv6',
            field=models.GenericIPAddressField(blank=True, null=True, protocol='ipv6'),
        ),
        migrations.AlterField(
            model_name='task',
            name='dated_complmeted',
            field=models.DateField(blank=True, null=True),
        ),
    ]
