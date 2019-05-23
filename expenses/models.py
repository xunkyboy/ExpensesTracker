from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from category.models import Category
# Create your models here.
class Expenses(models.Model):
    title=models.CharField(max_length=30)
    description=models.TextField(null=True, blank=True)
    bill = models.FileField(upload_to ='bill/',blank=True,null=True)
    date = models.DateField(default=timezone.now)
    rupees = models.FloatField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    user= models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title