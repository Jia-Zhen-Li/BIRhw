from django.urls import path
from hw1 import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('file_upload', views.upload_file, name='file_upload'),
    path('url_parser', views.url_parser, name='url_parser'),
]

if settings.DEBUG: 
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root = settings.MEDIA_ROOT
    )