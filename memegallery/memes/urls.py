from django.urls import path
from . import  views

app_name = 'memes'
urlpatterns = [
    # Базовые страницы
    path('', views.main, name='main'),
    path('memes/', views.memes, name='memes'),
    path('memes/<slug:meme_slug>/', views.meme_for_id, name='meme_for_id'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),

    # Отправка мемов
    path('send_meme/', views.send_meme, name='send_meme'),
    path('send_meme/processing', views.add_meme, name='add_meme'),

    # Страница со всеми опросами
    path('polls/', views.polls, name='polls'),

    # Создание опроса
    path('polls/create_poll/', views.create_poll_view, name='create_poll'),
    path('polls/create_poll/processing/', views.create_poll_processing, name='create_poll_processing'),

    # Просмотр опросов и голосование
    path('polls/<slug:poll_id>/', views.poll_view, name='poll_view'),
    path('polls/<slug:poll_id>/processing/', views.poll_view_processing, name='poll_view_processing'),
    path('polls/<slug:poll_id>/results/', views.poll_view_results, name='poll_view_results')
]