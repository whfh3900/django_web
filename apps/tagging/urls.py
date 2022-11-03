from django.urls import path
from . import views


urlpatterns = [
    path('tagging/', views.tagging, name='tagging'),
    path('complete_download/', views.complete_download, name='complete_download'),
    path('history_download/', views.history_download, name='history_download'),
]
