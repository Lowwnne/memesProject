from idlelib.rpc import request_queue

from django.db.models import F
from django.forms import ModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Memes, MemeForm

memes_list = Memes.objects.all()

def memes(request: HttpRequest):
  return render(request, 'memes/memes_list.html', context={'memes': memes_list})

def meme_for_id(request: HttpRequest, meme_slug):
  meme = get_object_or_404(Memes, slug=meme_slug)
  return render(request, 'memes/meme_detail.html', context={'meme': meme})

def about(request: HttpRequest):
  return render(request, 'memes/about.html')

def contacts(request: HttpRequest):
  return render(request, 'memes/contact.html')

def main(request: HttpRequest):
  return render(request, 'memes/index.html')

def send_meme(request: HttpRequest):
  return render(request, 'memes/add_meme.html')

def add_meme(request: HttpRequest):
  form = MemeForm(request.POST, request.FILES)
  print(request.FILES)
  if form.is_valid():
    new_meme = form.save(commit=False)
    new_meme.slug = request.POST['title'].replace(' ', '-')
    new_meme.save()
  print(form.errors)
  return HttpResponseRedirect(reverse('memes:main'))