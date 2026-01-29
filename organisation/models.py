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

class Committee(models.Model):
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    cohort = models.ForeignKey(Cohort, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='committee/', blank=True, null=True)

    def __str__(self):
        return self.name
