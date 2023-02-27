from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from .models import Note, Category


def hello(request):
    return HttpResponse('Hello from Notes app.')


def note_detail(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    return render(request, 'notes/note_detail.html', {'note': note})


def category_detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    notes = category.notes.all()
    return render(request, 'notes/category_detail.html', {'category': category, 'notes': notes})


def index(request):
    categories_list = get_list_or_404(Category.objects.order_by('-title'))
    context = {'categories_list': categories_list}
    return render(request, 'notes/index.html', context)


def note_new(request):
    pass
