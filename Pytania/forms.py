from django import forms
from questionApi.models import SuggestQuestion


class NewQuestionForm(forms.ModelForm):
    class Meta:
        model = SuggestQuestion
        #fields = '__all__'
        exclude = ('status', )
        widgets = {'player': forms.HiddenInput()}