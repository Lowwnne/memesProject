from django import forms
from prompt_toolkit.validation import ValidationError

from .models import *


class AddMemeForm(forms.ModelForm):
    class Meta:
        model = Memes
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TelInput(attrs={'id': 'title'}),
            'description': forms.Textarea(attrs={'rows': 4,
                                                 'id': 'description'}),
            'image': forms.FileInput(attrs={'id': 'image',
                                            'accept': 'image/*'})
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов')
        return title

class AddPollForm(forms.Form):
    title = forms.CharField(max_length=50,
                            widget=forms.TextInput(attrs={'id': 'title'}))
    description = forms.CharField(widget=forms.TextInput(attrs={
                                                'rows': 4,
                                                'id': 'description'
                                                }))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    memes = forms.ModelMultipleChoiceField(queryset=Memes.objects.all())

class VoteForm(forms.Form):
    choice = forms.ModelChoiceField(queryset=Choice.objects.all())

class RatingForm(forms.Form):
    CHOICES = [
        (1, 'Поднять рейтинг'),
        (-1, 'Опустить рейтинг')
    ]
    rating = forms.TypedChoiceField(choices=CHOICES,
                                    label='Рейтинг',
                                    widget=forms.RadioSelect(),
                                    )

class CommentForm(forms.ModelForm):
    meme = forms.ModelChoiceField(queryset=Memes.objects.all(),
                                  required=False,
                                  widget=forms.HiddenInput()
                                 )
    class Meta:
        model = AnonymousComment
        fields = ['name', 'comment', 'meme']
        widgets = {
            'comment': forms.Textarea(),
            'meme': forms.Select(attrs={'hidden': 'true'})
        }