#-*- coding: utf-8 -*-

from PIL import Image
from datetime import date, datetime
from django import get_version
from django.contrib.admin.models import LogEntry
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
from django.views.i18n import set_language
from twa.members.forms import LoginForm
from twa.members.models import Association, Country, Document, Dojo, Download, Graduation, License, LicenseManager, Person, PersonManager, RANK, TWAMembership, News
from twa.requests.models import Request
from twa.settings import LOGIN_REDIRECT_URL, LANGUAGES, LANGUAGE_CODE, SEND_MAIL_ON_LOGIN
import os, platform, sys

try:
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute( "SELECT version()" )
    version = cursor.fetchone()[0]
    if version.lower().startswith( 'postgresql' ):
        db_version = version[:version.find( ' ', 12 )]
        db_link = 'http://www.postgresql.org/'
    else:
        db_version = 'MySQL %s' % version
        db_link = 'http://www.mysql.de/'
except:
    db_version = ''
    db_link = ''

def __get_rank_display( rank ):
    for id, name in RANK:
        if id == rank:
            return name
    return ''

def set_lang( request, code = LANGUAGE_CODE ):
    if code in dict( LANGUAGES ).keys():
        request.session['django_language'] = code
    return set_language( request )

def get_context( request ):
    ua = request.META['HTTP_USER_AGENT']
    if ua.find( 'dummy connection' ) == - 1:
        r = Request( user = request.user.username )
        r.user_agent = ua
        r.remote = request.META['REMOTE_ADDR']
        r.path = request.get_full_path()
        r.save()

    ctx = {}
    ctx['LANGUAGES'] = LANGUAGES
    ctx['language'] = request.LANGUAGE_CODE

    return ctx

def twa_login( request ):
    ctx = get_context( request )
    ctx['menu'] = 'login'
    ctx['include_main_image'] = True
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
                msg = '%s: %s hat sich eingeloggt.\n\n' % ( datetime.now(), name )
                msg += 'User agent:\n%s\n\n' % request.META['HTTP_USER_AGENT']
                msg += 'Remote Address:\n%s\n\n' % request.META['REMOTE_ADDR']
                msg += '\nhttps://www.tendo-world-aikido.de/\n'

                mail_admins( 'Login %s' % name, msg, fail_silently = True )

            next = request.REQUEST.get( 'next', LOGIN_REDIRECT_URL )

            return redirect_to( request, next )
    else:
        form = LoginForm()

    ctx['form'] = form
    return render_to_response( 
               'twa-login.html',
               ctx,
            )

def twa_logout( request ):
    ctx = get_context( request )
    ctx['menu'] = 'logout'
    logout( request )
    return redirect_to( request, '/' )

@login_required
def info( request ):
    now = datetime.now()

    ctx = get_context( request )
    ctx['menu'] = 'info'

    ctx['db_version'] = db_version
    ctx['db_link'] = db_link
    try:
        ctx['os_version'] = open( '/etc/issue.net', 'r' ).read().strip()
    except:
        pass
    ctx['os_link'] = 'http://www.ubuntu.com/'
    ctx['django_version'] = get_version()
    ctx['django_link'] = 'http://www.djangoproject.com/'
    ctx['python_version'] = sys.version
    ctx['python_link'] = 'http://www.python.org/'
    ctx['users'] = User.objects.all().order_by( '-last_login' )
    ctx['active_sessions'] = Session.objects.filter( expire_date__gte = now ).order_by( 'expire_date' )
    ctx['expired_sessions'] = Session.objects.filter( expire_date__lt = now ).order_by( '-expire_date' )
    ctx['agents'] = Request.objects.get_user_agents_by_requests()
    ctx['hits'] = Request.objects.all().count()

    if request.user.is_authenticated():
        ctx['logentries'] = LogEntry.objects.all().order_by( '-action_time' )[:20]
    else:
        ctx['logentries'] = LogEntry.objects.none()

    return direct_to_template( request,
        template = 'info.html',
        extra_context = ctx,
    )

