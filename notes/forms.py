from django import forms
from .models import Note, Category


class NoteForm(forms.Form):
    """Form for creating a new note"""
    title = forms.CharField(max_length=200)
    text = forms.CharField(widget=forms.Textarea)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    reminder = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    # first().author is a temporary solution
    def save(self, author=Note.objects.first().author):
        note = Note()
        note.title = self.cleaned_data['title']
        note.text = self.cleaned_data['text']
        note.category = self.cleaned_data['category']
        note.reminder = self.cleaned_data['reminder']
        note.author = author
        return note
