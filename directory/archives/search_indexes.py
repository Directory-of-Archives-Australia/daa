from haystack.indexes import *
from haystack import site
from models import Archive

class ArchiveIndex(SearchIndex):
    text = CharField(document=True, use_template=True)

    def get_queryset(self):
        return Archive.objects.filter(public=True)

site.register(Archive, ArchiveIndex)
