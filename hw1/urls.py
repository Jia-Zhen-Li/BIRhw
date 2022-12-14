from django.urls import path
from hw1 import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('test', views.test, name='test'),
    path('file_upload_counter', views.upload_file_counter, name='file_upload_counter'),
    path('url_parser_counter', views.url_parser_counter, name='url_parser_counter'),
]

if settings.DEBUG: 
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root = settings.MEDIA_ROOT
    )