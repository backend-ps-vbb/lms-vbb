from rest_framework import serializers
from .models import Book,BookInstance,Student,Author,Notice

class BookSerializer(serializers.ModelSerializer):
	copies = serializers.HyperlinkedRelatedField(many=True, queryset=BookInstance.objects.all(),read_only=True,allow_null=True)
	# returns a list of hyperlinks to the book instances, can change to returning just the primary key
	class Meta:
		model = Book
		fields = ['code', 'bookname', 'author','publication','subject','instances','copies']

class BookInstanceSerializer(serializers.ModelSerializer):
	class Meta:
		model = BookInstance
		fields = ['id','book', 'due_back', 'student','status']

class StudentSerializer(serializers.ModelSerializer):
	copies = serializers.HyperlinkedRelatedField(many=True, queryset=BookInstance.objects.all(),read_only=True,allow_null=True)
	# returns a list of hyperlinks to the book instances, can change to returning just the primary key
	class Meta:
		model = Student
		fields = ['libid', 'regno', 'branch','branch','section','semester','yearofadm']

class AuthorSerializer(serializers.ModelSerializer):
	books = serializers.HyperlinkedRelatedField(many=True, queryset=Book.objects.all(),read_only=True,allow_null=True)
	class Meta:
		model = Author
		fields = ['id','first_name', 'last_name', 'books', 'about']

class NoticeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Notice
		fields = ['id','posted_on', 'title', 'content', 'status']