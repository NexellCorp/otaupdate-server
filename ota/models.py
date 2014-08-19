from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from util import hex_validator


# Create your models here.
class Rom(models.Model):
    device = models.CharField(max_length=16)
    name = models.CharField(max_length=32)
    ota_id = models.CharField(max_length=32)
    download_url = models.URLField()
    md5sum = models.CharField(max_length=64,
                              validators=[hex_validator()])
    version = models.IntegerField()
    date = models.DateTimeField()
    change_log = models.TextField()
    user = models.ForeignKey(User)

    class Meta:
        ordering = ('device', 'date',)


class RomAdmin(admin.ModelAdmin):
    list_display = \
        ('device', 'name', 'ota_id', 'download_url', 'version', 'date')

admin.site.register(Rom, RomAdmin)
