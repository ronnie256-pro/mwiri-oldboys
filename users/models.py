
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
    x_account = models.URLField(blank=True)
    tiktok_account = models.URLField(blank=True)
    youtube_account = models.URLField(blank=True)
    facebook_account = models.URLField(blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
        return super().save(*args, **kwargs)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    years_at_mwiri_from = models.PositiveIntegerField(null=True, blank=True)
    years_at_mwiri_to = models.PositiveIntegerField(null=True, blank=True)
    s4_year = models.PositiveIntegerField(null=True, blank=True)
    s6_year = models.PositiveIntegerField(null=True, blank=True)
    nickname = models.CharField(max_length=100, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class SideHustle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='side_hustles')
    title = models.CharField(max_length=255)
    details = models.TextField(help_text="Maximum 50 words.", max_length=500)
    address = models.CharField(max_length=255)
    image_1 = models.ImageField(upload_to='side_hustles/', blank=True, null=True)
    image_2 = models.ImageField(upload_to='side_hustles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"
