from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import BookModelViewset,BookInstanceModelViewset,AuthorModelViewset,NoticeModelViewset
app_name="api"
router=SimpleRouter()
router.register('instances',BookInstanceModelViewset,basename='Instances')
router.register('books',BookModelViewset,basename='Book-detail')
router.register('authors',AuthorModelViewset,basename='Author-detail')
router.register('noticeboard',NoticeModelViewset,basename='Noticeboard')
# router.register('students',StudentModelViewset,basename='Student-record')

urlpatterns = router.urls