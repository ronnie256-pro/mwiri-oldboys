from django.db import models

class Cohort(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class House(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Profession(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
