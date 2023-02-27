from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from .models import Note


def hello(request):
    return HttpResponse('Hello from Notes app.')


def note_detail(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    return render(request, 'notes/note_detail.html', {'note': note})


def index(request):
    notes_list = get_list_or_404(Note.objects.order_by('-created_date'))
    context = {'notes_list': notes_list}
    return render(request, 'notes/index.html', context)


def note_new(request):
    pass
