from datetime import date
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.simple import direct_to_template
from twa.members.models import Document, Dojo, Graduation, Person

def get_context( request ):
    my_context = {}
    my_context['language'] = request.session.get( 'django_language' )
    return my_context

def index( request ):
    today = date.today()
    ctx = get_context( request )
    if request.user.is_authenticated():
        ctx['license_requests'] = Person.objects.filter( twa_license_requested__isnull = False )
        ctx['membership_requests'] = Person.objects.filter( twa_membership_requested__isnull = False )
        ctx['birthdays'] = Person.persons.get_next_birthdays()
        ctx['nominations'] = Graduation.objects.filter( is_nomination = True )
    return direct_to_template( request,
        template = 'base.html',
        extra_context = ctx,
    )

def dojos( request ):
    qs = Dojo.objects.all()
    ctx = get_context( request )
    ctx['counter'] = qs.count()
    return object_list(
        request,
        queryset = qs,
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

    ctx['counter'] = qs.count()

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
    qs = Person.objects.all()
    ctx = get_context( request )
    ctx['counter'] = qs.count()
    return object_list(
        request,
        queryset = qs,
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
        qs = Person.objects.filter( Q( id__exact = sid ) )
    else:
        qs = Person.objects.filter( Q( firstname__icontains=s ) |
                    Q( lastname__icontains=s ) |
                    Q( text__icontains=s ) |
                    Q( email__icontains=s ) |
                    Q( street__icontains=s ) |
                    Q( zip__icontains=s ) |
                    Q( city__icontains=s ) )

    ctx['counter'] = qs.count()

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
        queryset = Person.objects.all(),
        object_id = mid,
        template_object_name = 'person',
        extra_context = ctx,
    )

@login_required
def dojos_csv( request ):
    response = HttpResponse( mimetype='text/csv' )
    response['Content-Disposition'] = 'attachment; filename=dojos.csv'

    from csvutf8 import UnicodeWriter
    writer = UnicodeWriter( response )

    writer.writerow( ['id', 'name', 'street', 'zip', 'city', 'country'] )

    for d in Dojo.objects.all():
        writer.writerow( [str( d.id ), d.name, d.street, d.zip, d.city, d.country.get_name()] )

    return response
