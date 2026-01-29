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

class DidYouKnow(models.Model):
    date_of_event = models.DateField()
    description_of_event = models.TextField()

    def __str__(self):
        return self.description_of_event[:50]
