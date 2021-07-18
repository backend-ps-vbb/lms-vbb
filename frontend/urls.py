from django.urls import path

from . import views
app_name="frontend"
urlpatterns = [
    # path("", views.index, name="index"),
    # path("search", views.search, name="search"),

    path("books", views.BookListView, name="books"),
    path('book/<int:pk>/',views.BookDetailView, name='detail'),
    path('book/create/', views.BookCreate, name='book_create'),
    # path('book/<int:pk>/update/', views.BookUpdate, name='book_update'),
    # path('book/<int:pk>/delete/', views.BookDelete, name='book_delete'),

    path("noticeboard", views.notice_board, name="notice_board"),
    path("approvenotice", views.approve_notice, name="approve_notice"),
     
]
