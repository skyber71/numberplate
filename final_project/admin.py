from django.contrib import admin
from .forms import ArrayInputForm

class ArrayInputAdmin(admin.ModelAdmin):
    form = ArrayInputForm

admin.site.register(ArrayInputForm, ArrayInputAdmin)
