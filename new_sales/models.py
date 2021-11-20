from django.db import models
from django.conf import settings
# Create your models here.
User = settings.AUTH_USER_MODEL

class Report(models.Model):
	file=models.FileField()