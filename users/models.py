
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        PUBLIC = "PUBLIC", "Public"
        SUBSCRIBER = "SUBSCRIBER", "Subscriber"
        ADMIN = "ADMIN", "Admin"

    base_role = Role.PUBLIC
    role = models.CharField(max_length=50, choices=Role.choices, default=base_role)
    cohort = models.ForeignKey('organisation.Cohort', on_delete=models.SET_NULL, null=True, blank=True)
    house = models.ForeignKey('organisation.House', on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    linkedin_profile = models.URLField(blank=True)
    website = models.URLField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    profession = models.ForeignKey('organisation.Profession', on_delete=models.SET_NULL, null=True, blank=True)
    whatsapp_contact = models.CharField(max_length=20, blank=True)
    biography = models.TextField(max_length=150, blank=True)
    side_hustle = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
        return super().save(*args, **kwargs)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)

    def __str__(self):
        return self.user.username
