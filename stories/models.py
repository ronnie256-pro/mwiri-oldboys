from django.db import models
from django.conf import settings


class Story(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='stories')
    title = models.CharField(max_length=255)
    content = models.TextField()
    hero_image = models.ImageField(upload_to='stories/')
    additional_image_1 = models.ImageField(upload_to='stories/', blank=True, null=True)
    additional_image_2 = models.ImageField(upload_to='stories/', blank=True, null=True)
    additional_image_3 = models.ImageField(upload_to='stories/', blank=True, null=True)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.author}"