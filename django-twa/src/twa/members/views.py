from datetime import date, datetime
from django import get_version
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.simple import direct_to_template, redirect_to
from twa.members.forms import LoginForm
from twa.members.models import Country, Document, Dojo, Graduation, Person, PersonManager, RANK
from twa.settings import LOGIN_REDIRECT_URL, LANGUAGES

def __get_rank_display( rank ):
    for id, name in RANK:
        if id == rank:
            return name
    return ''

def get_context( request ):
    my_context = {}
    my_context['language'] = request.session.get( 'django_language' )
    return my_context

def twa_login( request ):
    ctx = get_context( request )
    ctx['next'] = request.GET.get( 'next', LOGIN_REDIRECT_URL )
    ctx['LANGUAGES'] = LANGUAGES

    if request.method == 'POST':
        form = LoginForm( request.POST )
        if form.is_valid():
            # user authentication is done in LoginForm validation
            user = form.get_user()
            login( request, user )

            if not user.is_superuser:
                from django.core.mail import mail_admins, send_mail
                name = user.get_full_name()
                mail_admins( 'Login', '%s: %s hat sich eingeloggt' % ( datetime.now(), name ), fail_silently = True )

            if request.has_key( 'next' ):
                next = request['next']
            else:
                next = LOGIN_REDIRECT_URL

            return redirect_to( request, next )
    else:
        form = LoginForm()

    ctx['form'] = form
    return render_to_response(
               'members/login.html',
               ctx,
            )

@login_required
def info( request ):
    if not request.user.is_superuser:
        raise Http404

    now = datetime.now()

    if request.user.is_authenticated() and request.user.is_superuser:
        if request.POST.has_key( 'clean_up_expired_sessions' ):
            Session.objects.filter( expire_date__lt = now ).delete()
            transaction.commit_unless_managed()

    import sys
    ctx = get_context( request )
    ctx['django_version'] = get_version()
    ctx['python_version'] = sys.version
    ctx['users'] = User.objects.all().order_by( '-last_login' )
    ctx['active_sessions'] = Session.objects.filter( expire_date__gte = now ).order_by( 'expire_date' )
    ctx['expired_sessions'] = Session.objects.filter( expire_date__lt = now ).order_by( '-expire_date' )

    return direct_to_template( request,
        template = 'info.html',
        extra_context = ctx,
    )

def index( request ):
    today = date.today()
    ctx = get_context( request )
    if request.user.is_authenticated():
        ctx['license_requests'] = Person.persons.filter( twa_license_requested__isnull = False, twa_license__isnull = True ).order_by( '-twa_license_requested' )
        ctx['membership_requests'] = Person.persons.filter( twa_membership_requested__isnull = False, twa_membership__isnull = True ).order_by( '-twa_membership_requested' )
        ctx['birthdays'] = Person.persons.get_next_birthdays()
        ctx['nominations'] = Graduation.objects.filter( is_nomination = True )
    return direct_to_template( request,
        template = 'base.html',
        extra_context = ctx,
    )

def dojos( request ):
    ctx = get_context( request )

    countries = []
    for d in Dojo.objects.values( 'country' ).order_by( 'country' ).distinct():
        countries.append( ( str( d['country'] ), Country.objects.get( id = d['country'] ).get_name() ) )
    ctx['counties'] = countries

    if request.has_key( 's' ):
        s = request['s']
        ctx['search'] = s
        if s:
            qs = Dojo.objects.filter( Q( name__icontains=s ) |
                    Q( shortname__icontains=s ) |
                    Q( text__icontains=s ) |
                    Q( street__icontains=s ) |
                    Q( zip__icontains=s ) |
                    Q( city__icontains=s ) )
        else:
            qs = Dojo.objects.all()
    else:
        qs = Dojo.objects.all()

    if request.has_key( 'sid' ):
        sid = request['sid']
        ctx['searchid'] = sid
        if sid:
            qs &= Dojo.objects.filter( Q( id__icontains = sid ) )

    ctx['cities'] = Dojo.objects.values( 'city' ).order_by( 'city' ).distinct()
    if request.has_key( 'ci' ):
        city = request['ci']
        ctx['ci'] = city
        if city <> 'all':
            qs &= Dojo.objects.filter( city = city )

    if request.has_key( 'co' ):
        co = request['co']
        ctx['co'] = co
        if co <> 'all':
            ctx['cities'] = Dojo.objects.values( 'city' ).filter( country = co ).order_by( 'city' ).distinct()
            qs &= Dojo.objects.filter( country = co )
        else:
            ctx['cities'] = Dojo.objects.values( 'city' ).order_by( 'city' ).distinct()

    ctx['counter'] = qs.count()

    return object_list(
        request,
        queryset = qs,
        paginate_by = 50,
        extra_context = ctx,
    )

def dojo( request, did = None ):
    ctx = get_context( request )
    ctx['members'] = Person.persons.filter( dojos__id = did )
    return object_detail(
        request,
        queryset = Dojo.objects.filter( id = did ),
        object_id = did,
        template_object_name = 'dojo',
        extra_context = ctx,
    )

@login_required
def members( request ):
    #for p in Person.objects.all():
    #    p.save()

    ctx = get_context( request )

    if request.has_key( 'l' ):
        license = request['l']
        ctx['l'] = license
        if license == 'yes':
            qs = Person.persons.filter( twa_license__isnull = False )
        elif license == 'requested':
            qs = Person.persons.filter( twa_license_requested__isnull = False )
        else:
            qs = Person.persons.all()
    else:
        qs = Person.persons.all()

    if request.has_key( 'm' ):
        member = request['m']
        ctx['m'] = member
        if member == 'yes':
            qs &= Person.persons.filter( twa_membership__isnull = False )
        elif member == 'requested':
            qs &= Person.persons.filter( twa_membership_requested__isnull = False )
        else:
            qs &= Person.persons.all()

    if request.has_key( 's' ):
        s = request['s']
        ctx['search'] = s
        if s:
            qs &= Person.persons.filter( Q( firstname__icontains=s ) |
                    Q( lastname__icontains=s ) |
                    Q( text__icontains=s ) |
                    Q( email__icontains=s ) |
                    Q( street__icontains=s ) |
                    Q( zip__icontains=s ) |
                    Q( city__icontains=s ) )

    if request.has_key( 'sid' ):
        sid = request['sid']
        ctx['searchid'] = sid
        if sid:
            qs &= Person.persons.filter( Q( id__exact = sid ) )

    ranks = []
    for r in Graduation.objects.values( 'rank' ).distinct():
        ranks.append( ( str( r['rank'] ), __get_rank_display( r['rank'] ) ) )
    ctx['ranks'] = ranks

    if request.has_key( 'r' ):
        rank = request['r']
        ctx['r'] = rank
        if rank <> 'all':
            qs &= Person.persons.get_persons_by_rank( rank )

    ctx['counter'] = qs.count()

    return object_list(
        request,
        queryset = qs,
        paginate_by = 50,
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
        queryset = Person.persons.filter( id = mid ),
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

@login_required
def members_xls( request ):
    from pyExcelerator import *
    wb = Workbook()
    ws0 = wb.add_sheet( 'Members' )

    ws0.write( 0, 0, 'id')
    ws0.write( 0, 1, 'firstname')
    ws0.write( 0, 2, 'lastname')
    ws0.write( 0, 3, 'street')
    ws0.write( 0, 4, 'zip')
    ws0.write( 0, 5, 'city')
    ws0.write( 0, 6, 'country')
    ws0.write( 0, 7, 'phone')
    ws0.write( 0, 8, 'fax')
    ws0.write( 0, 9, 'mobile')
    ws0.write( 0, 10, 'email')
    ws0.write( 0, 11, 'website')
    ws0.write( 0, 12, 'rank')
    ws0.write( 0, 13, 'gender')
    ws0.write( 0, 14, 'birth')
    ws0.write( 0, 15, 'photo')
    ws0.write( 0, 16, 'text')

    x = 0
    for person in Person.persons.all().order_by( 'id' ):
        x += 1
        ws0.write( x, 0, str( person.id ) )
        ws0.write( x, 1, person.firstname )
        ws0.write( x, 2, person.lastname )
        ws0.write( x, 3, person.street )
        ws0.write( x, 4, person.zip )
        ws0.write( x, 5, person.city )
        ws0.write( x, 6, __get_name( person.country ) )
        ws0.write( x, 7, person.phone )
        ws0.write( x, 8, person.fax )
        ws0.write( x, 9, person.mobile )
        ws0.write( x, 10, person.email )
        ws0.write( x, 11, person.website )
        ws0.write( x, 12, person.get_current_rank_display() )
        ws0.write( x, 13, person.get_gender_display() )
        ws0.write( x, 14, str( person.birth ) )
        ws0.write( x, 15, person.photo )
        ws0.write( x, 16, person.text )

    filename = 'members-%s.xls' % datetime.now().strftime( '%Y%m%d%H%M%S' )
    wb.save( filename )
    response = HttpResponse( open( filename, 'r' ).read(), mimetype='application/ms-excel' )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response

@login_required
def members_csv( request ):
    response = HttpResponse( mimetype='text/csv' )
    response['Content-Disposition'] = 'attachment; filename=members.csv'

    from csvutf8 import UnicodeWriter
    writer = UnicodeWriter( response )

    writer.writerow( ['id',
                      'firstname',
                      'lastname',
                      'street',
                      'zip',
                      'city',
                      'country',
                      'phone',
                      'fax',
                      'mobile',
                      'email',
                      'website',
                      'rank',
                      'gender',
                      'birth',
                      'photo',
                      'text',
                      ] )

    for person in Person.persons.all().order_by( 'id' ):
        writer.writerow( [str( person.id ),
                          person.firstname,
                          person.lastname,
                          person.street,
                          person.zip,
                          person.city,
                          __get_name( person.country ),
                          person.phone,
                          person.fax,
                          person.mobile,
                          person.email,
                          person.website,
                          person.get_current_rank_display(),
                          person.get_gender_display(),
                          str( person.birth ),
                          person.photo,
                          person.text,
                          ] )

    return response

def __get_name( o ):
    if o:
        return o.get_name()
    else:
        return ''
