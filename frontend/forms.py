from django import forms

from api.models import *


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

#notice form for students => by default dont approve. approve by default for admins
class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title','content']

    