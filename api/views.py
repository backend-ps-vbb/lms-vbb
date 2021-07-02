from .models import Student, Book, BookInstance, Author, Notice
from .serializers import StudentSerializer, BookSerializer, AuthorSerializer, BookInstanceSerializer, NoticeSerializer
from rest_framework import viewsets

class StudentModelViewset(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
  
class BookModelViewset(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class AuthorModelViewset(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookInstanceModelViewset(viewsets.ModelViewSet):
    queryset = BookInstance.objects.all()
    serializer_class = BookInstanceSerializer
    
class NoticeModelViewset(viewsets.ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
















