from django import forms
from django.contrib import admin

from coltrane.models import Category, Entry, Link


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ['title'] }

admin.site.register(Category, CategoryAdmin)


class EntryAdminForm(forms.ModelForm):
    class Meta:
        model = Entry
        widgets = {
            'categories': forms.SelectMultiple(attrs={'size': 6}),
            'body_html': forms.Textarea(attrs={'rows': 60, 'cols': 120})
        }


class EntryAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ['title'] }
    form = EntryAdminForm

    def queryset(self, request):
        # use objects manager, rather than the default one
        qs = self.model.objects.get_query_set()

        # we need this from the superclass method
        ordering = self.ordering or () # otherwise we might try to *None, which is bad ;)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


admin.site.register(Entry, EntryAdmin)


class LinkAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ['title'] }
    
admin.site.register(Link, LinkAdmin)
