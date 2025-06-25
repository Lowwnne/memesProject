from django.urls import path
from . import  views

app_name = 'memes'
urlpatterns = [
    # Базовые страницы
    path('', views.main, name='main'),
    path('memes/', views.memes, name='memes'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),

    # Страница с мемом
    path('memes/<slug:meme_slug>/', views.meme_for_id, name='meme_for_id'),
    path('memes/<slug:meme_slug>/comment/', views.meme_comment, name='meme_comment'),

    # Отправка мемов
    path('send_meme/', views.send_meme, name='add_meme'),

    # Страница со всеми опросами
    path('polls/', views.polls, name='polls'),

    # Создание опроса
    path('polls/create_poll/', views.create_poll_view, name='create_poll'),

    # Просмотр опросов и голосование
    path('polls/<slug:poll_id>/', views.poll_view, name='poll_view'),
    path('polls/<slug:poll_id>/processing/', views.poll_view_processing, name='poll_view_processing'),
    path('polls/<slug:poll_id>/results/', views.poll_view_results, name='poll_view_results')
]