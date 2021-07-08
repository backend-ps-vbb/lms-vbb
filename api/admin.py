from django.contrib import admin
from .models import Author, Book, BookInstance, Notice

# @admin.register(Student)
# class StudentAdmin(admin.ModelAdmin):
#     list_display = ['libid', 'regno', 'branch', 'section', 'semester']
    
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['code', 'bookname', 'author', 'publication', 'subject', 'instances']
    
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ['book', 'due_back']
    
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'about']
    
@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ['posted_on', 'title', 'content']
    
