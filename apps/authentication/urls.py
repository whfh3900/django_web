from django.urls import path
from . import views


urlpatterns = [

    path('', views.home, name='home'),
    path('introduction_download/', views.introduction_download, name='introduction_download'),
    path('ats_login/', views.ats_login, name='ats_login'),
    path('userinfo/', views.userinfo, name='userinfo'),
    path('settings/', views.settings, name='settings'),
]
