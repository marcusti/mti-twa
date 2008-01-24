from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.simple import direct_to_template
from twa.members.models import Document, Dojo, Graduation, Person
import csv

def get_context( request ):
    my_context = {}
    my_context['language'] = request.session.get( 'django_language' )
    return my_context

def mylogin( request ):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate( username=username, password=password )
    if user is not None:
        if user.is_active:
            login( request, user )
            return direct_to_template( request,
                template = 'base.html',
                extra_context = get_context( request )
            )

def index( request ):
    ctx = get_context( request )
    return direct_to_template( request,
        template = 'base.html',
        extra_context = ctx,
    )

def dojos( request ):
    ctx = get_context( request )
    return object_list(
        request,
        queryset = Dojo.objects.all(),
        paginate_by = 50,
        extra_context = ctx,
    )

def dojos_search( request ):
    s = request['s']
    sid = request['sid']
    ctx = get_context( request )
    ctx['search'] = s
    ctx['searchid'] = sid

    if sid:
        qs = Dojo.objects.filter( Q( id__icontains = sid ) )
    else:
        qs = Dojo.objects.filter( Q( name__icontains=s ) |
                    Q( shortname__icontains=s ) |
                    Q( text__icontains=s ) |
                    Q( street__icontains=s ) |
                    Q( zip__icontains=s ) |
                    Q( city__icontains=s ) )

    return object_list(
        request,
        queryset = qs,
        extra_context = ctx,
    )

def dojo( request, did = None ):
    ctx = get_context( request )
    ctx['members'] = Person.objects.filter( dojos__id = did )
    return object_detail(
        request,
        queryset = Dojo.objects.all(),
        object_id = did,
        template_object_name = 'dojo',
        extra_context = ctx,
    )

@login_required
def members( request ):
    ctx = get_context( request )
    return object_list(
        request,
        queryset = Person.actives.all(),
        paginate_by = 50,
        extra_context = ctx,
    )

@login_required
def members_search( request, p=None ):
    s = request['s']
    sid = request['sid']
    ctx = get_context( request )
    ctx['search'] = s
    ctx['searchid'] = sid

    if sid:
        qs = Person.actives.filter( Q( id__icontains = sid ) )
    else:
        qs = Person.actives.filter( Q( firstname__icontains=s ) |
                    Q( lastname__icontains=s ) |
                    Q( text__icontains=s ) |
                    Q( email__icontains=s ) |
                    Q( street__icontains=s ) |
                    Q( zip__icontains=s ) |
                    Q( city__icontains=s ) )

    return object_list(
        request,
        queryset = qs,
        extra_context = ctx,
    )

@login_required
def member( request, mid = None ):
    ctx = get_context( request )
    ctx['dojos'] = Dojo.objects.filter( person__id = mid )
    ctx['graduations'] = Graduation.objects.filter( person__id = mid )
    ctx['documents'] = Document.objects.filter( person__id = mid )
    return object_detail(
        request,
        queryset = Person.actives.all(),
        object_id = mid,
        template_object_name = 'person',
        extra_context = ctx,
    )

@login_required
def dojos_csv( request ):
    response = HttpResponse( mimetype='text/csv' )
    response['Content-Disposition'] = 'attachment; filename=dojos.csv'

    writer = csv.writer( response )

    for p in Person.objects.all():
        writer.writerow( [p.firstname, p.lastname] )

    return response
