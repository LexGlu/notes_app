from django.urls import path
from . import views


urlpatterns = [
    path('hello/', views.hello),
    path('category_<int:category_id>/', views.category_detail, name='category_detail'),
    path('note_<int:note_id>/', views.note_detail, name='note_detail'),
    path('', views.index, name='notes_list'),
]
