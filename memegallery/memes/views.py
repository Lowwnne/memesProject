from idlelib.rpc import request_queue
from pprint import pprint

from django.db.models import F
from django.forms import ModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.base import kwarg_re
from django.urls import reverse
from django.utils import timezone

from .forms import AddMemeForm, AddPollForm, VoteForm, RatingForm, CommentForm
from .to_slug import to_slug

from .models import Memes, Question

### Базовые страницы ###
def main(request: HttpRequest):
    memes_list = Memes.objects.filter(date__lte=timezone.now()).order_by('-date')
    return render(request, 'memes/index.html', context={'recent_memes': memes_list})

def memes(request: HttpRequest):
    memes_list = Memes.objects.all()
    return render(request, 'memes/memes_list.html', context={'memes': memes_list})

def about(request: HttpRequest):
    return render(request, 'memes/about.html')

def contacts(request: HttpRequest):
    return render(request, 'memes/contact.html')


### Страница с мемом ###
def meme_for_id(request: HttpRequest, meme_slug):
    meme = get_object_or_404(Memes, slug=meme_slug)
    if request.method != 'POST':
        comment_form = CommentForm()
        return render(request,
                      'memes/meme_detail.html',
                      context={'meme': meme, 'comment_form': comment_form, 'comments': meme.anonymouscomment_set.all()})

    rating_form = RatingForm(request.POST)
    if rating_form.is_valid():
        meme.rating += int(rating_form.cleaned_data['rating'])
        meme.save()

    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment_form.save()

    return HttpResponseRedirect(reverse('memes:meme_for_id', args=[meme_slug]))


def meme_comment(request: HttpRequest, meme_slug):
    return HttpResponseRedirect(reverse('memes:meme_for_id', args=[meme_slug]))

### Отправка мемов ###
def send_meme(request: HttpRequest):
    if request.method == 'POST':
        form = AddMemeForm(request.POST, request.FILES)
        if form.is_valid():
            meme = form.save(commit=False)
            meme.slug = to_slug(form.cleaned_data['title'])
            meme.save()
            return HttpResponseRedirect(reverse('memes:main'))
    else:
        form = AddMemeForm()

    return render(request, 'memes/add_meme.html', context={'form': form})


### Страница со всеми опросами ##
def polls(request: HttpRequest):
    recent_polls = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
    return render(request, 'memes/polls.html', context={'recent_polls': recent_polls})


### Создание опроса ##
def create_poll_view(request: HttpRequest):
    if request.method == 'POST':
        form = AddPollForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            question = Question.objects.create(title=data['title'],
                                               description=data['description'],
                                               slug = to_slug(data['title']),
                                               end_date = data['end_date']
                                               )

            for meme in data['memes']:
                question.choice_set.create(question=question,
                                        meme=meme)
        HttpResponseRedirect(reverse('memes:main'))
    else:
        form = AddPollForm()

    return render(request, 'memes/create_poll.html', context={'form': form})


### Просмотр опросов и голосование ###
def poll_view(request: HttpRequest, poll_id):
    if request.method == 'POST':
        form = VoteForm(request.POST)
        if form.is_valid():
            form.cleaned_data['choice'].votes += 1
            form.cleaned_data['choice'].save()
        return HttpResponseRedirect(reverse('memes:main'))
    else:
        return render(request, 'memes/view_poll.html',
                      context={'question': get_object_or_404(Question, slug=poll_id)}
                      )

def poll_view_processing(request: HttpRequest, poll_id):
    if request.method == 'POST':
        q = get_object_or_404(Question, slug=poll_id)
        c = q.choice_set.get(meme=int(request.POST.getlist('voted_meme')[0]))
        c.votes += 1
        c.save()
    return HttpResponseRedirect(reverse('memes:poll_view_results', kwargs={'poll_id': q.slug}))

def poll_view_results(request: HttpRequest, poll_id):
    question = get_object_or_404(Question, slug=poll_id)
    return render(request, 'memes/poll_result.html', context={'question': question})