from django.db import models

# Create your models here.
class Person(models.Model):
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    company_name=models.CharField(max_length=200)
    Email_id=models.CharField(max_length=200)
    phone_number=models.CharField(max_length=10)                        
    subject_name=models.CharField(max_length=100)
    password=models.CharField(max_length=500,blank=True, null=True)
    address=models.TextField()
    is_active=models.BooleanField(default=True)
    