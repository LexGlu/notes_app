from django.urls import path, include
from . import views

app_name = 'notes'
urlpatterns = [
    path('category_<int:category_id>/', views.category_detail, name='category_detail'),
    path('note_<int:note_id>/', views.note_detail, name='note_detail'),
    path('new_note/', views.new_note, name='new_note'),
    path('note_<int:note_id>/delete/', views.delete_note, name='delete_note'),
    path('note_<int:note_id>/edit/', views.edit_note, name='edit_note'),
    path('categories/', views.categories, name='categories_list'),
    path('search/', views.search_notes, name='search_notes'),
    path('filter/', views.filtered_results, name='filtered_results'),
    path('easter_egg/', views.easter_egg, name='easter_egg'),
    path('account/', include('django.contrib.auth.urls')),
    path('account/register/', views.register, name='register'),
    path('my_notes/', views.my_notes, name='my_notes'),
    path('public_notes/', views.public_notes, name='public_notes'),
    path('', views.home, name='homepage'),
]
