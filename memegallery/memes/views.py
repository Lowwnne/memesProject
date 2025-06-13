from django.http import HttpRequest
from django.shortcuts import render
from .models import Memes

memes_list = Memes.objects.all()

def memes(request: HttpRequest):
  print([memes_list[i].image.url for i in range(len(memes_list))])
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

def send_meme(request: HttpRequest):
  return render(request, 'memes/add_meme.html')