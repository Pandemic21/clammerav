import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

# Sends raw logs from asset
class FormAssetSendRawLog(forms.Form):
    log_data = forms.CharField()

# Creates a new asset
class FormCreateNewAsset(forms.Form):
    hostname = forms.CharField()
    ext_ipv4 = forms.GenericIPAddressField(protocol='ipv4')
    int_ipv4 = forms.GenericIPAddressField(protocol='ipv4')
    ext_ipv6 = forms.GenericIPAddressField(protocol='ipv6')
    int_ipv6 = forms.GenericIPAddressField(protocol='ipv6')
