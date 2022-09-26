from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('introduction_download/', views.introduction_download, name='introduction_download'),
    path('ats_login/', views.ats_login, name='ats_login'),
    # path('ats_logout/', views.ats_logout, name='ats_logout'),

    path('tagging/', views.tagging, name='tagging'),
    path('complete_download/', views.complete_download, name='complete_download'),

]
