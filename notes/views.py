from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.db.models import Q
from .models import Note, Category
from .forms import NoteForm, NewUserForm
from django.contrib.auth import login
from django.contrib import messages


def home(request):
    notes_list = get_list_or_404(Note.objects.order_by('-created_date'))
    categories_list = get_list_or_404(Category.objects.order_by('-title'))
    context = {'notes_list': notes_list, 'categories_list': categories_list}
    return render(request, 'notes/home.html', context)


def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("notes:homepage")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = NewUserForm()
    return render(request, "notes/register.html", {"register_form": form})


def note_detail(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    return render(request, 'notes/note_detail.html', {'note': note})


def category_detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    notes = category.notes.all()
    return render(request, 'notes/category_detail.html', {'category': category, 'notes': notes})


def categories(request):
    categories_list = get_list_or_404(Category.objects.order_by('-title'))
    context = {'categories_list': categories_list}
    return render(request, 'notes/categories.html', context)


def form_view(request):
    note_form = NoteForm()
    context = {'note_form': note_form}
    return render(request, 'notes/note_form.html', context)


def new_note(request, category_id):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to create a new note.")
        return redirect('notes:login')
    if request.method == 'POST':
        note_form = NoteForm(request.POST)
        if note_form.is_valid():
            note = note_form.save()
            note.author = request.user
            note.save()
            return redirect('notes:note_detail', note_id=note.id)
    else:
        if category_id == 0:
            note_form = NoteForm()
        else:
            note_form = NoteForm(initial={'category': Category.objects.get(pk=category_id)})
        return render(request, 'notes/note_form.html', {'note_form': note_form})


def edit_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    if note.author != request.user and not request.user.is_superuser:
        messages.error(request, "You do not have permission to edit this note.")
        return redirect('notes:note_detail', note_id=note.id)
    else:
        if request.method == 'POST':
            note_form = NoteForm(request.POST)
            if note_form.is_valid():
                note.title = note_form.cleaned_data['title']
                note.text = note_form.cleaned_data['text']
                note.category = note_form.cleaned_data['category']
                note.reminder = note_form.cleaned_data['reminder']
                note.save()
                return redirect('notes:note_detail', note_id=note.id)
        else:
            note_form = NoteForm(initial={'title': note.title, 'text': note.text, 'category': note.category,
                                          'reminder': note.reminder})
        return render(request, 'notes/note_form.html', {'note_form': note_form})


def delete_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    if note.author != request.user and not request.user.is_superuser:
        messages.error(request, "You do not have permission to delete this note.")
        return redirect('notes:note_detail', note_id=note.id)
    note.delete()
    return redirect('notes:homepage')


def search_notes(request):
    query = request.GET.get('query')
    notes = Note.objects.filter(Q(title__icontains=query))
    context = {'notes': notes, 'query': query}
    return render(request, 'notes/search_notes.html', context)


def filtered_results(request):
    category = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if category == 'all':
        notes = Note.objects.all().order_by('-created_date')
    elif category == 'uncategorized':
        notes = Note.objects.filter(category__isnull=True).order_by('-created_date')
    else:
        notes = Note.objects.filter(category__title__exact=category).order_by('-created_date')

    if start_date and end_date:
        notes = notes.filter(reminder__range=[start_date, end_date])
    elif start_date:
        notes = notes.filter(reminder__gte=start_date)
    elif end_date:
        notes = notes.filter(reminder__lte=end_date)
        
    context = {'notes': notes, 'start_date': start_date, 'end_date': end_date, 'category': category}
    return render(request, 'notes/filtered_results.html', context)


def easter_egg(request):
    context = {'hide_egg': 1}
    return render(request, 'notes/easter_egg.html', context)
