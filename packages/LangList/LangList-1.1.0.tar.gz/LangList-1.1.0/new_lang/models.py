from django.db import models
import sys

print(sys.path)
# Create your models here.
class Lang_app(models.Model):
    name = models.CharField(max_length=100)
    