from .models import Note, Category
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Save note', css_class='btn btn-success'))

    title = forms.CharField(max_length=200)
    text = forms.CharField(widget=forms.Textarea)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    reminder = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    public_note = forms.BooleanField(required=False)

    def save(self):
        note = Note()
        note.title = self.cleaned_data['title']
        note.text = self.cleaned_data['text']
        note.category = self.cleaned_data['category']
        note.reminder = self.cleaned_data['reminder']
        note.public = self.cleaned_data['public_note']
        return note


class LoginForm(forms.Form):
    """Form for logging in"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Log in', css_class='btn btn-success'))

    username = forms.CharField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput)
