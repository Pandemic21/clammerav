import uuid

from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns

# Create your models here.
class Asset(models.Model):
    asset_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    hostname = models.CharField(max_length=100, blank=True, null=True)
    ext_ipv4 = models.GenericIPAddressField(protocol='ipv4', blank=True, null=True)
    int_ipv4 = models.GenericIPAddressField(protocol='ipv4', blank=True, null=True)
    ext_ipv6 = models.GenericIPAddressField(protocol='ipv6', blank=True, null=True)
    int_ipv6 = models.GenericIPAddressField(protocol='ipv6', blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_heartbeat = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String for representing the Model object."""
        return str(self.asset_id)

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('asset-detail', args=[str(self.asset_id)])


class RawLog(models.Model):
    class Meta:
        ordering = ['-id']

    asset_id = models.ForeignKey('Asset', on_delete=models.RESTRICT, null=True)
    # name of the log (e.g. freshclam, clamav...)
    log_name = models.CharField(max_length=500, blank=True, null=True)
    # path to the log on the endpoint
    log_path = models.CharField(max_length=500, blank=True, null=True)
    date_received = models.DateTimeField(auto_now=True)
    log_data = models.CharField(max_length=500)

    def __str__(self):
        """String for representing the Model object."""
        return self.log_data

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('rawlog-detail', args=[str(self.id)])


class Task(models.Model):
    asset_id = models.ForeignKey('Asset', on_delete=models.RESTRICT, null=True)
    date_issued = models.DateTimeField(auto_now=True)
    dated_complmeted = models.DateTimeField(blank=True, null=True)
    task = models.CharField(max_length=100)


class Ingest(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    # TODO: un-hard code the default for url
    active = models.BooleanField(default=True)
    existing_clamav = models.BooleanField(default=False) # is there an existing ClamAV install?
    date_created = models.DateTimeField(auto_now_add=True)
    url = models.URLField(max_length=500, default="http://127.0.0.1:8000/endpoints/ingest/" + str(id) + "/join", editable=False)
    login_url = models.URLField(max_length=500, default="http://127.0.0.1:8000/accounts/login/")
    logout_url = models.URLField(max_length=500, default="http://127.0.0.1:8000/accounts/logout/")
    rawlog_url = models.URLField(max_length=500, default="http://127.0.0.1:8000/endpoints/assets/")

    log_level_choies = [
        ('CRITICAL', 'CRITICAL'),
        ('ERROR', 'ERROR'),
        ('WARNING', 'WARNING'),
        ('INFO', 'INFO'),
        ('DEBUG', 'DEBUG')
    ]

    log_level = models.CharField(choices=log_level_choies, max_length=10, default='DEBUG')

    # ClamAV files
    log_files = models.CharField(max_length=500, blank=True, null=True, \
        help_text="Enter ClamAV log files to monitor separated by commas. \
        For example, /var/log/clam.log,/var/log/freshclam.log") # ClamAV log files to monitor
    config_files = models.CharField(max_length=500, blank=True, null=True, \
        help_text="Enter ClamAV log files to monitor separated by commas. \
        For example, /var/log/clam.log,/var/log/freshclam.log") # ClamAV config files to manage

    # agent info
    home = models.CharField(max_length=100, default="/opt/clammer")

    # this overrides the save function to allow us to use the id it already generated
    def save(self, *args, **kwargs):
        self.url = "http://127.0.0.1:8000/endpoints/ingest/" + str(self.id) + "/join"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('ingest-detail', args=[str(self.id)])
