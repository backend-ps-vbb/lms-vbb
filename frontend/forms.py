from django import forms

from api.models import *


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'