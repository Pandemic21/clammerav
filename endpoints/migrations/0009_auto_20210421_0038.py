# Generated by Django 3.2 on 2021-04-21 00:38

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('endpoints', '0008_ingest_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingest',
            name='id',
            field=models.UUIDField(default=uuid.UUID('90bea12f-e082-4970-b64c-f22f06b467af'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='ingest',
            name='url',
            field=models.URLField(default='http://127.0.0.1:8000/endpoints/ingest/90bea12f-e082-4970-b64c-f22f06b467af/join', editable=False, max_length=500),
        ),
    ]