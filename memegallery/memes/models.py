from django.db import models
from django.forms import ModelForm
from django.urls import reverse


class Memes(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)

    def get_absolute_url(self):
        return reverse('meme_for_id', kwargs={'meme_slug': self.slug})

    def __str__(self):
        return self.title


class MemeForm(ModelForm):
  class Meta:
    model = Memes
    fields = ('title', 'image', 'description')