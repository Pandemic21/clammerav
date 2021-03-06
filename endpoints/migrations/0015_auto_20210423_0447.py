# Generated by Django 3.2 on 2021-04-23 04:47

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('endpoints', '0014_auto_20210423_0424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingest',
            name='id',
            field=models.UUIDField(default=uuid.UUID('c9ce826d-22d3-4aa2-b59c-e7a933a25b47'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='ingest',
            name='url',
            field=models.URLField(default='http://127.0.0.1:8000/endpoints/ingest/c9ce826d-22d3-4aa2-b59c-e7a933a25b47/join', editable=False, max_length=500),
        ),
    ]
