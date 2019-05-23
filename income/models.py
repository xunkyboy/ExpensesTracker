from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class Income(models.Model):
    title=models.CharField(max_length=30)
    description=models.TextField(null=True, blank=True)
    date = models.DateField(default=timezone.now)
    rupees = models.FloatField(null=True)
    user= models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title