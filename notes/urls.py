from django.urls import path
from . import views


urlpatterns = [
    path('hello/', views.hello),
    path('note_<int:note_id>/', views.note_detail, name='note_detail'),
    path('', views.index, name='notes_list'),
]
