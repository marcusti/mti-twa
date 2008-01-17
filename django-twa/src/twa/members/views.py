from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.simple import direct_to_template
from twa.members.models import Dojo, Person
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

def index(request):
    return direct_to_template( request,
        template = 'base.html',
        extra_context = get_context( request )
    )

def dojos( request ):
    return object_list(
        request,
        queryset = Dojo.objects.all(),
        extra_context = get_context( request ),
    )

@login_required
def members( request ):
    return object_list(
        request,
        queryset = Person.actives.all(),
        extra_context = get_context( request ),
    )

@login_required
def dojos_csv( request ):
    response = HttpResponse( mimetype='text/csv' )
    response['Content-Disposition'] = 'attachment; filename=dojos.csv'

    writer = csv.writer( response )

    for p in Person.objects.all():
        writer.writerow( [p.firstname, p.lastname] )

    return response
