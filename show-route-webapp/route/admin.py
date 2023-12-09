from django.contrib.gis.admin.options import GISModelAdmin
from django.contrib import admin
from .models import Attraction

@admin.register(Attraction)
class AttractionAdmin(GISModelAdmin):
    list_display = ('name', 'location')


