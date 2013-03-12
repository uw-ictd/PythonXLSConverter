from django.db import models

class ConversionLogItem(models.Model):
    timestamp = models.DateField(auto_now=True)