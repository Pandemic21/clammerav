from django.contrib import admin

from .models import Asset, RawLog, Task, Ingest

# Register your models here.
admin.site.register(Asset)
admin.site.register(RawLog)
admin.site.register(Task)
admin.site.register(Ingest)
