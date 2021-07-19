from django.contrib.auth.models import AbstractUser
#from django.utils.translation import gettext as _
from django.db import models

#user model. Give superuser status to librarian, not so for students
class CustomUser(AbstractUser):
    # libid=models.AutoField(primary_key=True) # using default pk for now. 

#   username = None
#   email = models.EmailField(_('email address'), unique=True)
#   USERNAME_FIELD = 'email'
    regno=models.IntegerField(null=True, blank=True)
    branch=models.CharField(max_length=255 , null=True, default=None , blank=True)
    section=models.CharField(max_length=2 , null=True, default=None , blank=True)
    semester=models.CharField(max_length=255 , null=True, default=None , blank=True)
    yearofadm=models.CharField(max_length=5 , null=True, default=None , blank=True)

    def __str__(self):
        return (self.username)
