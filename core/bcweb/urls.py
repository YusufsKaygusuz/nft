from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.mainpage, name="mainpage"),
    path('register/', views.register, name='register'),
    path('verify/', views.verify_certificate, name='verify_certificate'),
    path('search/', views.search_certificate, name='search_certificate'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)