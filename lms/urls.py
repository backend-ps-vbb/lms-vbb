from django.contrib import admin
from django.urls import path, include
from api import views
from rest_framework.routers import DefaultRouter
from django.views.generic.base import TemplateView
#Create router object
router = DefaultRouter()

# router.register('studentapi', views.StudentModelViewset, basename = 'student')
router.register('bookapi', views.BookModelViewset, basename = 'book')
router.register('bookinstanceapi', views.BookInstanceModelViewset, basename = 'bookinstance')
router.register('noticeapi', views.NoticeModelViewset, basename = 'notice')
router.register('authorapi', views.AuthorModelViewset, basename = 'author')

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('admin/', admin.site.urls),
    path('api/',include('api.urls') ),
    path('app/',include('frontend.urls') ),
    path('auth/', include('rest_framework.urls', namespace = 'rest_framework')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

