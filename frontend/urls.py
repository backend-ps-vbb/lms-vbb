from django.urls import path

from . import views
app_name="frontend"
urlpatterns = [
    # path("", views.index, name="index"),
    # path("search", views.search, name="search"),
    path('stdentcreate', views.StudentCreate, name='student_create'),

    path("books", views.BookListView, name="books"),
    path('book/<int:pk>/',views.BookDetailView, name='detail'),
    path('book/create/', views.BookCreate, name='book_create'),
    path('book/<int:pk>/issue/', views.BookIssue, name='book_issue'),
    path('book/<int:pk>/return/', views.BookReturn, name='book_return'),

    # path('authors', views.AuthorListView, name='author_list'),
    path('authors/create', views.AuthorCreate, name='author_create'),
    # path('authors/<int:pk>', views.AuthorDetail, name='author_create'),

    path("noticeboard/", views.notice_board, name="notice_board"),
    path("noticeboard/create", views.NoticeCreate, name="notice_create"),
    path("noticeboard/approve", views.approve_notice, name="approve_notice"),
     
]
