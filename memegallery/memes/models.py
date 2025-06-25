import datetime

from django.db import models
from django.forms import ModelForm
from django.urls import reverse
from django.utils import timezone

def date_path(instance, filename):
    return f'{timezone.now().date()}/{filename}'

class Memes(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    image = models.ImageField(upload_to=date_path, verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание', null=True)
    rating = models.IntegerField(default=0, null=True)
    date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date <= now

    def get_absolute_url(self):
        return reverse('memes:meme_for_id', kwargs={'meme_slug': self.slug})

    def __str__(self):
        return self.title

class Question(models.Model):
    title = models.CharField(max_length=202, verbose_name='Заголовок')
    description = models.CharField(max_length=202, verbose_name='Описание')
    slug = models.SlugField(unique=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(verbose_name='Дата окончания', null=True)
    winner = models.ForeignKey(Memes, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    meme = models.ForeignKey(Memes, on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.question.title

class AnonymousComment(models.Model):
    name = models.CharField(max_length=202, default='Anonymous')
    comment = models.CharField(max_length=300)
    pub_date = models.DateTimeField(auto_now_add=True, null=True)
    meme = models.ForeignKey(Memes, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name, self.meme

class MemeForm(ModelForm):
  class Meta:
        model = Memes
        fields = ('title', 'image', 'description')

class PollQuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ('title', 'description')
