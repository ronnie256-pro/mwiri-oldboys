from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class SOSRequest(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
