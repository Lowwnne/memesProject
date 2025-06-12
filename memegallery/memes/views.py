from django.http import HttpRequest
from django.shortcuts import render

memes_list = [
  {'id': 1, 'title': 'Python – это боль', 'image': 'memes/python_pain.jpg', 'description': 'Но красивый синтаксис всё прощает.'},
  {'id': 2, 'title': 'Django в 2 ночи', 'image': 'memes/django_night.jpg', 'description': 'Когда дебаггер твой единственный друг.'},
]

def memes(request: HttpRequest):
  return render(request, 'memes/memes_list.html', context={'memes': memes_list})

def meme_for_id(request: HttpRequest, meme_id: int):
  return render(request, 'memes/meme_detail.html', context={'memes': memes_list, 'req_id': meme_id,
                                                                          'memes_ids': len(memes_list)})

def about(request: HttpRequest):
  return render(request, 'memes/about.html')

def contacts(request: HttpRequest):
  return render(request, 'memes/contact.html')

def main(request: HttpRequest):
  return render(request, 'memes/index.html')