from django.urls import path
from . import views


urlpatterns = [
    path('hello/', views.hello),
    path('category_<int:category_id>/', views.category_detail, name='category_detail'),
    path('note_<int:note_id>/', views.note_detail, name='note_detail'),
    path('new_note_<int:category_id>', views.new_note, name='new_note'),
    path('note_<int:note_id>/delete/', views.delete_note, name='delete_note'),
    path('note_<int:note_id>/edit/', views.edit_note, name='edit_note'),
    path('categories/', views.categories, name='categories_list'),
    path('search/', views.search_notes, name='search_notes'),
    path('filter/', views.filtered_results, name='filtered_results'),
    path('', views.home, name='homepage'),
]
