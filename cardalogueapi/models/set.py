from django.db import models

class Set(models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=50)
    year = models.CharField(max_length=50, default="0000")
