import django_filters
from .models import Book

class BookModelFilter(django_filters.FilterSet):

    class Meta:
        model = Book 
        fields = ('code', 'bookname', 'author','publication','subject','instances')