# coding=utf-8
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.db.models import BLANK_CHOICE_DASH

from news.models import News


class NewsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        form = super(NewsForm, self).__init__(*args, **kwargs)

    class Meta:
        model = News
        exclude = ['published_by']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'short_description': CKEditorWidget(attrs={'cols': 80, 'rows': 30}),
            'description': CKEditorWidget(attrs={'cols': 80, 'rows': 30}),
            'banner_image': forms.FileInput(attrs={}),
            'more_info_text': forms.TextInput(attrs={'class': 'form-control'}),
            'more_info_url': forms.TextInput(attrs={'class': 'form-control'}),
        }

