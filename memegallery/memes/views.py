from idlelib.rpc import request_queue
from pprint import pprint

from django.db.models import F
from django.forms import ModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.base import kwarg_re
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView, ListView, FormView

from .forms import AddMemeForm, AddPollForm, VoteForm, RatingForm, CommentForm

from .models import Memes, Question

import re

symbols = r'!%^&*()+={}|~[]\;"' + "':<>?,./#"

def translate(line: str):
    return re.sub(r"[^\w]", '-', line)


### Базовые страницы ###
class HomeView(ListView):
    template_name = 'memes/memes_list.html'
    context_object_name = 'memes'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Актуальные мемы'
        return context

    def get_queryset(self):
        return Memes.objects.filter(date__lte=timezone.now()).order_by('-date')[:5]

class MemesListView(HomeView):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все мемы'
        return context

    def get_queryset(self):
        return Memes.objects.filter(date__lte=timezone.now()).order_by('-date')

class AboutView(TemplateView):
    template_name = 'memes/about.html'

class ContactsView(TemplateView):
    template_name = 'memes/contact.html'

### Страница с мемом ###
class MemeDetailView(View):
    def get(self, request, meme_slug, *args, **kwargs):
        meme = get_object_or_404(Memes, slug=meme_slug)
        comment_form = CommentForm()
        return render(request,
                      'memes/meme_detail.html',
                      context={'meme': meme, 'comment_form': comment_form, 'comments': meme.anonymouscomment_set.all()})

    def post(self, request, meme_slug):
        meme = get_object_or_404(Memes, slug=meme_slug)
        rating_form = RatingForm(request.POST)
        if rating_form.is_valid():
            meme.rating += int(rating_form.cleaned_data['rating'])
            meme.save()

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.save()

        return HttpResponseRedirect(reverse('memes:meme_for_id', args=[meme_slug]))

### Отправка мемов ###
class SendMemeView(FormView):
    template_name = 'memes/add_meme.html'
    form_class = AddMemeForm
    success_url = reverse_lazy('memes:memes')

    def form_valid(self, form):
        meme = form.save(commit=False)
        title = form.cleaned_data['title'].replace(' ', '-')
        meme.slug = translate(title)
        meme.save()
        return super().form_valid(form)


### Страница со всеми опросами ##
class PollView(ListView):
    template_name = 'memes/polls.html'
    context_object_name = 'recent_polls'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')


### Создание опроса ##
class CreatePollView(FormView):
    template_name = 'memes/create_poll.html'
    form_class = AddPollForm
    success_url = reverse_lazy('memes:main')

    def form_valid(self, form):
        data = form.cleaned_data
        question = Question.objects.create(title=data['title'],
                                           description=data['description'],
                                           slug=translate(data['title']),
                                           end_date=data['end_date']
                                           )

        for meme in data['memes']:
            question.choice_set.create(question=question, meme=meme)

        return super().form_valid(form)


### Просмотр опросов и голосование ###
class PollDetailView(View):
    def get(self, request, poll_id, *args, **kwargs):
        return render(request, 'memes/view_poll.html',
                      context={'question': get_object_or_404(Question, slug=poll_id)}
                      )

    def post(self, request, *args, **kwargs):
        form = VoteForm(request.POST)
        if form.is_valid():
            form.cleaned_data['choice'].votes += 1
            form.cleaned_data['choice'].save()

        return HttpResponseRedirect(reverse('memes:main'))

def poll_view_results(request: HttpRequest, poll_id):
    question = get_object_or_404(Question, slug=poll_id)
    return render(request, 'memes/poll_result.html', context={'question': question})

class PollResultsView(ListView):
    template_name = 'memes/poll_result.html'
    context_object_name = 'choices'

    def get_queryset(self):
        queryset = get_object_or_404(Question, slug=self.kwargs['poll_id']).choice_set.all()
        return queryset