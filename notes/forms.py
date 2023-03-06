from django import forms
from .models import Note, Category
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout


class NoteForm(forms.Form):
    """Form for creating a new note"""
    title = forms.CharField(max_length=200)
    text = forms.CharField(widget=forms.Textarea)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    reminder = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'

        self.helper.layout = Layout(
            'title',
            'text',
            'category',
            'reminder',
            Submit('submit', 'Save', css_class='btn btn-primary')
        )



    # first().author is a temporary solution
    def save(self, author=Note.objects.first().author):
        note = Note()
        note.title = self.cleaned_data['title']
        note.text = self.cleaned_data['text']
        note.category = self.cleaned_data['category']
        note.reminder = self.cleaned_data['reminder']
        note.author = author
        return note
