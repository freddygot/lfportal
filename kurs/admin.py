from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models import Count, F, ExpressionWrapper, FloatField, Q, Subquery, OuterRef
from .models import Kurs, Modul, FullfortModul

class ModulInline(admin.TabularInline):
    model = Modul
    extra = 1

class KursAdmin(admin.ModelAdmin):
    inlines = [ModulInline]

class GroupFilter(admin.SimpleListFilter):
    title = 'group'
    parameter_name = 'group'

    def lookups(self, request, model_admin):
        groups = Group.objects.all()
        return [(group.id, group.name) for group in groups]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(bruker__groups__id=self.value())
        return queryset

class CompletionFilter(admin.SimpleListFilter):
    title = 'completion'
    parameter_name = 'completion'

    def lookups(self, request, model_admin):
        return [
            ('incomplete', 'Ikke 100% fullført'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'incomplete':
            # Subquery to get the total number of modules per course
            total_moduler_subquery = Modul.objects.filter(kurs=OuterRef('modul__kurs')).values('kurs').annotate(total=Count('id')).values('total')

            # Annotate each FullfortModul with the total number of modules and calculate the progress
            queryset = queryset.annotate(
                total_moduler=Subquery(total_moduler_subquery, output_field=FloatField()),
                fullforte_moduler_count=Count('modul'),
                progresjon=ExpressionWrapper(
                    (F('fullforte_moduler_count') * 100.0) / F('total_moduler'),
                    output_field=FloatField()
                )
            ).filter(progresjon__lt=100)
            return queryset
        return queryset

class FullfortModulAdmin(admin.ModelAdmin):
    list_display = ('bruker', 'modul', 'fullfort_dato', 'prosent_fullfort')
    readonly_fields = ('prosent_fullfort',)
    list_filter = (GroupFilter, CompletionFilter)

    def prosent_fullfort(self, obj):
        kurs = obj.modul.kurs
        total_moduler = Modul.objects.filter(kurs=kurs).count()
        fullforte_moduler_count = FullfortModul.objects.filter(bruker=obj.bruker, modul__kurs=kurs).count()
        progresjon = (fullforte_moduler_count / total_moduler) * 100 if total_moduler > 0 else 0
        return f"{progresjon:.2f}%"

    prosent_fullfort.short_description = 'Prosent Fullført'

admin.site.register(Kurs, KursAdmin)
admin.site.register(Modul)
admin.site.register(FullfortModul, FullfortModulAdmin)
