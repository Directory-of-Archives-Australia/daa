from django.views.generic import list_detail
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponsePermanentRedirect
from models import Archive, Slug
from string import ascii_lowercase

STATES = ['ACT','NSW','NT','SA','Qld','Vic','Tas','WA']
STATES_UPPER = ['ACT','NSW','NT','SA','Qld','VIC','TAS','WA']

def show_home(request):
    return render_to_response('archives/home.html')

def show_archives(request, page='1', **kwargs):
    extra = {}
    if 'letter' in kwargs:
        archives_list = Archive.objects.filter(name__istartswith=kwargs['letter']).order_by('name')
        extra = {'letter': kwargs['letter'], 'path': '/archives/%s' % kwargs['letter'], 'letters': ascii_lowercase}
    elif 'state' in kwargs:
        archives_list = Archive.objects.filter(state__iexact=kwargs['state']).order_by('name')
        extra = {'state': kwargs['state'], 'path': '/archives/%s' % kwargs['state'], 'states': STATES}
    else:
        archives_list = Archive.objects.all().order_by('name')
        extra = { 'path': '/archives', 'letters': ascii_lowercase, 'states': STATES}
    return list_detail.object_list(
        request,
        queryset = archives_list,
        template_name = 'archives/list.html',
        template_object_name = 'archives',
        extra_context = extra,
        paginate_by = 25,
        page = page
    )

def show_archive(request, daa_id):
    if 'state' in request.GET:
        if request.GET['state'].upper() in STATES_UPPER:
            state = request.GET['state'].lower()
        else:
            state = None
    else:
        state = None
    extra = {'state': state}
    return list_detail.object_detail(
        request,
        queryset = Archive.objects.all().order_by('name'),
        template_name = 'archives/detail.html',
        template_object_name = 'archive',
        object_id = daa_id,
        extra_context = extra
    )

def show_page(request, page):
    return render_to_response('archives/%s.html' % page)
        
def redirect_archive(request, **kwargs):
    if 'daa_id' in kwargs:
        new_url = '/archives/%s' % kwargs['daa_id']
    if 'slug' in kwargs:
        slug_link = get_object_or_404(Slug, slug=kwargs['slug'])
        new_url = '/archives/%s' % slug_link.archive.daa_id
    return HttpResponsePermanentRedirect(new_url)
    