#-*- coding: utf-8 -*-

from datetime import date
from datetime import datetime
import logging
import mimetypes
import os
import sys

from PIL import Image
from csvutf8 import UnicodeWriter
from django import get_version
from django.contrib.admin.models import LogEntry
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.core.mail import mail_admins
from django.core.mail import send_mass_mail
from django.db import connection
from django.db.models import Q
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.views.generic.list_detail import object_detail
from django.views.generic.list_detail import object_list
from django.views.generic.simple import direct_to_template
from django.views.generic.simple import redirect_to
from django.views.i18n import set_language
import pyExcelerator as xl

from twa.members.forms import LoginForm
from twa.members.models import *
from twa.requests.models import Request
from twa.settings import *


try:
    cursor = connection.cursor()
    cursor.execute("SELECT version()")
    version = cursor.fetchone()[0]
    if version.lower().startswith('postgresql'):
        db_version = version[:version.find(' ', 12)]
        db_link = 'http://www.postgresql.org/'
    else:
        db_version = 'MySQL %s' % version
        db_link = 'http://www.mysql.de/'
except:
    db_version = ''
    db_link = ''


def set_lang(request, code=LANGUAGE_CODE):
    if code in dict(LANGUAGES).keys():
        request.session['django_language'] = code
    return set_language(request)


def get_context(request):
    #try:
    #    ua = request.META['HTTP_USER_AGENT']
    #    if ua.find( 'dummy connection' ) == -1:
    #        r = Request( user = request.user.username )
    #        r.user_agent = ua
    #        r.remote = request.META['REMOTE_ADDR']
    #        r.path = request.get_full_path()
    #        r.save()
    #except:
    #    pass

    ctx = {}
    ctx['LANGUAGES'] = LANGUAGES
    ctx['language'] = request.LANGUAGE_CODE

    return ctx


def twa_login(request):
    ctx = get_context(request)
    ctx['menu'] = 'login'
    ctx['include_main_image'] = True
    ctx['next'] = request.GET.get('next', LOGIN_REDIRECT_URL)

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # user authentication is done in LoginForm validation
            user = form.get_user()
            login(request, user)

            #send mail
            if SEND_MAIL_ON_LOGIN and not user.is_superuser:
                name = user.get_full_name()
                msg = '%s: %s hat sich eingeloggt.\n\n' % (datetime.now(), name)
                msg += 'User agent:\n%s\n\n' % request.META['HTTP_USER_AGENT']
                msg += 'Remote Address:\n%s\n\n' % request.META['REMOTE_ADDR']
                msg += '\nhttp://www.tendo-world-aikido.de/\n'

                mail_admins('Login %s' % name, msg, fail_silently=True)

            next = request.REQUEST.get('next', LOGIN_REDIRECT_URL)

            return redirect_to(request, next)
    else:
        form = LoginForm()

    ctx['form'] = form
    return render_to_response('twa-login.html', ctx)


def twa_logout(request):
    ctx = get_context(request)
    ctx['menu'] = 'logout'
    logout(request)
    return redirect_to(request, '/')


@login_required
def info(request):
    '''Displays technical information.'''

    now = datetime.now()

    ctx = get_context(request)
    ctx['menu'] = 'info'

    ctx['db_version'] = db_version
    ctx['db_link'] = db_link
    ctx['users'] = User.objects.all().order_by('-last_login')
    ctx['agents'] = Request.objects.get_user_agents_top_10()
    try:
        ctx['os_version'] = open('/etc/issue.net', 'r').read().strip()
        ctx['os_link'] = 'http://www.ubuntu.com/'
        ctx['django_version'] = get_version()
        ctx['django_link'] = 'http://www.djangoproject.com/'
        ctx['python_version'] = sys.version.split()[0]
        ctx['python_link'] = 'http://www.python.org/'
        ctx['active_sessions'] = Session.objects.filter(expire_date__gte=now).order_by('expire_date')
        ctx['expired_sessions'] = Session.objects.filter(expire_date__lt=now).order_by('-expire_date')
        ctx['hits'] = Request.objects.all().count()
    except:
        pass

    if request.user.is_authenticated():
        ctx['logentries'] = LogEntry.objects.all().order_by('-action_time')[:20]
    else:
        ctx['logentries'] = LogEntry.objects.none()

    return direct_to_template(request, template='info.html', extra_context=ctx)


def public(request):
    '''Displays the public home page.'''

    ctx = get_context(request)
    ctx['menu'] = 'home'
    ctx['current_news'] = News.current_objects.all()[:5]
    ctx['current_seminars'] = Seminar.public_objects.get_current()
    ctx['include_main_image'] = True

    if request.user.is_authenticated():
        ctx['birthdays'] = Person.persons.get_next_birthdays()

    return direct_to_template(request,
                              template='2011/index.html',
                              extra_context=ctx)


def index(request):
    '''Displays the home page for logged in users.'''

    ctx = get_context(request)
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

    return direct_to_template(request,
                              template='base.html',
                              extra_context=ctx)


