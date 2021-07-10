from django.utils import translation
from rest_framework import serializers
from .models import Book,BookInstance,Author,Notice

class AuthorSerializer(serializers.ModelSerializer):
	# books = serializers.HyperlinkedRelatedField(view_name='Author-detail',many=True, queryset=Book.objects.all(),allow_null=True)
	class Meta:
		model = Author
		fields = ['id','first_name', 'last_name', 'about']


class BookSerializer(serializers.ModelSerializer):
	# copies = serializers.HyperlinkedRelatedField(view_name='Book-detail',many=True, queryset=BookInstance.objects.all(),allow_null=True)
	# instance = serializers.PrimaryKeyRelatedField(many=True,queryset=BookInstance.objects.all())
	# returns a list of hyperlinks to the book instances, can change to returning just the primary key
	class Meta:
		model = Book
		fields = ['code', 'bookname', 'author','publication','subject','instances']
	# while creating book, by default create req number of instances.
	def create(self, validated_data):
		book_model = Book(
			bookname=validated_data['bookname'],
			author=validated_data['author'],
			publication=validated_data['publication'],
			subject=validated_data['subject'],
			instances=validated_data['instances'],
		)
		book_model.save()
		book_id = book_model.code
		copies = int (validated_data['instances'])
		for i in range(copies):
			instance = BookInstance(
				book=book_model,
				due_back=None,
				student=None,
				is_available=True,
			)
			instance.save()

		return book_model

# class StudentSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = Student
# 		fields = ['libid','regno','branch','section','semester','yearofadm']

class BookInstanceSerializer(serializers.ModelSerializer):
	# book = BookSerializer()
	# student = StudentSerializer()
	class Meta:
		model = BookInstance
		fields = ['id','book', 'due_back','is_available']


class NoticeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Notice
		fields = ['id','posted_on', 'title', 'content', 'is_approved']