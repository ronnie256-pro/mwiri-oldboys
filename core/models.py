from django.db import models

class HeroSlider(models.Model):
    image = models.ImageField(upload_to='hero_slider/')
    hero_text = models.CharField(max_length=255)
    hero_description = models.TextField()

    def __str__(self):
        return self.hero_text

class Fixture(models.Model):
    cohort_1_image = models.ImageField(upload_to='fixture_images/')
    cohort_1_name = models.CharField(max_length=255)
    cohort_2_image = models.ImageField(upload_to='fixture_images/')
    cohort_2_name = models.CharField(max_length=255)
    date = models.DateTimeField()
    location = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.cohort_1_name} vs {self.cohort_2_name}'

class ManOfTheHour(models.Model):
    title = models.CharField(max_length=255)
    hero_image = models.ImageField(upload_to='man_of_the_hour/')
    youtube_link = models.URLField()

    def __str__(self):
        return self.title

class SiteSettings(models.Model):
    site_logo = models.ImageField(upload_to='brand/', blank=True, null=True)
    site_icon = models.ImageField(upload_to='brand/', blank=True, null=True)

    class Meta:
        verbose_name = 'Site Setting'
        verbose_name_plural = 'Site Settings'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Site Settings"
