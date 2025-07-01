from django.urls import path
from . import  views

app_name = 'memes'
urlpatterns = [
    # Базовые страницы
    path('', views.HomeView.as_view(), name='main'),
    path('memes/', views.MemesListView.as_view(), name='memes'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),

    # Страница с мемом
    path('memes/<slug:meme_slug>/', views.MemeDetailView.as_view(), name='meme_for_id'),

    # Отправка мемов
    path('send_meme/', views.SendMemeView.as_view(), name='add_meme'),

    # Страница со всеми опросами
    path('polls/', views.PollView.as_view(), name='polls'),

    # Создание опроса
    path('polls/create_poll/', views.CreatePollView.as_view(), name='create_poll'),

    # Просмотр опросов и голосование
    path('polls/<slug:poll_id>/', views.PollDetailView.as_view(), name='poll_view'),
    path('polls/<slug:poll_id>/results/', views.PollResultsView.as_view(), name='poll_view_results')
]