from django.urls import path

from . import views
app_name="frontend"
urlpatterns = [
    # path("", views.index, name="index"),
    # path("search", views.search, name="search"),
    path("noticeboard", views.notice_board, name="notice_board"),
    path("approvenotice", views.approve_notice, name="approve_notice"),
     
]
