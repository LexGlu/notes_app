from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.db.models import Q
from .models import Note, Category
from .forms import NoteForm, NewUserForm
from django.contrib.auth import login
from django.contrib import messages


def home(request):
    public_notes = get_list_or_404(Note.objects.filter(public=True).order_by('-created_date'))
    categories_list = get_list_or_404(Category.objects.order_by('-title'))
    if request.user.is_authenticated:
        user_notes = Note.objects.filter(author=request.user).order_by('-created_date')
        context = {'public_notes': public_notes, 'categories_list': categories_list, 'user_notes': user_notes}
    else:
        context = {'public_notes': public_notes, 'categories_list': categories_list}
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
    if note.author == request.user or note.public:
        return render(request, 'notes/note_detail.html', {'note': note})
    else:
        messages.error(request, "Requested note either does not exist or you do not have access to it.")
        return redirect('notes:homepage')


def category_detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.user.is_authenticated:
        notes = Note.objects.filter(Q(category=category) & (Q(author=request.user) | Q(public=True)))
    else:
        notes = Note.objects.filter(Q(category=category) & Q(public=True))
    return render(request, 'notes/category_detail.html', {'category': category, 'notes': notes})


def categories(request):
    if request.user.is_authenticated:
        categories_user_or_public = Category.objects.filter(Q(notes__author=request.user) | Q(notes__public=True)).distinct()
        context = {'categories_list': categories_user_or_public}
    else:
        context = {'categories_list': Category.objects.filter(notes__public=True).distinct()}
    return render(request, 'notes/categories.html', context)


def form_view(request):
    note_form = NoteForm(initial={'public_note': False})
    context = {'note_form': note_form}
    return render(request, 'notes/note_form.html', context)


def new_note(request):
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
        note_form = NoteForm()
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
                note.public = note_form.cleaned_data['public_note']
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
    if not request.user.is_authenticated:
        notes = Note.objects.filter(Q(title__icontains=query) & Q(public=True))
    else:
        notes = Note.objects.filter(Q(title__icontains=query) & (Q(author=request.user) | Q(public=True)))
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

    if not request.user.is_authenticated:
        notes = notes.filter(public=True)
    else:
        notes = notes.filter(Q(author=request.user) | Q(public=True))
        
    context = {'notes': notes, 'start_date': start_date, 'end_date': end_date, 'category': category}
    return render(request, 'notes/filtered_results.html', context)


def easter_egg(request):
    context = {'hide_egg': 1}
    return render(request, 'notes/easter_egg.html', context)
