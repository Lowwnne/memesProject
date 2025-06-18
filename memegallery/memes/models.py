import datetime

from django.db import models
from django.forms import ModelForm
from django.urls import reverse
from django.utils import timezone

def date_path(instance, filename):
    return f'{timezone.now().date()}/{filename}'

class Memes(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to=date_path)
    description = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date <= now

    def get_absolute_url(self):
        return reverse('memes:meme_for_id', kwargs={'meme_slug': self.slug})

    def __str__(self):
        return self.title


class MemeForm(ModelForm):
  class Meta:
    model = Memes
    fields = ('title', 'image', 'description')