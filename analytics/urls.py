from django.urls import path 
from  . import views
urlpatterns=[ 
    path('book/',views.book_report,name='bookreport'),
    path('mentor/',views.mentor_report,name='mentorreport'),
    path('student/',views.student_report,name='studentreport'),
    path('issue/',views.issue_report,name='issuereport'),
]