@login_required
def dojos(request):
    '''Displays a list of Dojos.'''

    ctx = get_context(request)
    ctx['menu'] = 'dojos'

    countries = []
    for d in Dojo.dojos.values('country').order_by('country').distinct():
        countries.append((str(d['country']), Country.objects.get(id=d['country']).get_name()))
    ctx['counties'] = countries
    ctx['cities'] = Dojo.dojos.values('city').order_by('city').distinct()

    if 's' in request.REQUEST:
        s = request.REQUEST['s']
        ctx['search'] = s
        if s:
            qs = Dojo.dojos.filter(Q(name__icontains=s) |
                                   Q(shortname__icontains=s) |
                                   Q(text__icontains=s) |
                                   Q(country__name__icontains=s) |
                                   Q(country__name_de__icontains=s) |
                                   Q(country__name_ja__icontains=s) |
                                   Q(street__icontains=s) |
                                   Q(zip__icontains=s) |
                                   Q(city__icontains=s))
        else:
            qs = Dojo.dojos.all()
    else:
        qs = Dojo.dojos.all()

    if 'sid' in request.REQUEST:
        sid = request.REQUEST['sid']
        ctx['searchid'] = sid
        if sid:
            qs &= Dojo.dojos.filter(Q(id__icontains=sid))

    ctx['counter'] = qs.count()

    return object_list(request,
                       queryset=qs,
                       paginate_by=100,
                       extra_context=ctx,
                       template_name="twa-dojos.html")


@login_required
def dojo(request, did=None):
    '''Displays a Dojo with it's members.'''

    ctx = get_context(request)
    ctx['menu'] = 'dojos'
    ctx['members'] = Person.persons.filter(dojos__id=did)

    return object_detail(request,
                         queryset=Dojo.dojos.filter(id=did),
                         object_id=did,
                         template_object_name='dojo',
                         extra_context=ctx,
                         template_name="twa-dojo.html")


@login_required
def associations(request):
    '''Displays a list of national associations.'''

    ctx = get_context(request)
    ctx['menu'] = 'associations'

    qs = Association.objects.all()
    ctx['counter'] = qs.count()

    return object_list(request,
                       queryset=qs,
                       paginate_by=50,
                       extra_context=ctx,
                       template_name="twa-associations.html")


@login_required
def association(request, aid=None):
    '''Displays a national association.'''

    ctx = get_context(request)
    ctx['menu'] = 'associations'

    qs = Association.objects.all()
    ctx['counter'] = qs.count()

    return object_detail(request,
                         queryset=Association.objects.filter(id=aid),
                         object_id=aid,
                         template_object_name='association',
                         template_name="twa-association.html",
                         extra_context=ctx)


@login_required
def members_all(request):
    '''Displays a list of all members; no photos; 1000 entries per page.'''

    ctx, qs = __get_members(request)
    ctx['menu'] = 'all members'
    ctx['counter'] = qs.count()

    return object_list(request,
                       queryset=qs,
                       paginate_by=1000,
                       extra_context=ctx,
                       template_name="twa-members-all.html")


@login_required
def members(request):
    '''Displays a list of members; photo thumbnails; 50 entries per page.'''

    ctx, qs = __get_members(request)
    ctx['menu'] = 'members'
    ctx['counter'] = qs.count()

    return object_list(request,
                       queryset=qs,
                       paginate_by=50,
                       extra_context=ctx,
                       template_name="twa-members.html")


@login_required
def __get_members(request):
    '''Returns the default context and a list of members.'''

    ctx = get_context(request)
    qs = Person.persons.all()

    if 's' in request.REQUEST:
        s = request.REQUEST['s']
        ctx['search'] = s
        if s:
            try:
                qs = Person.persons.filter(twamembership__twa_id_number=int(s))
            except:
                qs = Person.persons.filter(
                                           Q(firstname__icontains=s) |
                                           Q(nickname__icontains=s) |
                                           Q(lastname__icontains=s) |
                                           Q(email__icontains=s))

    if 'sort' in request.REQUEST:
        sort = request.REQUEST['sort']
        ctx['search'] = sort
        if sort:
            if sort == 'f':
                qs = qs.order_by('firstname')
            if sort == 'l':
                qs = qs.order_by('lastname')

    if 'sid' in request.REQUEST:
        sid = request.REQUEST['sid']
        ctx['searchid'] = sid
        if sid:
            qs = Person.persons.filter(Q(id__exact=sid))

    if qs is None:
        qs = Person.persons.all()

    return (ctx, qs)


@login_required
def member(request, mid=None):
    '''Displays a member.'''

    ctx = get_context(request)
    ctx['menu'] = 'members'
    ctx['dojos'] = Dojo.dojos.filter(person__id=mid)
    ctx['graduations'] = Graduation.objects.filter(person__id=mid)
    ctx['documents'] = Document.objects.filter(person__id=mid)

    return object_detail(request,
                         queryset=Person.persons.filter(id=mid),
                         object_id=mid,
                         template_object_name='person',
                         template_name='twa-member.html',
                         extra_context=ctx)