def public( request ):
    ctx = get_context( request )
    ctx['news'] = News.current_objects.all()[:3]
    ctx['include_main_image'] = True

    if request.user.is_authenticated():
        ctx['birthdays'] = Person.persons.get_next_birthdays()

    return direct_to_template( request,
        template = 'twa-index.html',
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

    today = date.today()
    ctx = get_context( request )
    ctx['menu'] = 'home'
    if request.user.is_authenticated():
        ctx['requested_licenses'] = License.objects.get_requested_licenses().count()
        ctx['membership_requests'] = Person.persons.get_by_requested_membership().count()
        ctx['countries'] = Country.objects.all().count()
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

@login_required
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
            qs = Dojo.dojos.filter( Q( name__icontains = s ) | 
                    Q( shortname__icontains = s ) | 
                    Q( text__icontains = s ) | 
                    Q( street__icontains = s ) | 
                    Q( zip__icontains = s ) | 
                    Q( city__icontains = s ) )
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

@login_required
def dojos2( request ):
    ctx = get_context( request )
    ctx['menu'] = 'dojos'

    countries = []
    for d in Dojo.dojos.values( 'country' ).order_by( 'country' ).distinct():
        countries.append( ( str( d['country'] ), Country.objects.get( id = d['country'] ).get_name() ) )
    ctx['counties'] = countries
    ctx['cities'] = Dojo.dojos.values( 'city' ).order_by( 'city' ).distinct()

    if request.REQUEST.has_key( 's' ):
        s = request.REQUEST['s']
        ctx['search'] = s
        if s:
            qs = Dojo.dojos.filter( Q( name__icontains = s ) | 
                    Q( shortname__icontains = s ) | 
                    Q( text__icontains = s ) | 
                    Q( country__name__icontains = s ) | 
                    Q( country__name_de__icontains = s ) | 
                    Q( country__name_ja__icontains = s ) | 
                    Q( street__icontains = s ) | 
                    Q( zip__icontains = s ) | 
                    Q( city__icontains = s ) )
        else:
            qs = Dojo.dojos.all()
    else:
        qs = Dojo.dojos.all()

    if request.REQUEST.has_key( 'sid' ):
        sid = request.REQUEST['sid']
        ctx['searchid'] = sid
        if sid:
            qs &= Dojo.dojos.filter( Q( id__icontains = sid ) )

    ctx['counter'] = qs.count()

    return object_list( 
        request,
        queryset = qs,
        paginate_by = 100,
        extra_context = ctx,
        template_name = "twa-dojos.html",
    )

@login_required
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

@login_required
def dojo2( request, did = None ):
    ctx = get_context( request )
    ctx['menu'] = 'dojos'
    ctx['members'] = Person.persons.filter( dojos__id = did )
    return object_detail( 
        request,
        queryset = Dojo.dojos.filter( id = did ),
        object_id = did,
        template_object_name = 'dojo',
        extra_context = ctx,
        template_name = "twa-dojo.html",
    )

@login_required
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
        template_name = "twa-associations.html",
    )

@login_required
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
        template_name = "twa-association.html",
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
            qs &= Person.persons.get_members()
        elif member == 'requested':
            qs &= Person.persons.get_by_requested_membership()
        else:
            qs &= Person.persons.all()

    if request.REQUEST.has_key( 's' ):
        s = request.REQUEST['s']
        ctx['search'] = s
        if s:
            qs &= Person.persons.filter( Q( firstname__icontains = s ) | 
                    Q( nickname__icontains = s ) | 
                    Q( lastname__icontains = s ) | 
                    Q( text__icontains = s ) | 
                    Q( email__icontains = s ) | 
                    Q( street__icontains = s ) | 
                    Q( zip__icontains = s ) | 
                    Q( city__icontains = s ) )

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
def members_all( request ):
    ctx, qs = __get_members( request )
    ctx['menu'] = 'members'
    ctx['counter'] = qs.count()

    return object_list( 
        request,
        queryset = qs,
        paginate_by = 500,
        extra_context = ctx,
        template_name = "twa-members-all.html",
    )


@login_required
def members2( request ):
    ctx, qs = __get_members( request )
    ctx['menu'] = 'members'
    ctx['counter'] = qs.count()

    return object_list( 
        request,
        queryset = qs,
        paginate_by = 50,
        extra_context = ctx,
        template_name = "twa-members.html",
    )

