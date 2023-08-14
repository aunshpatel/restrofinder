from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.
class Restaurant(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    opening_time = models.IntegerField()
    closing_time = models.IntegerField()
    description = models.TextField(max_length=250)

    def __str__(self):
        return f'{self.name} ({self.id})'
    
    def get_absolute_url(self):
        return reverse('index')