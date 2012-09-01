from directory.archives.models import *
from django.contrib import admin
from reversion.admin import VersionAdmin

class SlugInline(admin.TabularInline):
    model = Slug

class ArchiveAdmin(VersionAdmin):
    list_display = ('name', 'daa_id')
    search_fields = ('name',)
    ordering = ('daa_id',)


admin.site.register(Archive, ArchiveAdmin)
admin.site.register(Slug)
admin.site.register(ArchiveType)
admin.site.register(City_or_Suburb)
admin.site.register(Address)
admin.site.register(Website)
admin.site.register(Account)
admin.site.register(Role)
admin.site.register(Person)
admin.site.register(Publication)
admin.site.register(RelatedCollection)
admin.site.register(RelatedPerson)
admin.site.register(Collection)
admin.site.register(Organisation)
admin.site.register(Schema)
admin.site.register(Attribute)
admin.site.register(Relationship)
admin.site.register(Mapping)
