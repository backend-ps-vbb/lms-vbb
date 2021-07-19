from django.shortcuts import render
from django.http import HttpResponse
from api.models import Book,BookInstance,Mentor,History

# Create your views here.

def book_report(request):
    books=Book.objects.all()
    instances=BookInstance.objects.all()
    return render(request,"analytics/book.html",{
    'books':books,
    'instances':instances,
    })

def mentor_report(request):
    mentors=Mentor.objects.all()
    return render(request,"analytics/mentor.html",{
    'mentors':mentors,
    })

def student_report(request):
    students=History.objects.all()
    return render (request,"analytics/student.html",{
    'students':students,
    })

def issue_report(request):
    issues=History.objects.all()
    return render (request,"analytics/issues.html",{
    'issues':issues,
    })