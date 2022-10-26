from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('introduction_download/', views.introduction_download, name='introduction_download'),
    path('ats_login/', views.ats_login, name='ats_login'),
    path('tagging/', views.tagging, name='tagging'),
    path('complete_download/', views.complete_download, name='complete_download'),
    path('history_download/', views.history_download, name='history_download'),
]
