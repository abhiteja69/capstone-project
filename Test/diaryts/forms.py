from . models import Diaryt
from django import forms


class DiaryForm(forms.ModelForm):

    class Meta:
        model = Diaryt
        fields = ['title', 'description']