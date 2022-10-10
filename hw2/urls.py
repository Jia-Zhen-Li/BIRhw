from django.urls import path
from hw2 import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('test', views.test, name='test'),
    path('file_upload_zipf', views.uploadfile_zipf, name='file_upload_zipf'),
    path('url_parser_zipf', views.url_zipf, name='url_parser_zipf'),
]

if settings.DEBUG: 
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root = settings.MEDIA_ROOT
    )