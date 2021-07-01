from django.db import models
from django.db.models.deletion import RESTRICT

# Create your models here.
class Book(models.Model):
    code=models.AutoField(primary_key=True, unique=True, max_length=100)
    bookname=models.CharField(max_length=255,unique=True, default= 'NULL' , null=True)
    author=models.ForeignKey('Author',on_delete=models.SET_NULL,null=True)
    publication=models.CharField(max_length=255,null=True)
    subject=models.CharField( max_length=255, null=True, blank=True)
    instances=models.IntegerField(null=True)
    
    def __str__(self):
        return self.bookname


class Author(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.first_name} , {self.last_name}'

class BookInstance(models.Model):
    book = models.ForeignKey(Book, on_delete=models.RESTRICT , null=True)
    due_back = models.DateField(null=True, blank=True)
    # check if using student here is correct in relationship
    student=models.ForeignKey('Student' , on_delete=models.RESTRICT, null=True )

    LOAN_STATUS = (
        ('o', 'On loan'),
        ('a', 'Available'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='a',
        help_text='Book availability',
    )


    def __str__(self):
        return f' {self.pk} ({self.book.bookname})'

class Student(models.Model):
    libid=models.AutoField(primary_key=True)
    regno=models.IntegerField(default='NULL',null=True, blank=True)
    branch=models.CharField(max_length=255 , null=True, default='NULL' , blank=True)
    section=models.CharField(max_length=2 , null=True, default='NULL' , blank=True)
    semester=models.CharField(max_length=255 , null=True, default='NULL' , blank=True)
    yearofadm=models.CharField(max_length=5 , null=True, default='NULL' , blank=True)

    def __str__(self):
        return self.libid


    