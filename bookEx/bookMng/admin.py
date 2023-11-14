from django.contrib import admin
from .models import MainMenu
from .models import Book

# Register your models here.

admin.site.register(MainMenu)
admin.site.register(Book)