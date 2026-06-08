from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ElectionCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Election Categories"

    def __str__(self):
        return self.name

class Position(models.Model):
    category = models.ForeignKey(ElectionCategory, on_delete=models.CASCADE, related_name='positions')
    title = models.CharField(max_length=255)
    description = models.TextField(help_text="Describe the tasks and roles for this position")

    def __str__(self):
        return f"{self.title} - {self.category.name}"

class Candidate(models.Model):
    STATUS_PENDING = 'PENDING'
    STATUS_APPROVED = 'APPROVED'
    STATUS_DENIED = 'DENIED'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_DENIED, 'Denied'),
    ]

    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='candidates')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='candidacies')
    manifesto = models.TextField(blank=True, null=True, help_text="Candidate's message or promises to the voters.")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} for {self.position.title}"
