from django import forms
from .models import Note, Category
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class NoteForm(forms.Form):
    """Form for creating a new note"""
    title = forms.CharField(max_length=200)
    text = forms.CharField(widget=forms.Textarea)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    reminder = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    def save(self):
        note = Note()
        note.title = self.cleaned_data['title']
        note.text = self.cleaned_data['text']
        note.category = self.cleaned_data['category']
        note.reminder = self.cleaned_data['reminder']
        return note