@login_required
def __get_members( request ):
    ctx = get_context( request )
    qs = None

    if request.REQUEST.has_key( 's' ):
        s = request.REQUEST['s']
        ctx['search'] = s
        if s:
            qs = Person.persons.filter( Q( firstname__icontains = s ) | 
                    Q( nickname__icontains = s ) | 
                    Q( lastname__icontains = s ) | 
                    Q( text__icontains = s ) | 
                    Q( email__icontains = s ) | 
                    Q( street__icontains = s ) | 
                    Q( zip__icontains = s ) | 
                    Q( city__icontains = s ) )

    if request.REQUEST.has_key( 'sid' ):
        sid = request.REQUEST['sid']
        ctx['searchid'] = sid
        if sid:
            qs = Person.persons.filter( Q( id__exact = sid ) )

    if qs is None:
        qs = Person.persons.all()

    return ( ctx, qs )

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
def member2( request, mid = None ):
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
        template_name = 'twa-member.html',
        extra_context = ctx,
    )

@login_required
def member_requests( request ):
    ctx = get_context( request )
    ctx['menu'] = 'member-requests'

    qs = TWAMembership.objects.get_requested_memberships().order_by( '-id' )
    ctx['counter'] = qs.count()

    return object_list( 
        request,
        queryset = qs,
        paginate_by = 50,
        extra_context = ctx,
        template_name = 'members/member_requests_list.html',
    )

@login_required
def member_requests2( request ):
    ctx = get_context( request )
    ctx['menu'] = 'member-requests'

    qs = TWAMembership.objects.get_requested_memberships().order_by( '-id' )
    ctx['counter'] = qs.count()

    return object_list( 
        request,
        queryset = qs,
        paginate_by = 50,
        extra_context = ctx,
        template_name = 'twa-member-requests.html',
    )

@login_required
def licenses( request ):
    ctx = get_context( request )
    ctx['menu'] = 'licenses'

    qs = License.objects.get_granted_licenses()#.select_related().order_by( 'members_person.firstname', 'members_person.lastname' )
    ctx['counter'] = qs.count()

    return object_list( 
        request,
        queryset = qs,
        paginate_by = 50,
        extra_context = ctx,
    )