@login_required
def member_requests(request, status=None, dojo_id=None, region_id=None, no_payment_filter=False):
    '''Displays a list of member requests.'''

    ctx = get_context(request)
    ctx['menu'] = 'member-requests'

    ctx['dojos'] = Dojo.dojos.filter(person__twamembership__isnull=False).distinct().order_by('city', 'shortname', 'name')
    ctx['regions'] = TWA_REGION

    qs = TWAMembership.objects.get_requested_memberships().order_by('-id')
    if status is not None:
        ctx['filter'] = 'status'
        ctx['filter_value'] = int(status)
        qs = qs.filter(status=status)
    if dojo_id is not None:
        ctx['filter'] = 'dojo'
        ctx['filter_value'] = int(dojo_id)
        qs = qs.filter(person__dojos__id=dojo_id)
    if region_id is not None:
        ctx['filter'] = 'region'
        ctx['filter_value'] = int(region_id)
        qs = qs.filter(person__dojos__twa_region=region_id)
    if no_payment_filter == True:
        ctx['filter'] = 'no_payment'
        qs = qs.filter(twapayment__isnull=True).exclude(status=MEMBERSHIP_STATUS_OPEN)
        qs = qs.exclude(status=MEMBERSHIP_STATUS_ACCEPTED)

    ctx['counter'] = qs.count()
    ctx['queryset'] = qs.exclude(status=MEMBERSHIP_STATUS_OPEN).order_by('person__lastname', 'person__firstname')

    return object_list(request,
                       queryset=qs,
                       paginate_by=50,
                       extra_context=ctx,
                       template_name='twa-member-requests.html')


@login_required
def twa_region(request, region_id=None):
    '''Displays a list of dojos for the selected twa region.'''

    ctx = get_context(request)
    ctx['menu'] = 'twa-region'
    ctx['filter'] = 'region'

    dojos = Dojo.dojos.none()
    if region_id:
        dojos = Dojo.dojos.filter(twa_region=region_id)
        ctx['filter_value'] = int(region_id)
    ctx['dojos'] = dojos
    ctx['regions'] = TWA_REGION

    ctx['counter'] = dojos.count()

    return object_list(request,
                       queryset=dojos,
                       paginate_by=50,
                       extra_context=ctx,
                       template_name='twa-region.html')


def licensees(request):
    '''Displays a public list of licensed twa teachers.'''

    ctx = get_context(request)
    ctx['menu'] = 'licensees'
    qs = License.objects.get_public_licenses()

    l = list(qs)
    l = sorted(l, key=lambda x: x.person.current_rank(), reverse=True)
    l = sorted(l, key=lambda x: x.person.dojos.all()[0].name)
    l = sorted(l, key=lambda x: x.person.dojos.all()[0].city)
    l = sorted(l, key=lambda x: x.person.dojos.all()[0].country.code)

    ctx['object_list'] = l

    return direct_to_template(request,
                              template='twa-licensees-public.html',
                              extra_context=ctx)


@login_required
def licenses(request, twa_status=None, dojo_id=None):
    '''Displays a list of licensed twa teachers for logged in users.'''

    ctx = get_context(request)
    ctx['menu'] = 'licenses'
    ctx['dojos'] = Dojo.dojos.filter(person__license__isnull=False, person__license__status=5).distinct().order_by('city', 'shortname', 'name')

    qs = License.objects.get_granted_licenses()

    if twa_status == True:
        ctx['filter'] = 'twa'
        qs = qs.filter(person__twamembership__isnull=False)

    if twa_status == False:
        ctx['filter'] = 'nontwa'
        qs = qs.filter(person__twamembership__isnull=True)

    if dojo_id is not None:
        ctx['filter'] = 'dojo'
        ctx['filtervalue'] = int(dojo_id)
        qs = qs.filter(person__dojos__id=dojo_id)

    ctx['counter'] = qs.count()

    return object_list(request,
                       queryset=qs,
                       paginate_by=100,
                       extra_context=ctx,
                       template_name='twa-licenses.html')


@login_required
def license_requests(request):
    '''Displays a list of applications for twa license.'''

    ctx = get_context(request)
    ctx['menu'] = 'license-requests'

    qs = License.objects.get_requested_licenses().order_by('-id')
    ctx['counter'] = qs.count()

    return object_list(request,
                       queryset=qs,
                       paginate_by=50,
                       extra_context=ctx,
                       template_name='twa-license-requests.html')


@login_required
def license_rejected(request):
    '''Displays a list of rejected license applications.'''

    ctx = get_context(request)
    ctx['menu'] = 'license-rejected'

    qs = License.objects.get_rejected_licenses().order_by('-id')
    ctx['counter'] = qs.count()

    return object_list(request,
                       queryset=qs,
                       paginate_by=50,
                       extra_context=ctx,
                       template_name='members/license_requests_list.html')


@login_required
def graduations(request):
    '''Displays a list of graduations.'''

    ctx = get_context(request)
    ctx['menu'] = 'graduations'

    qs = Graduation.graduations.get_this_years_graduations().select_related().order_by('-date', '-rank', 'members_person.firstname', 'members_person.lastname')
    ctx['counter'] = qs.count()

    return object_list(request,
                       queryset=qs,
                       paginate_by=100,
                       extra_context=ctx,
                       template_name='twa-graduations.html')


