from django.contrib.auth.models import AbstractUser
from django.db import models

#user model. Give superuser status to librarian, not so for students
class CustomUser(AbstractUser):
    # libid=models.AutoField(primary_key=True) # using default pk for now. 
    
    regno=models.IntegerField(null=True, blank=True)
    branch=models.CharField(max_length=255 , null=True, default=None , blank=True)
    section=models.CharField(max_length=2 , null=True, default=None , blank=True)
    semester=models.CharField(max_length=255 , null=True, default=None , blank=True)
    yearofadm=models.CharField(max_length=5 , null=True, default=None , blank=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    def __str__(self):
        return (self.username)
