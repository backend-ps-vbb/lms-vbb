from django import forms
from django.contrib.auth.forms import UserCreationForm
from api.models import *
from accounts.models import CustomUser

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

#notice form for students => by default dont approve. approve by default for admins
class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title','content']

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'    

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username' ,'email', 'password1', 'password2', 'branch', 'section','semester','yearofadm') 