@login_required
def licenses2( request ):
    ctx = get_context( request )
    ctx['menu'] = 'licenses'

    qs = License.objects.get_granted_licenses()#.select_related().order_by( 'members_person.firstname', 'members_person.lastname' )
    ctx['counter'] = qs.count()

    return object_list( 
        request,
        queryset = qs,
        paginate_by = 100,
        extra_context = ctx,
        template_name = 'twa-licenses.html',
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
def license_requests2( request ):
    ctx = get_context( request )
    ctx['menu'] = 'license-requests'

    qs = License.objects.get_requested_licenses().order_by( '-id' )
    ctx['counter'] = qs.count()

    return object_list( 
        request,
        queryset = qs,
        paginate_by = 50,
        extra_context = ctx,
        template_name = 'twa-license-requests.html',
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

@login_required
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
def graduations2( request ):
    ctx = get_context( request )
    ctx['menu'] = 'graduations'

    qs = Graduation.graduations.get_this_years_graduations().select_related().order_by( '-date', '-rank', 'members_person.firstname', 'members_person.lastname' )
    ctx['counter'] = qs.count()

    return object_list( 
        request,
        queryset = qs,
        paginate_by = 100,
        extra_context = ctx,
        template_name = 'twa-graduations.html',
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
def suggestions2( request ):
    ctx = get_context( request )
    ctx['menu'] = 'suggestions'

    qs = Graduation.suggestions.select_related().order_by( '-date', '-rank', 'members_person.firstname', 'members_person.lastname' )
    ctx['counter'] = qs.count()

    return object_list( 
        request,
        queryset = qs,
        paginate_by = 50,
        extra_context = ctx,
        template_name = 'twa-suggestions.html',
    )

@login_required
def dojos_csv( request ):
    ctx = get_context( request )
    response = HttpResponse( mimetype = 'text/csv' )
    response['Content-Disposition'] = 'attachment; filename=dojos.csv'

    from csvutf8 import UnicodeWriter
    writer = UnicodeWriter( response )

    writer.writerow( ['id', 'name', 'street', 'zip', 'city', 'country'] )

    for d in Dojo.dojos.all():
        writer.writerow( [str( d.id ), d.name, d.street, d.zip, d.city, d.country.get_name()] )

    return response

@login_required
def members_xls( request ):
    ctx = get_context( request )
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
    response = HttpResponse( open( 'tmp/' + filename, 'r' ).read(), mimetype = 'application/ms-excel' )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response

@login_required
def licenses_xls( request ):
    ctx = get_context( request )
    import pyExcelerator as xl

    workbook = xl.Workbook()
    sheet = workbook.add_sheet( 'Lizenz Anträge' )
    header_font = xl.Font()
    header_font.bold = True

    header_style = xl.XFStyle()
    header_style.font = header_font

    for y, header in enumerate( ['LID', 'STATUS', 'VORNAME', 'NACHNAME', 'ORT', 'GRAD', 'ANTRAG', 'ZAHLUNG', 'TEXT'] ):
        sheet.write( 0, y, header, header_style )

    for x, license in enumerate( License.objects.get_granted_licenses().order_by( '-id' ) ):
        person = license.person
        content = [str( license.id ), license.get_status_display(), person.firstname, person.lastname, person.city, str( person.current_rank() ), __get_date( license.request ), __get_date( license.receipt ), license.text]
        col = 0
        for y, content in enumerate( content ):
            sheet.write( x + 1, y, content )

    filename = 'license-requests-%s.xls' % datetime.now().strftime( '%Y%m%d-%H%M%S' )
    workbook.save( 'tmp/' + filename )
    response = HttpResponse( open( 'tmp/' + filename, 'r' ).read(), mimetype = 'application/ms-excel' )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response

@login_required
def license_requests_xls( request ):
    ctx = get_context( request )
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
        content = [str( license.id ), license.get_status_display(), person.firstname, person.lastname, person.city, str( person.current_rank() ), __get_date( license.request ), __get_date( license.receipt ), license.text]
        col = 0
        for y, content in enumerate( content ):
            sheet.write( x + 1, y, content )

    filename = 'license-requests-%s.xls' % datetime.now().strftime( '%Y%m%d-%H%M%S' )
    workbook.save( 'tmp/' + filename )
    response = HttpResponse( open( 'tmp/' + filename, 'r' ).read(), mimetype = 'application/ms-excel' )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response

@login_required
def membership_requests_xls( request ):
    ctx = get_context( request )
    import pyExcelerator as xl

    workbook = xl.Workbook()
    sheet = workbook.add_sheet( 'TWA Anträge' )
    header_font = xl.Font()
    header_font.bold = True

    header_style = xl.XFStyle()
    header_style.font = header_font

    for y, header in enumerate( ['REQUEST-ID', 'TWA-ID', 'VORNAME', 'NACHNAME', 'ORT', 'GRAD', 'ANTRAG'] ):
        sheet.write( 0, y, header, header_style )

    for x, membership in enumerate( TWAMembership.objects.get_requested_memberships().select_related().order_by( '-id' ) ):
        person = membership.person
        content = [str( membership.id ), membership.twa_id(), person.firstname, person.lastname, person.city, str( person.current_rank() ), __get_date( membership.request )]
        col = 0
        for y, content in enumerate( content ):
            sheet.write( x + 1, y, content )

    filename = 'membership-%s.xls' % datetime.now().strftime( '%Y%m%d-%H%M%S' )
    workbook.save( 'tmp/' + filename )
    response = HttpResponse( open( 'tmp/' + filename, 'r' ).read(), mimetype = 'application/ms-excel' )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response

@login_required
def nominations_xls( request ):
    ctx = get_context( request )
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
    response = HttpResponse( open( 'tmp/' + filename, 'r' ).read(), mimetype = 'application/ms-excel' )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response

@login_required
def members_csv( request ):
    ctx = get_context( request )
    response = HttpResponse( mimetype = 'text/csv' )
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
    if p and p.current_rank():
        return str( p.current_rank() )
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
        return unicode( ' '.join( o.splitlines() ) )
    
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
        head, tail = os.path.split( fileobject.path )
        return tail
    except:
        return ''

def news( request, nid = None ):
    ctx = get_context( request )
    ctx['menu'] = 'news'
    ctx['include_main_image'] = True

    return object_detail( 
        request,
        queryset = News.current_objects.filter( id = nid ),
        object_id = nid,
        template_object_name = 'news',
        template_name = 'twa-news.html',
        extra_context = ctx,
    )

def news_archive( request ):
    ctx = get_context( request )
    ctx['menu'] = 'news'
    ctx['include_main_image'] = True

    return object_list( 
        request,
        queryset = News.current_objects.all(),
        paginate_by = 50,
        extra_context = ctx,
        template_name = 'twa-news-archive.html',
    )

def downloads( request ):
    ctx = get_context( request )
    ctx['menu'] = 'downloads'
    ctx['include_main_image'] = True

    return object_list( 
        request,
        queryset = Download.public_objects.all(),
        paginate_by = 50,
        extra_context = ctx,
        template_name = 'twa-downloads.html',
    )
