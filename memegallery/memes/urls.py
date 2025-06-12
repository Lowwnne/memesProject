from django.urls import path
from . import  views

urlpatterns = [
    path('memes/', views.memes, name='memes'),
    path('memes/<int:meme_id>', views.meme_for_id, name='meme_for_id'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('', views.main, name='main')
]