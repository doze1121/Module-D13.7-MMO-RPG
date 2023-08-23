from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from .models import *


class PostCreateForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        label='Категория',
        widget=forms.Select(attrs={'class': 'form-select'}),
        queryset=Category.objects.all()
    )
    title = forms.CharField(label='Заголовок', widget=forms.TextInput(attrs={'class': 'form-control'}))
    text = forms.CharField(label='Описание', widget=CKEditorUploadingWidget(attrs={'class': 'form-control'}))


    class Meta:
        model = Post
        exclude = ('author',)


class CommentCreateForm(forms.ModelForm):
    text = forms.CharField(label='Текст', widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Comment
        fields = ('text',)
