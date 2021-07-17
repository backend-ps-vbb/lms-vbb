from django.db import models
from django.db.models.deletion import RESTRICT
from accounts.models import CustomUser
# Create your models here.
class Book(models.Model):
    code=models.AutoField(primary_key=True, unique=True)
    bookname=models.CharField(max_length=255,unique=True, default= None , null=True)
    author=models.ForeignKey('Author',on_delete=models.SET_NULL,null=True)
    publication=models.CharField(max_length=255,null=True)
    subject=models.CharField( max_length=255, null=True, blank=True)
    instances=models.IntegerField(null=False,blank=False,default=0)
    
    def __str__(self):
        return self.bookname

class Author(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    about = models.TextField(null=True, default=None , blank=True) #added this field incase we want to display an author page down the line
    def __str__(self):
        return f'{self.first_name} , {self.last_name}'

class History(models.Model): # record instance of issue and return
    book = models.ForeignKey('Book',on_delete=models.DO_NOTHING,null=False,blank=False)
    issued_on = models.DateField(null=False, blank=False)
    due_on = models.DateField(null=False, blank=False)
    instancne = models.ForeignKey('BookInstance',on_delete=models.DO_NOTHING,null=False,blank=False)
    issuer = models.ForeignKey(CustomUser,on_delete=models.DO_NOTHING,null=False,blank=False)
    returned = models.BooleanField(
        blank=True,
        default=None,
        help_text='Has the book been returned?',
    )

    def __str__(self):
        return f'{self.book} on {self.issued_on}'


class BookInstance(models.Model):
    book = models.ForeignKey(Book, on_delete=models.RESTRICT , null=True)
    due_back = models.DateField(null=True, blank=True)
    # student here is the user we're lending the book to.
    student=models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True ) # on deletion of a student we can assume the book is recovered. Suggest alt?

    is_available = models.BooleanField(
        blank=True,
        default=True,
        help_text='Is the book available?',
    )


    def __str__(self):
        return f' {self.book.bookname} #{self.pk} '

class Notice(models.Model):
    posted_on = models.DateField(null=True, blank=True)
    title = models.CharField(max_length=200,blank=False,null=False)
    content = models.TextField()
    posted_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True ) # on deletion of a student we can we delete their posings or set is as none?
    
    is_approved = models.BooleanField(
        blank=True,
        default=False,
        help_text='Approval status by librarian',
    )
    
    def __str__(self):
        return f' {self.title} ({self.posted_on})'