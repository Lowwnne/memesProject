from django.urls import path
from . import  views

app_name = 'memes'
urlpatterns = [
    path('memes/', views.memes, name='memes'),
    path('memes/<slug:meme_slug>/', views.meme_for_id, name='meme_for_id'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('send_meme/', views.send_meme, name='send_meme'),
    path('send_meme/processing', views.add_meme, name='add_meme'),
    path('', views.main, name='main')
]