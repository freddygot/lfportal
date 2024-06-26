from django.contrib import admin
from .models import Prosedyre, ProsedyrePunkt, ProsedyreGjennomgang

class ProsedyrePunktInline(admin.TabularInline):
    model = ProsedyrePunkt
    extra = 1

@admin.register(Prosedyre)
class ProsedyreAdmin(admin.ModelAdmin):
    list_display = ('tittel', 'beskrivelse')
    inlines = [ProsedyrePunktInline]

@admin.register(ProsedyrePunkt)
class ProsedyrePunktAdmin(admin.ModelAdmin):
    list_display = ('prosedyre', 'beskrivelse', 'rekkefolge')
    list_filter = ('prosedyre',)
    ordering = ('prosedyre', 'rekkefolge')

@admin.register(ProsedyreGjennomgang)
class ProsedyreGjennomgangAdmin(admin.ModelAdmin):
    list_display = ('bruker', 'prosedyre', 'fullført', 'fullført_dato')
    list_filter = ('fullført', 'fullført_dato')
    search_fields = ('bruker__username', 'prosedyre__tittel')