@login_required
def suggestions(request):
    '''Displays a list of graduation suggestions.'''

    ctx = get_context(request)
    ctx['menu'] = 'suggestions'

    qs = Graduation.suggestions.order_by('-rank', '-date')
    ctx['counter'] = qs.count()

    return object_list(request,
                       queryset=qs,
                       paginate_by=50,
                       extra_context=ctx,
                       template_name='twa-suggestions.html')


@login_required
def dojo_csv(request, dojo_id):
    '''Returns a csv file containing a list of members for this dojo.'''

    dojo = get_object_or_404(Dojo, id=dojo_id)
    payments_first_year = 2009
    current_year = date.today().year

    get_context(request)
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=dojo-%s.csv' % dojo_id

    columns = [
        'DOJO',
        'TWA-ID',
        'FIRSTNAME',
        'LASTNAME',
        'RANK',
        'MEMBER SINCE',
        'PASSPORT DATE'
    ]
    for year in range(payments_first_year, current_year + 1):
        columns.append('PAYMENT %s' % year)

    writer = UnicodeWriter(response)
    writer.writerow(columns)

    people = list(Person.persons.filter(dojos__id=dojo_id))
    people.sort(key=lambda p: p.twa_id())
    for p in people:
        if p.twa_id():
            try:
                membership = p.twamembership_set.filter(is_active=True)[0]
                payments = TWAPayment.objects.filter(public=True, twa__person__id=p.id)

                row = [
                    dojo.name,
                    p.twa_id(),
                    p.firstname,
                    p.lastname,
                    __get_currentrank(p),
                    __get_date(membership.date),
                    __get_date(membership.passport_date),
                ]

                for year in range(payments_first_year, current_year + 1):
                    row.append(__get_twa_payment(payments, year))

                writer.writerow(row)
            except Exception, ex:
                logging.error('error writing person: dojo_id=%s, person=%s, %s' % (dojo_id, p, ex))

    return response


@login_required
def region_csv(request, region_id):
    '''Returns a csv file containing a list of members for this twa region.'''

    dojos = Dojo.dojos.filter(twa_region=region_id).order_by('country__code', 'name')
    payments_first_year = 2009
    current_year = date.today().year

    get_context(request)
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=region-%s.csv' % region_id

    columns = [
        'DOJO',
        'TWA-ID',
        'FIRSTNAME',
        'LASTNAME',
        'RANK',
        'MEMBER SINCE',
        'PASSPORT DATE'
    ]
    for year in range(payments_first_year, current_year + 1):
        columns.append('PAYMENT %s' % year)

    writer = UnicodeWriter(response)
    writer.writerow(columns)

    pids = []
    for dojo in dojos:
        people = Person.persons.filter(dojos__id=dojo.id).order_by('twamembership__twa_id_number')
        for p in people:
            if p.twa_id() and p.id not in pids:
                try:
                    membership = p.twamembership_set.filter(is_active=True)[0]
                    payments = TWAPayment.objects.filter(public=True, twa__person__id=p.id)

                    row = [
                        dojo.name,
                        p.twa_id(),
                        p.firstname,
                        p.lastname,
                        __get_currentrank(p),
                        __get_date(membership.date),
                        __get_date(membership.passport_date),
                    ]

                    for year in range(payments_first_year, current_year + 1):
                        row.append(__get_twa_payment(payments, year))

                    writer.writerow(row)
                    pids.append(p.id)
                except Exception, ex:
                    logging.error('error writing person: dojo_id=%s, person=%s, %s' % (dojo.id, p, ex))

    return response


@login_required
def dojos_csv(request):
    '''Returns a csv file containing a list of dojos.'''

    if not request.user.is_superuser:
        raise Http404

    get_context(request)
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=dojos.csv'

    writer = UnicodeWriter(response)
    writer.writerow(['id', 'name', 'street', 'zip', 'city', 'country'])

    for d in Dojo.dojos.all():
        writer.writerow([str(d.id), d.name, d.street, d.zip, d.city, d.country.get_name()])

    return response


@login_required
def documents_handler(request, filename):
    '''Returns a document for download.'''

    try:
        filepath = os.path.join(DOCUMENTS_DIR, filename)
        mimetype = mimetypes.guess_type(filename)
        response = HttpResponse(open(filepath, 'r').read(), mimetype=mimetype)
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response
    except:
        raise Http404


