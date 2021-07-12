from rest_framework.serializers import Serializer
from .models import  Book, BookInstance, Author, Notice
from .serializers import  BookSerializer, AuthorSerializer, BookInstanceSerializer, NoticeSerializer
from rest_framework import viewsets
# from rest_framework.parsers import JSONParser
# class StudentModelViewset(viewsets.ModelViewSet):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer
  
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
    # for students, view only approved notices, allow POST request. Do not allow acces to modify, delete. Do not allow modification of is_approved field
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
















