# Generated by Django 3.2 on 2021-04-20 00:12

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Endpoints',
            fields=[
                ('endpoint_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('hostname', models.CharField(max_length=100, null=True)),
                ('ext_ipv4', models.GenericIPAddressField(null=True, protocol='ipv4')),
                ('int_ipv4', models.GenericIPAddressField(null=True, protocol='ipv4')),
                ('ext_ipv6', models.GenericIPAddressField(null=True, protocol='ipv6')),
                ('int_ipv6', models.GenericIPAddressField(null=True, protocol='ipv6')),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('last_heartbeat', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='RawLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('endpoint_id', models.UUIDField()),
                ('date_received', models.DateField(auto_now=True)),
                ('log_data', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('endpoint_id', models.UUIDField()),
                ('date_issued', models.DateField(auto_now=True)),
                ('dated_complmeted', models.DateField(null=True)),
                ('task', models.CharField(max_length=100)),
            ],
        ),
    ]
