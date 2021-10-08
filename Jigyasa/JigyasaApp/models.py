from django.db import models

# Create your models here.

class contact(models.Model):
    name = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.CharField(max_length=5000)