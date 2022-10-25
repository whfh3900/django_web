from django.urls import path
from . import views_linux
from . import views_windows
from django.conf import settings
from django.conf.urls.static import static
import platform

if platform.system() == 'Windows':
    urlpatterns = [
        path('', views_windows.home, name='home'),
        path('introduction_download/', views_windows.introduction_download, name='introduction_download'),
        path('ats_login/', views_windows.ats_login, name='ats_login'),
        path('tagging/', views_windows.tagging, name='tagging'),
        path('complete_download/', views_windows.complete_download, name='complete_download'),
        path('history_download/', views_windows.history_download, name='history_download'),

    ]

elif platform.system() == 'Linux':
    urlpatterns = [
        path('', views_linux.home, name='home'),
        path('introduction_download/', views_linux.introduction_download, name='introduction_download'),
        path('ats_login/', views_linux.ats_login, name='ats_login'),
        path('tagging/', views_linux.tagging, name='tagging'),
        path('complete_download/', views_linux.complete_download, name='complete_download'),
        path('history_download/', views_linux.history_download, name='history_download'),

    ]