@login_required
def image_handler(request, filename, size='64x64'):
    '''Returns an image, scaled to the given dimensions.'''

    try:
        filepath = os.path.join(DOCUMENTS_DIR, filename)

        if not os.path.exists(filepath):
            return ''
        # defining the size
        x, y = [int(x) for x in size.split('x')]
        # defining the filename and the miniature filename
        filehead, filetail = os.path.split(filepath)
        basename, format = os.path.splitext(filetail)
        miniature = basename + '_' + size + format
        filename = filepath
        miniature_filename = os.path.join(filehead, miniature)
        if os.path.exists(miniature_filename) and os.path.getmtime(filename) > os.path.getmtime(miniature_filename):
            os.unlink(miniature_filename)
        # if the image wasn't already resized, resize it
        if not os.path.exists(miniature_filename):
            image = Image.open(filename)
            image.thumbnail([x, y], Image.ANTIALIAS)
            try:
                image.save(miniature_filename, image.format, quality=90, optimize=1)
            except:
                image.save(miniature_filename, image.format, quality=90)

        mimetype = mimetypes.guess_type(filename)

        response = HttpResponse(open(miniature_filename, 'r').read(), mimetype=mimetype)

        return response
    except:
        raise Http404


@login_required
def members_xls(request):
    '''Returns an excel sheet including all members.'''

    if not request.user.is_superuser:
        raise Http404

    get_context(request)
    workbook = xl.Workbook()
    sheet = workbook.add_sheet('Members')
    header_font = xl.Font()
    header_font.bold = True

    header_style = xl.XFStyle()
    header_style.font = header_font

    for y, header in enumerate(__get_export_headers()):
        sheet.write(0, y, header, header_style)

    from operator import attrgetter
    people = Person.persons.all().distinct()
    people = sorted(people, key=attrgetter('lastname'))
    people = sorted(people, key=attrgetter('firstname'))
    people = sorted(people, key=lambda p: __get_dojo_name(__get_dojo(p)))
    people = sorted(people, key=lambda p: __get_dojo_city(__get_dojo(p)))
    people = sorted(people, key=lambda p: __get_dojo_country(__get_dojo(p)))

    for x, person in enumerate(people):
        for y, content in enumerate(__get_export_content(person)):
            sheet.write(x + 1, y, content)

    filename = 'members-%s.xls' % datetime.now().strftime('%Y%m%d-%H%M%S')
    filepath = os.path.join(TMP_DIR, filename)
    workbook.save(filepath)
    response = HttpResponse(open(filepath, 'r').read(), mimetype='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response


@login_required
def licenses_xls(request):
    '''Returns an excel sheet including all licensed twa teachers.'''

    if not request.user.is_superuser:
        raise Http404

    get_context(request)
    workbook = xl.Workbook()
    sheet = workbook.add_sheet('Licences')
    header_font = xl.Font()
    header_font.bold = True

    header_style = xl.XFStyle()
    header_style.font = header_font

    for y, header in enumerate(['LID', 'STATUS', 'FIRSTNAME', 'LASTNAME', 'CITY', 'GRADE', 'REQUEST', 'PAYMENT', 'TWA STATUS', 'TEXT']):
        sheet.write(0, y, header, header_style)

    for x, license in enumerate(License.objects.get_granted_licenses().order_by('-id')):
        person = license.person
        content = [str(license.id), license.get_status_display(), person.firstname, person.lastname, person.city, str(person.current_rank()), __get_date(license.request), __get_date(license.receipt), person.twa_status(), license.text]
        for y, content in enumerate(content):
            sheet.write(x + 1, y, content)

    filename = 'license-requests-%s.xls' % datetime.now().strftime('%Y%m%d-%H%M%S')
    filepath = os.path.join(TMP_DIR, filename)
    workbook.save(filepath)
    response = HttpResponse(open(filepath, 'r').read(), mimetype='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response


@login_required
def license_requests_xls(request):
    '''Returns an excel sheet including all requested licenses.'''

    if not request.user.is_superuser:
        raise Http404

    get_context(request)
    workbook = xl.Workbook()
    sheet = workbook.add_sheet('Licences Requests')
    header_font = xl.Font()
    header_font.bold = True

    header_style = xl.XFStyle()
    header_style.font = header_font

    for y, header in enumerate(['LID', 'STATUS', 'FIRSTNAME', 'LASTNAME', 'CITY', 'GRADE', 'REQUEST', 'PAYMENT', 'TEXT']):
        sheet.write(0, y, header, header_style)

    for x, license in enumerate(License.objects.get_requested_licenses().order_by('-id')):
        person = license.person
        content = [str(license.id), license.get_status_display(), person.firstname, person.lastname, person.city, str(person.current_rank()), __get_date(license.request), __get_date(license.receipt), license.text]
        for y, content in enumerate(content):
            sheet.write(x + 1, y, content)

    filename = 'license-requests-%s.xls' % datetime.now().strftime('%Y%m%d-%H%M%S')
    filepath = os.path.join(TMP_DIR, filename)
    workbook.save(filepath)
    response = HttpResponse(open(filepath, 'r').read(), mimetype='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response


@login_required
def membership_requests_xls(request):
    '''Returns an excel sheet including all membership requests.'''

    if not request.user.is_superuser:
        raise Http404

    get_context(request)
    workbook = xl.Workbook()
    sheet = workbook.add_sheet('TWA Requests')
    header_font = xl.Font()
    header_font.bold = True

    header_style = xl.XFStyle()
    header_style.font = header_font

    for y, header in enumerate(['REQUEST-ID', 'STATUS', 'TWA-ID', 'FIRSTNAME', 'LASTNAME', 'EMAIL', 'BIRTH', 'COUNTRY', 'REGION', 'DOJO', 'RANK', 'REQUEST DATE', 'MEMBER SINCE', 'PAYMENT 2009', 'PAYMENT 2010', 'TEXT']):
        sheet.write(0, y, header, header_style)

    for x, membership in enumerate(TWAMembership.objects.get_requested_memberships().select_related().order_by('-id')):
        person = membership.person

        dojo = person.dojos.all()[:1]
        if dojo and len(dojo) > 0:
            cc = dojo[0].country.code
            if dojo[0].twa_region:
                region = dojo[0].get_twa_region_display()
            else:
                region = ''
            dojo = unicode(dojo[0])
        else:
            cc = ''
            region = ''
            dojo = ''

        try:
            payment2009 = TWAPayment.objects.filter(twa=membership, year=2009).latest('date').date
        except:
            payment2009 = None

        try:
            payment2010 = TWAPayment.objects.filter(twa=membership, year=2010).latest('date').date
        except:
            payment2010 = None

        content = [str(membership.id),
            membership.get_status_display(),
            membership.twa_id(),
            person.firstname,
            person.lastname,
            person.email,
            __get_date(person.birth),
            cc,
            region,
            dojo,
            str(person.current_rank()),
            __get_date(membership.request),
            __get_date(membership.date),
            __get_date(payment2009),
            __get_date(payment2010),
            membership.text]

        for y, content in enumerate(content):
            sheet.write(x + 1, y, content)

    filename = 'membership-requests-%s.xls' % datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    filepath = os.path.join(TMP_DIR, filename)
    workbook.save(filepath)
    response = HttpResponse(open(filepath, 'r').read(), mimetype='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response


@login_required
def nominations_xls(request):
    '''Returns an excel sheet including all suggested graduations.'''

    if not request.user.is_superuser:
        raise Http404

    get_context(request)

    workbook = xl.Workbook()
    sheet = workbook.add_sheet('Graduierungen')
    header_font = xl.Font()
    header_font.bold = True

    header_style = xl.XFStyle()
    header_style.font = header_font

    for y, header in enumerate(['NR', 'P-ID', 'VORNAME', 'NACHNAME', 'ORT', 'VORSCHLAG', 'DATUM', 'TEXT']):
        sheet.write(0, y, header, header_style)

    for x, grad in enumerate(Graduation.suggestions.all().order_by('-date', '-rank')):
        person = grad.person
        content = [str(x + 1), str(person.id), person.firstname, person.lastname, person.city, grad.get_rank_display(), __get_date(grad.date), grad.text]

        for y, content in enumerate(content):
            sheet.write(x + 1, y, content)

    filename = 'nominations-%s.xls' % datetime.now().strftime('%Y%m%d-%H%M%S')
    filepath = os.path.join(TMP_DIR, filename)
    workbook.save(filepath)
    response = HttpResponse(open(filepath, 'r').read(), mimetype='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response


@login_required
def members_csv(request):
    '''Returns a csv file including all members.'''

    if not request.user.is_superuser:
        raise Http404

    get_context(request)
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=members.csv'

    writer = UnicodeWriter(response)
    writer.writerow(__get_export_headers())

    people = Person.persons.all().select_related().order_by('firstname', 'lastname')
    for person in people:
        writer.writerow(__get_export_content(person))

    return response


def __get_export_headers():
    #print Person._meta.fields
    return [
        'DB-ID',
        'FIRSTNAME',
        'LASTNAME',
        'NICKNAME',
        'FIRSTNAME_JP',
        'LASTNAME_JP',
        'TITLE',
        'STREET',
        'ZIP',
        'CITY',
        'COUNTRY',
        'PHONE',
        'FAX',
        'MOBILE',
        'EMAIL',
        'DOJO-ID',
        'DOJO COUNTRY',
        'DOJO CITY',
        'DOJO',
        'TENDORYU SINCE',
        '5. KYU',
        '4. KYU',
        '3. KYU',
        '2. KYU',
        '1. KYU',
        '1. DAN',
        '2. DAN',
        '3. DAN',
        '4. DAN',
        '5. DAN',
        '6. DAN',
        'GENDER',
        'BIRTH',
        'PHOTO',
        'TEXT',
        'LICENSE',
        'TWA-ID',
        'TWA REGION',
        'TWA MEMBER SINCE',
        'TWA PASSPORT DATE',
        'TWA PAYMENT 2009',
        'TWA PAYMENT 2010',
        'TWA PAYMENT 2011',
        ]


def __get_export_content(person):
    dojo = __get_dojo(person)
    graduations = person.graduations.filter(is_active=True)
    membership = __get_twa_membership(person)
    try:
        payments = TWAPayment.objects.filter(public=True, twa__person__id=person.id)
    except:
        payments = None
    return [
        str(person.id),
        __get_null_safe(person.firstname),
        __get_null_safe(person.lastname),
        __get_null_safe(person.nickname),
        __get_null_safe(person.firstname_jp),
        __get_null_safe(person.lastname_jp),
        __get_null_safe(person.get_name_prefix_display()),
        __get_null_safe(person.street),
        __get_null_safe(person.zip),
        __get_null_safe(person.city),
        __get_country(person.country),
        __get_null_safe(person.phone),
        __get_null_safe(person.fax),
        __get_null_safe(person.mobile),
        __get_null_safe(person.email),
        __get_dojo_id(dojo),
        __get_dojo_country(dojo),
        __get_dojo_city(dojo),
        __get_dojo_name(dojo),
        __get_date(person.aikido_since),
        __get_rank(graduations, 10),
        __get_rank(graduations, 20),
        __get_rank(graduations, 30),
        __get_rank(graduations, 40),
        __get_rank(graduations, 50),
        __get_rank(graduations, 100),
        __get_rank(graduations, 200),
        __get_rank(graduations, 300),
        __get_rank(graduations, 400),
        __get_rank(graduations, 500),
        __get_rank(graduations, 600),
        __get_gender(person),
        __get_date(person.birth),
        __get_path(person.photo),
        __get_null_safe(person.text),
        __get_license(person),
        person.twa_id(),
        __get_twa_region(dojo),
        __get_twa_member_since(membership),
        __get_twa_passport_date(membership),
        __get_twa_payment(payments, 2009),
        __get_twa_payment(payments, 2010),
        __get_twa_payment(payments, 2011),
        ]


def __get_dojo(p):
    try:
        return p.dojos.all()[0]
    except:
        return None


def __get_dojo_name(dojo):
    if dojo:
        if dojo.name_jp:
            name = "%s %s" % (dojo.name_jp, dojo.name)
        else:
            name = dojo.name
        return unicode(name.strip())
    else:
        return ''


def __get_dojo_country(dojo):
    if dojo:
        return __get_country(dojo.country)
    else:
        return ''


def __get_dojo_city(dojo):
    if dojo:
        return dojo.city
    else:
        return ''


def __get_dojo_id(dojo):
    if dojo:
        return str(dojo.id)
    else:
        return ''


def __get_rank(graduations, rank):
    try:
        return str(graduations.filter(rank=rank).latest('date').date)
    except:
        return ''


def __get_currentrank(p):
    if p and p.current_rank():
        return str(p.current_rank())
    else:
        return ''


def __get_license(p):
    if p and p.is_licensed():
        return __get_date(p.license_set.filter(status=LICENSE_STATUS_LICENSED, is_active=True)[0].date)
    else:
        return ''


def __get_twa_membership(p):
    if p and p.is_member():
        return p.twamembership_set.filter(status=MEMBERSHIP_STATUS_MEMBER, is_active=True)[0]
    else:
        return None


def __get_twa_region(dojo):
    if dojo and dojo.twa_region:
        return dojo.get_twa_region_display()
    else:
        return ''


def __get_twa_member_since(membership):
    if membership:
        return __get_date(membership.date)
    else:
        return ''


def __get_twa_passport_date(membership):
    if membership:
        return __get_date(membership.passport_date)
    else:
        return ''


def __get_twa_payment(payments, year=None):
    if payments and year:
        try:
            return __get_date(payments.filter(year=year).latest('date').date)
        except:
            return ''
    else:
        return ''


def __get_gender(p):
    if p and p.gender:
        return p.gender
    else:
        return ''


def __get_null_safe(o):
    if o is None:
        return ''
    else:
        return unicode(' '.join(o.splitlines()))


def __get_name(o):
    if o is not None:
        return o.get_name()
    else:
        return ''


def __get_country(o):
    if o is not None:
        return o.code
    else:
        return ''


def __get_date(d):
    if d is not None:
        return str(d)
    else:
        return ''


def __get_path(fileobject):
    try:
        head, tail = os.path.split(fileobject.path)
        return tail
    except:
        return ''


@login_required
def news_preview(request, nid=None):
    '''Display a news article.
    If there is a logged in user, a preview of non-published news is shown.
    '''

    ctx = get_context(request)
    ctx['menu'] = 'news'
    ctx['include_main_image'] = False

    return object_detail(request,
                         queryset=News.objects.filter(id=nid),
                         object_id=nid,
                         template_object_name='news',
                         template_name='twa-news.html',
                         extra_context=ctx)


def news(request, nid=None):
    '''Display a public news article.'''
    ctx = get_context(request)
    ctx['menu'] = 'news'
    ctx['detailed'] = True
    ctx['all_news'] = News.current_objects.filter(id=nid)
    return direct_to_template(request,
                              template='2011/news-view.html',
                              extra_context=ctx)

    # ctx = get_context(request)
    # ctx['menu'] = 'news'
    # ctx['include_main_image'] = False

    # return object_detail(request,
    #                      queryset=News.current_objects.filter(id=nid),
    #                      object_id=nid,
    #                      template_object_name='news',
    #                      template_name='twa-news.html',
    #                      extra_context=ctx)


def news_archive(request, year=date.today().year):
    '''Displays the news archive.'''

    ctx = get_context(request)
    ctx['menu'] = 'news'
    ctx['include_main_image'] = False
    ctx['all_news'] = News.current_objects.filter(pub_date__year=year)
    ctx['years'] = reversed(News.current_objects.dates('pub_date', 'year'))
    ctx['year'] = year

    return direct_to_template(request,
                              template='2011/news-archive.html',
                              extra_context=ctx)


def seminar(request, sid=None):
    ctx = get_context(request)
    ctx['menu'] = 'seminars'
    ctx['detailed'] = True
    ctx['seminars'] = Seminar.public_objects.filter(id=sid)
    return direct_to_template(request,
                              template='2011/seminar-view.html',
                              extra_context=ctx)


def seminars_current(request):
    ctx = get_context(request)
    ctx['menu'] = 'seminars'
    ctx['seminars'] = Seminar.public_objects.get_current()
    return direct_to_template(request,
                              template='2011/seminar-current.html',
                              extra_context=ctx)


def seminar_archive(request, year=date.today().year):
    ctx = get_context(request)
    ctx['menu'] = 'seminars'
    city = request.GET.get('city', None)

    if city:
        ctx['seminars'] = Seminar.public_objects.filter(city__icontains=city)
    else:
        ctx['seminars'] = Seminar.public_objects.filter(start_date__year=year)

    ctx['years'] = reversed(Seminar.public_objects.dates('start_date', 'year'))
    ctx['cities'] = Seminar.public_objects.values_list('city', flat=True).distinct().order_by('city')
    ctx['city'] = city
    ctx['year'] = year

    return direct_to_template(request,
                              template='2011/seminar-archive.html',
                              extra_context=ctx)


def downloads(request):
    '''Displays the public downloads site.'''

    ctx = get_context(request)
    ctx['menu'] = 'downloads'
    ctx['include_main_image'] = False

    return object_list(
                       request,
                       queryset=Download.public_objects.all(),
                       paginate_by=50,
                       extra_context=ctx,
                       template_name='twa-downloads.html',
                       )


@login_required
def create_twa_ids(request):
    '''Create twa IDs and redirect to open member requests.'''

    if request.user.is_superuser:
        antraege = TWAMembership.objects.filter(twa_id_number=None).exclude(person__country__code='JP')
        antraege = antraege.filter(Q(status=MEMBERSHIP_STATUS_ACCEPTED) |
                                   Q(status=MEMBERSHIP_STATUS_CONFIRMED) |
                                   Q(status=MEMBERSHIP_STATUS_TO_BE_CONFIRMED)
                                   ).order_by('id')
        for antrag in antraege:
            dojos = antrag.person.dojos.all()
            if dojos.count() > 0:
                country = dojos[0].country
            else:
                country = antrag.person.country
            antrag.twa_id_country = country
            twa_id_number = TWAMembership.objects.get_next_id_for_country(country.code)
            if twa_id_number is not None:
                antrag.twa_id_number = twa_id_number
                antrag.save()

    return member_requests(request, status=LICENSE_STATUS_OPEN)


@login_required
def confirmation_email(request):
    '''Sends confirmation by email and redirect to open member requests.'''

    if request.user.is_superuser:

        antraege = TWAMembership.objects.filter(status=MEMBERSHIP_STATUS_ACCEPTED)

        datalist = []
        try:
            for antrag in antraege:
                if antrag.person.email:
                    subject = 'Aufnahme in den TWA bestätigt'
                    message = EMAIL_TEMPLATE_MEMBERSHIP_CONFIRMATION % {'firstname': antrag.person.firstname, 'twaid': antrag.twa_id()}
                    from_email = EMAIL_HOST_USER
                    recipient_list = []
                    recipient_list.append(antrag.person.email)
                    recipient_list.append(EMAIL_HOST_USER)

                    datalist.append((subject, message, from_email, recipient_list))

                    antrag.status = MEMBERSHIP_STATUS_CONFIRMED
                    antrag.save()
                else:
                    antrag.status = MEMBERSHIP_STATUS_TO_BE_CONFIRMED
                    antrag.save()

            send_mass_mail(tuple(datalist), fail_silently=True)

        except:
            raise Http404
    else:
        raise Http404

    return member_requests(request, status=LICENSE_STATUS_OPEN)


@login_required
def accept_open_requests(request):
    '''Sets all open membership requests to status "accepted".'''

    if request.user.is_superuser:
        for antrag in TWAMembership.objects.filter(status=MEMBERSHIP_STATUS_OPEN):
            antrag.status = MEMBERSHIP_STATUS_ACCEPTED
            antrag.save()
        return member_requests(request, status=LICENSE_STATUS_OPEN)
    else:
        raise Http404


def dynamic_pages(request, path):
    '''Displays a static page stored in the database.'''

    if not path.startswith('/'):
        path = '/' + path

    try:
        page = get_object_or_404(Page, url__iexact=path)
    except Http404:
        page = get_object_or_404(Page, url__iexact=path + '/')

    return direct_to_template(request,
                              template='flatpages/default.html',
                              extra_context=dict(page=page))
