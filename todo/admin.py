from django.contrib import admin

# Register your models here.
from .models import ToDo


@admin.register(ToDo)
class ToDoAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', )