from django.db import models

class LegacyPhoto(models.Model):
    image = models.ImageField(upload_to='legacy_photos/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.caption or "Legacy Photo"
