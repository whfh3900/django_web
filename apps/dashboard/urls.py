from django.urls import path
from . import views


urlpatterns = [
    path('board/', views.board, name='board'),
    path('filelist/', views.filelist, name='filelist'),
    path('modify/', views.modify, name='modify'),
]
