from django.contrib import admin
from .models import Note


admin.site.register(Note)  # Note class will be showed in admin panel
