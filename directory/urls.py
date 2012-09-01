from django.conf.urls.defaults import *
from django.views.generic import list_detail
from django.conf import settings
from directory.archives.models import Archive
from haystack.forms import SearchForm
from haystack.views import SearchView
from django.contrib import admin
admin.autodiscover()

archive_list_info = {
    'queryset': Archive.objects.all().order_by('name'),
    'template_name': 'archives/list.html',
    'template_object_name': 'archives'
}
archive_detail_info = {
    'queryset': Archive.objects.all(),
    'template_name': 'archives/detail.html',
    'template_object_name': 'archive'
}

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('haystack.views',
    url(r'^search/', SearchView(
        form_class=SearchForm
    ), name='haystack_search'),
)

urlpatterns += patterns('directory.archives.views',
    (r'^$', 'show_home'),
    (r'^archives/$', 'show_archives'),
    (r'^(?P<page>acknowledgements|about|contact)/$', 'show_page'),
    (r'^archives/page(?P<page>[0-9]+)/$', 'show_archives'),
    (r'^archives/(?P<letter>[a-zA-Z]{1})/$', 'show_archives'),
    (r'^archives/(?P<letter>[a-zA-Z]{1})/page(?P<page>[0-9]+)/$', 'show_archives'),
    (r'^archives/(?P<state>act|nsw|nt|qld|sa|tas|vic|wa)/$', 'show_archives'),
    (r'^archives/(?P<state>act|nsw|nt|qld|sa|tas|vic|wa)/page(?P<page>[0-9]+)/$', 'show_archives'),
    (r'^archive/(?P<daa_id>\d+)/$', 'redirect_archive'),
    (r'^archives/(?P<daa_id>\d+)/$', 'show_archive'),
    (r'^directory/data/(?P<daa_id>\d+).htm$', 'redirect_archive'),
    (r'^archive/(?P<slug>[\w\-]+)/$', 'redirect_archive'),
    (r'^(?P<slug>[\w\-]+)/$', 'redirect_archive'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )