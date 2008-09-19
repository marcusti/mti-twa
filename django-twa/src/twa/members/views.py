#-*- coding: utf-8 -*-

from PIL import Image
from datetime import date, datetime
from django import get_version
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.sessions.models import Session
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.simple import direct_to_template, redirect_to
from twa.members.forms import LoginForm
from twa.members.models import Association, Country, Document, Dojo, Graduation, License, LicenseManager, Person, PersonManager, RANK
from twa.requests.models import Request, RequestManager
from twa.settings import LOGIN_REDIRECT_URL, LANGUAGES, SEND_MAIL_ON_LOGIN
import os, platform, sys

def __get_rank_display( rank ):
    for id, name in RANK:
        if id == rank:
            return name
    return ''

def get_context( request ):
    ua = request.META['HTTP_USER_AGENT']
    if ua.find( 'dummy connection' ) == -1:
        r = Request( user = request.user )
        r.user_agent = ua
        r.remote = request.META['REMOTE_ADDR']
        r.path = request.get_full_path()
        r.save()

    my_context = {}
    my_context['LANGUAGES'] = LANGUAGES
    my_context['language'] = request.LANGUAGE_CODE
    return my_context

def twa_login( request ):
    ctx = get_context( request )
    ctx['menu'] = 'login'
    ctx['next'] = request.GET.get( 'next', LOGIN_REDIRECT_URL )

    if request.method == 'POST':
        form = LoginForm( request.POST )
        if form.is_valid():
            # user authentication is done in LoginForm validation
            user = form.get_user()
            login( request, user )

            #send mail
            if SEND_MAIL_ON_LOGIN and not user.is_superuser:
                from django.core.mail import mail_admins, send_mail
                name = user.get_full_name()
                msg = '%s: %s hat sich eingeloggt.\n' % ( datetime.now(), name )
                msg += 'https://marcusti.dyndns.org/'
                mail_admins( 'Login', msg, fail_silently = True )

            next = request.REQUEST.get( 'next', LOGIN_REDIRECT_URL )
#            if request.REQUEST.has_key( 'next' ):
#                next = request.REQUEST['next']
#            else:
#                next = LOGIN_REDIRECT_URL

            return redirect_to( request, next )
    else:
        form = LoginForm()

    ctx['form'] = form
    return render_to_response(
               'members/login.html',
               ctx,
            )

def twa_logout( request ):
    ctx = get_context( request )
    ctx['menu'] = 'logout'
    logout( request )
    return redirect_to( request, '/login/' )

@login_required
def info( request ):
    now = datetime.now()

    if request.user.is_authenticated() and request.user.is_superuser:
        if request.POST.has_key( 'clean_up_expired_sessions' ):
            Session.objects.filter( expire_date__lt = now ).delete()
            transaction.commit_unless_managed()

    ctx = get_context( request )
    ctx['menu'] = 'info'
    try:
        from django import db
        ctx['mysql_version'] = '%s %s' % ( db.settings.DATABASE_ENGINE, db.backend.Database.get_client_info() )
    except:
        pass
    ctx['django_version'] = get_version()
    ctx['python_version'] = sys.version
    ctx['os_version'] = platform.platform()
    ctx['users'] = User.objects.all().order_by( '-last_login' )
    ctx['active_sessions'] = Session.objects.filter( expire_date__gte = now ).order_by( 'expire_date' )
    ctx['expired_sessions'] = Session.objects.filter( expire_date__lt = now ).order_by( '-expire_date' )
    ctx['requests'] = Request.objects.all().order_by( '-id' )[:200]
    ctx['agents'] = Request.objects.get_user_agents_by_requests()
    ctx['hits'] = Request.objects.all().count()

    return direct_to_template( request,
        template = 'info.html',
        extra_context = ctx,
    )

def index( request ):
    #if License.ocjects.all().count() == 0:
    #    for person in Person.persons.filter( twa_license_requested__isnull = False, twa_license__isnull = True ).order_by( 'twa_license_requested', 'lastname' ):
    #        l = License()
    #        l.person = person
    #        l.request = person.twa_license_requested
    #        l.receipt = person.twa_license_receipt
    #        for doc in Document.objects.filter( person__id = person.id ):
    #            l.request_doc = doc.file
    #        l.save()

    #for person in Person.objects.all():
    #    if person.country_id is None:
    #        person.country_id = 1
    #        person.save()

    today = date.today()
    ctx = get_context( request )
    ctx['menu'] = 'home'
    if request.user.is_authenticated():
        ctx['requested_licenses'] = License.objects.get_requested_licenses().count()
        ctx['membership_requests'] = Person.persons.get_by_requested_membership().count()
        ctx['associations'] = Association.objects.all().count()
        ctx['dojos'] = Dojo.dojos.count()
        ctx['members'] = Person.persons.count()
        ctx['licenses'] = License.objects.get_granted_licenses().count()
        ctx['graduations'] = Graduation.graduations.get_this_years_graduations().count()
        ctx['suggestions'] = Graduation.suggestions.count()
        ctx['birthdays'] = Person.persons.get_next_birthdays()
    return direct_to_template( request,
        template = 'base.html',
        extra_context = ctx,
    )

def dojos( request ):
    ctx = get_context( request )
    ctx['menu'] = 'dojos'

    countries = []
    for d in Dojo.dojos.values( 'country' ).order_by( 'country' ).distinct():
        countries.append( ( str( d['country'] ), Country.objects.get( id = d['country'] ).get_name() ) )
    ctx['counties'] = countries

    if request.REQUEST.has_key( 's' ):
        s = request.REQUEST['s']
        ctx['search'] = s
        if s:
            qs = Dojo.dojos.filter( Q( name__icontains=s ) |
                    Q( shortname__icontains=s ) |
                    Q( text__icontains=s ) |
                    Q( street__icontains=s ) |
                    Q( zip__icontains=s ) |
                    Q( city__icontains=s ) )
        else:
            qs = Dojo.dojos.all()
    else:
        qs = Dojo.dojos.all()

    if request.REQUEST.has_key( 'sid' ):
        sid = request.REQUEST['sid']
        ctx['searchid'] = sid
        if sid:
            qs &= Dojo.dojos.filter( Q( id__icontains = sid ) )

    ctx['cities'] = Dojo.dojos.values( 'city' ).order_by( 'city' ).distinct()
    if request.REQUEST.has_key( 'ci' ):
        city = request.REQUEST['ci']
        ctx['ci'] = city
        if city <> 'all':
            qs &= Dojo.dojos.filter( city = city )

    if request.REQUEST.has_key( 'co' ):
        co = request.REQUEST['co']
        ctx['co'] = co
        if co <> 'all':
            ctx['cities'] = Dojo.dojos.values( 'city' ).filter( country = co ).order_by( 'city' ).distinct()
            qs &= Dojo.dojos.filter( country = co )
        else:
            ctx['cities'] = Dojo.dojos.values( 'city' ).order_by( 'city' ).distinct()

    ctx['counter'] = qs.count()

    return object_list(
        request,
        queryset = qs,
        paginate_by = 50,
        extra_context = ctx,
    )

def dojo( request, did = None ):
    ctx = get_context( request )
    ctx['menu'] = 'dojos'
    ctx['members'] = Person.persons.filter( dojos__id = did )
    return object_detail(
        request,
        queryset = Dojo.dojos.filter( id = did ),
        object_id = did,
        template_object_name = 'dojo',
        extra_context = ctx,
    )

def associations( request ):
    ctx = get_context( request )
    ctx['menu'] = 'associations'

    qs = Association.objects.all()
    ctx['counter'] = qs.count()

    return object_list(
        request,
        queryset = qs,
        paginate_by = 50,
        extra_context = ctx,
    )

def association( request, aid = None ):
    ctx = get_context( request )
    ctx['menu'] = 'associations'

    qs = Association.objects.all()
    ctx['counter'] = qs.count()

    return object_detail(
        request,
        queryset = Association.objects.filter( id = aid ),
        object_id = aid,
        template_object_name = 'association',
        extra_context = ctx,
    )

@login_required
def members( request ):
    ctx = get_context( request )
    ctx['menu'] = 'members'

    if request.REQUEST.has_key( 'l' ):
        license = request.REQUEST['l']
        ctx['l'] = license
        if license == 'yes':
            qs = Person.persons.get_licensed()
        elif license == 'requested':
            qs = Person.persons.get_by_requested_licenses()
        else:
            qs = Person.persons.all()
    else:
        qs = Person.persons.all()

    if request.REQUEST.has_key( 'm' ):
        member = request.REQUEST['m']
        ctx['m'] = member
        if member == 'yes':
            qs &= Person.persons.filter( twa_membership__isnull = False )
        elif member == 'requested':
            qs &= Person.persons.filter( twa_membership_requested__isnull = False )
        else:
            qs &= Person.persons.all()

    if request.REQUEST.has_key( 's' ):
        s = request.REQUEST['s']
        ctx['search'] = s
        if s:
            qs &= Person.persons.filter( Q( firstname__icontains=s ) |
                    Q( nickname__icontains=s ) |
                    Q( lastname__icontains=s ) |
                    Q( text__icontains=s ) |
                    Q( email__icontains=s ) |
                    Q( street__icontains=s ) |
                    Q( zip__icontains=s ) |
                    Q( city__icontains=s ) )

    if request.REQUEST.has_key( 'sid' ):
        sid = request.REQUEST['sid']
        ctx['searchid'] = sid
        if sid:
            qs &= Person.persons.filter( Q( id__exact = sid ) )

    ranks = []
    for r in Graduation.graduations.values( 'rank' ).distinct():
        ranks.append( ( str( r['rank'] ), __get_rank_display( r['rank'] ) ) )
    ctx['ranks'] = ranks

    if request.REQUEST.has_key( 'r' ):
        rank = request.REQUEST['r']
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
    ctx['menu'] = 'members'
    ctx['dojos'] = Dojo.dojos.filter( person__id = mid )
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
def member_requests( request ):
    ctx = get_context( request )
    ctx['menu'] = 'member-requests'

    qs = Person.persons.get_by_requested_membership().order_by( '-id' )
    ctx['counter'] = qs.count()

    return object_list(
        request,
        queryset = qs,
        paginate_by = 50,
        extra_context = ctx,
        template_name = 'members/member_requests_list.html',
    )

@login_required
def licenses( request ):
    ctx = get_context( request )
    ctx['menu'] = 'licenses'

    qs = License.objects.get_granted_licenses().select_related().order_by( 'members_person.firstname', 'members_person.lastname' )
    ctx['counter'] = qs.count()

    return object_list(
        request,
        queryset = qs,
        paginate_by = 50,
        extra_context = ctx,
    )

@login_required
def license_requests( request ):
    ctx = get_context( request )
    ctx['menu'] = 'license-requests'

    qs = License.objects.get_requested_licenses().order_by( '-id' )
    ctx['counter'] = qs.count()

    return object_list(
        request,
        queryset = qs,
        paginate_by = 50,
        extra_context = ctx,
        template_name = 'members/license_requests_list.html',
    )

@login_required
def license_rejected( request ):
    ctx = get_context( request )
    ctx['menu'] = 'license-rejected'

    qs = License.objects.get_rejected_licenses().order_by( '-id' )
    ctx['counter'] = qs.count()

    return object_list(
        request,
        queryset = qs,
        paginate_by = 50,
        extra_context = ctx,
        template_name = 'members/license_requests_list.html',
    )

def graduations( request ):
    ctx = get_context( request )
    ctx['menu'] = 'graduations'

    qs = Graduation.graduations.get_this_years_graduations().select_related().order_by( '-date', '-rank', 'members_person.firstname', 'members_person.lastname' )
    ctx['counter'] = qs.count()

    return object_list(
        request,
        queryset = qs,
        paginate_by = 100,
        extra_context = ctx,
    )

@login_required
def suggestions( request ):
    ctx = get_context( request )
    ctx['menu'] = 'suggestions'

    qs = Graduation.suggestions.select_related().order_by( '-date', '-rank', 'members_person.firstname', 'members_person.lastname' )
    ctx['counter'] = qs.count()

    return object_list(
        request,
        queryset = qs,
        paginate_by = 50,
        extra_context = ctx,
        template_name = 'members/graduation_suggestion_list.html',
    )

@login_required
def dojos_csv( request ):
    response = HttpResponse( mimetype='text/csv' )
    response['Content-Disposition'] = 'attachment; filename=dojos.csv'

    from csvutf8 import UnicodeWriter
    writer = UnicodeWriter( response )

    writer.writerow( ['id', 'name', 'street', 'zip', 'city', 'country'] )

    for d in Dojo.dojos.all():
        writer.writerow( [str( d.id ), d.name, d.street, d.zip, d.city, d.country.get_name()] )

    return response

@login_required
def members_xls( request ):
    import pyExcelerator as xl

    workbook = xl.Workbook()
    sheet = workbook.add_sheet( 'Members' )
    header_font = xl.Font()
    header_font.bold = True

    header_style = xl.XFStyle()
    header_style.font = header_font

    for y, header in enumerate( __get_export_headers() ):
        sheet.write( 0, y, header, header_style )

    for x, person in enumerate( Person.persons.all().order_by( 'firstname', 'lastname' ) ):
        col = 0
        for y, content in enumerate( __get_export_content( person ) ):
            sheet.write( x + 1, y, content )
            col = y
#        if person.thumbnail:
#            file, ext = os.path.splitext( person.get_thumbnail_filename() )
#            bmp_name = file + '.bmp'
#            img = Image.open( person.get_thumbnail_filename() )
#            img.convert( 'RGB' )
#            img.save( bmp_name )
#            try:
#                sheet.insert_bitmap( bmp_name, x + 1, col + 1 )
#            except:
#                pass


    filename = 'members-%s.xls' % datetime.now().strftime( '%Y%m%d-%H%M%S' )
    workbook.save( 'tmp/' + filename )
    response = HttpResponse( open( 'tmp/' + filename, 'r' ).read(), mimetype='application/ms-excel' )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response

@login_required
def license_requests_xls( request ):
    import pyExcelerator as xl

    workbook = xl.Workbook()
    sheet = workbook.add_sheet( 'Lizenz Anträge' )
    header_font = xl.Font()
    header_font.bold = True

    header_style = xl.XFStyle()
    header_style.font = header_font

    for y, header in enumerate( ['LID', 'STATUS', 'VORNAME', 'NACHNAME', 'ORT', 'GRAD', 'ANTRAG', 'ZAHLUNG', 'TEXT'] ):
        sheet.write( 0, y, header, header_style )

    for x, license in enumerate( License.objects.get_requested_licenses().order_by( '-id' ) ):
        person = license.person
        content = [str( license.id ), license.get_status_display(), person.firstname, person.lastname, person.city, person.get_current_rank_display(), __get_date( license.request ), __get_date( license.receipt ), license.text]
        col = 0
        for y, content in enumerate( content ):
            sheet.write( x + 1, y, content )

    filename = 'license-requests-%s.xls' % datetime.now().strftime( '%Y%m%d-%H%M%S' )
    workbook.save( 'tmp/' + filename )
    response = HttpResponse( open( 'tmp/' + filename, 'r' ).read(), mimetype='application/ms-excel' )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response

@login_required
def licenses_xls( request ):
    import pyExcelerator as xl

    workbook = xl.Workbook()
    sheet = workbook.add_sheet( 'Lizenzen' )
    header_font = xl.Font()
    header_font.bold = True

    header_style = xl.XFStyle()
    header_style.font = header_font

    for y, header in enumerate( ['LID', 'VORNAME', 'NACHNAME', 'ORT', 'GRAD', 'LIZENZ', 'ANTRAG', 'BELEG'] ):
        sheet.write( 0, y, header, header_style )

    for x, license in enumerate( License.objects.get_granted_licenses().select_related().order_by( 'members_person.firstname', 'members_person.lastname' ) ):
        person = license.person
        content = [str( license.id ), person.firstname, person.lastname, person.city, person.get_current_rank_display(), __get_date( license.date ), __get_date( license.request ), __get_date( license.receipt )]
        col = 0
        for y, content in enumerate( content ):
            sheet.write( x + 1, y, content )

    filename = 'licenses-%s.xls' % datetime.now().strftime( '%Y%m%d-%H%M%S' )
    workbook.save( 'tmp/' + filename )
    response = HttpResponse( open( 'tmp/' + filename, 'r' ).read(), mimetype='application/ms-excel' )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response

@login_required
def nominations_xls( request ):
    import pyExcelerator as xl

    workbook = xl.Workbook()
    sheet = workbook.add_sheet( 'Graduierungen' )
    header_font = xl.Font()
    header_font.bold = True

    header_style = xl.XFStyle()
    header_style.font = header_font

    for y, header in enumerate( ['NR', 'P-ID', 'VORNAME', 'NACHNAME', 'ORT', 'VORSCHLAG', 'DATUM', 'TEXT'] ):
        sheet.write( 0, y, header, header_style )

    for x, grad in enumerate( Graduation.suggestions.all().order_by( '-date', '-rank' ) ):
        person = grad.person
        content = [str( x + 1 ), str( person.id ), person.firstname, person.lastname, person.city, grad.get_rank_display(), __get_date( grad.date ), grad.text]
        col = 0
        for y, content in enumerate( content ):
            sheet.write( x + 1, y, content )

    filename = 'nominations-%s.xls' % datetime.now().strftime( '%Y%m%d-%H%M%S' )
    workbook.save( 'tmp/' + filename )
    response = HttpResponse( open( 'tmp/' + filename, 'r' ).read(), mimetype='application/ms-excel' )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response

@login_required
def members_csv( request ):
    response = HttpResponse( mimetype='text/csv' )
    response['Content-Disposition'] = 'attachment; filename=members.csv'

    from csvutf8 import UnicodeWriter
    writer = UnicodeWriter( response )

    writer.writerow( __get_export_headers() )

    for person in Person.persons.all().order_by( 'id' ):
        writer.writerow( __get_export_content( person ) )

    return response

def __get_export_headers():
    #print Person._meta.fields
    return [
            'ID',
            'FIRSTNAME',
            'LASTNAME',
            'STREET',
            'ZIP',
            'CITY',
            'COUNTRY',
            'PHONE',
            'FAX',
            'MOBILE',
            'EMAIL',
            'WEBSITE',
            'RANK',
            'GENDER',
            'BIRTH',
            'PHOTO',
            'TEXT',
            ]

def __get_export_content( person ):
    return [
            str( person.id ),
            __get_null_safe( person.firstname ),
            __get_null_safe( person.lastname ),
            __get_null_safe( person.street ),
            __get_null_safe( person.zip ),
            __get_null_safe( person.city ),
            __get_name( person.country ),
            __get_null_safe( person.phone ),
            __get_null_safe( person.fax ),
            __get_null_safe( person.mobile ),
            __get_null_safe( person.email ),
            __get_null_safe( person.website ),
            __get_rank( person ),
            __get_gender( person ),
            __get_date( person.birth ),
            __get_path( person.photo ),
            __get_null_safe( person.text ),
            ]

def __get_rank( p ):
    if p and p.current_rank:
        return p.get_current_rank_display()
    else:
        return ''
    
def __get_gender( p ):
    if p and p.gender:
        return p.get_gender_display()
    else:
        return ''
    
def __get_null_safe( o ):
    if o is None:
        return ''
    else:
        return unicode( o )
    
def __get_name( o ):
    if o is not None:
        return o.get_name()
    else:
        return ''

def __get_date( d ):
    if d is not None:
        return str( d )
    else:
        return ''

def __get_path( fileobject ):
    try:
        return fileobject.path
    except:
        return ''
