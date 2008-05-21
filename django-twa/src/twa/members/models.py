#-*- coding: utf-8 -*-

from PIL import Image
from datetime import date, datetime, timedelta
from django.db import models
from django.db.models import Q
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
import calendar

DEFAULT_MAX_LENGTH = 200

GENDER = [
    ( 'm', _( 'male' ) ),
    ( 'f', _( 'female' ) ),
]

NAME_PREFIX = [
    ( 'd', _( 'Dr.' ) ),
    ( 'p', _( 'Prof.' ) ),
    ( 'dd', _( 'Dr. Dr.' ) ),
    ( 'pd', _( 'Prof. Dr.' ) ),
]

RANK = [
    ( 1000, _( '10. Dan' ) ),
    ( 900, _( '9. Dan' ) ),
    ( 800, _( '8. Dan' ) ),
    ( 700, _( '7. Dan' ) ),
    ( 600, _( '6. Dan' ) ),
    ( 500, _( '5. Dan' ) ),
    ( 400, _( '4. Dan' ) ),
    ( 300, _( '3. Dan' ) ),
    ( 200, _( '2. Dan' ) ),
    ( 100, _( '1. Dan' ) ),
    ( 50, _( '1. Kyu' ) ),
    ( 40, _( '2. Kyu' ) ),
    ( 30, _( '3. Kyu' ) ),
    ( 20, _( '4. Kyu' ) ),
    ( 10, _( '5. Kyu' ) ),
]

LICENSE_STATUS_OPEN = 1
LICENSE_STATUS_ACCEPTED = 2
LICENSE_STATUS_REJECTED = 3
LICENSE_STATUS_VERIFY = 4
LICENSE_STATUS_LICENSED = 5

LICENSE_STATUS = [
    ( LICENSE_STATUS_OPEN, _( 'open' ) ),
    ( LICENSE_STATUS_ACCEPTED, _( 'accepted' ) ),
    ( LICENSE_STATUS_REJECTED, _( 'rejected' ) ),
    ( LICENSE_STATUS_VERIFY, _( 'verify' ) ),
    ( LICENSE_STATUS_LICENSED, _( 'licensed' ) ),
]

class RequestManager( models.Manager ):
    def get_query_set( self ):
        return super( RequestManager, self ).get_query_set()

    def get_user_agents( self ):
        return self.get_query_set().values( 'user_agent' ).distinct()

    def get_user_agents_by_requests( self ):
        agents = []
        for ua in self.get_user_agents():
            agents.append( { 'count': self.get_query_set().filter( user_agent = ua['user_agent'] ).count(), 'user_agent': ua['user_agent'] } )
        #agents.append( { 'user_agent': '[all requests]', 'count': self.get_query_set().count() } )
        return agents

class Request( models.Model ):
    user = models.CharField( 'User', max_length = DEFAULT_MAX_LENGTH, blank = True )
    user_agent = models.CharField( 'User Agent', max_length = 500, blank = True )
    path = models.CharField( 'Path', max_length = DEFAULT_MAX_LENGTH, blank = True )
    remote = models.CharField( 'Remote', max_length = DEFAULT_MAX_LENGTH, blank = True )

    created = models.DateTimeField( _( 'Created' ), auto_now_add = True )
    last_modified = models.DateTimeField( _( 'Last Modified' ), auto_now = True )

    objects = RequestManager()

    #class Admin:
    #    ordering = [ '-created' ]
    #    list_display = ( 'id', 'created', 'user', 'path', 'user_agent', 'remote' )
    #    #list_display_links = ( 'created', 'user' )
    #    list_filter = [ 'user' ]

class Translation( models.Model ):
    name = models.CharField( 'Name', max_length = DEFAULT_MAX_LENGTH, unique = True )
    entry = models.CharField( 'Entry (en)', max_length = DEFAULT_MAX_LENGTH )
    entry_de = models.CharField( 'Entry (de)', max_length = DEFAULT_MAX_LENGTH, blank = True )
    entry_ja = models.CharField( 'Entry (ja)', max_length = DEFAULT_MAX_LENGTH, blank = True )

    created = models.DateTimeField( 'Created', auto_now_add = True )
    last_modified = models.DateTimeField( 'Last Modified', auto_now = True )

    def get_entry( self, language = None ):
        return getattr( self, "entry_%s" % ( language or translation.get_language()[:2] ), "" ) or self.entry

    def __unicode__( self ):
        return self.get_entry()

class Country( models.Model ):
    name = models.CharField( _( 'Name (en)' ), max_length = DEFAULT_MAX_LENGTH, unique = True )
    name_de = models.CharField( _( 'Name (de)' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    name_ja = models.CharField( _( 'Name (ja)' ), max_length = DEFAULT_MAX_LENGTH, blank = True )

    created = models.DateTimeField( _( 'Created' ), auto_now_add = True )
    last_modified = models.DateTimeField( _( 'Last Modified' ), auto_now = True )

    def get_name( self, language = None ):
        return getattr( self, "name_%s" % ( language or translation.get_language()[:2] ), "" ) or self.name

    def __unicode__( self ):
        return self.name

    class Meta:
        ordering = [ 'name' ]
        verbose_name = _( 'Country' )
        verbose_name_plural = _( 'Countries' )

    class Admin:
        ordering = [ 'name' ]
        list_display = ( 'name', 'name_de', 'name_ja' )
        list_display_links = ( 'name', 'name_de', 'name_ja' )

class PersonManager( models.Manager ):
    def get_query_set( self ):
        #if Person.objects.all().count() == 0:
        #    from createInitialData import Import
        #    Import()
        return super( PersonManager, self ).get_query_set().filter( is_active = True )

    def get_persons_by_rank( self, rank ):
        return self.get_query_set().filter( current_rank = rank )

    def get_licensed( self ):
        return self.get_query_set().filter( license__date__isnull = False )

    def get_by_requested_licenses( self ):
        return self.get_query_set().filter( license__request__isnull = False, license__date__isnull = True )

    def get_by_requested_membership( self ):
        return self.get_query_set().filter( twa_membership_requested__isnull = False, twa_membership__isnull = True )

    def get_members( self ):
        return self.get_query_set().filter( twa_membership__isnull = False )

    def get_next_birthdays( self ):
        liste = []
        persons = self.get_query_set().filter( birth__isnull = False )
        for person in persons:
            if person.days() < 8:
                liste.append( person )
        liste.sort()
        return liste

class Person( models.Model ):
    firstname = models.CharField( _( 'First Name' ), max_length = DEFAULT_MAX_LENGTH )
    nickname = models.CharField( _( 'Nickname' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    lastname = models.CharField( _( 'Last Name' ), max_length = DEFAULT_MAX_LENGTH )
    name_prefix = models.CharField( _( 'Name Prefix' ), max_length = 5, choices = NAME_PREFIX, blank = True )
    text = models.TextField( _( 'Text' ), blank = True )
    text_beirat = models.TextField( _( 'Text (Beirat)' ), editable = False, blank = True )
    photo = models.ImageField( _( 'Photo' ), upload_to = 'photos/', blank = True )
    thumbnail = models.ImageField( _( 'Thumbnail' ), upload_to = 'photos/thumbs/', blank = True, editable = False )

    street = models.CharField( _( 'Street' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    zip = models.CharField( _( 'Zip' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    city = models.CharField( _( 'City' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    country = models.ForeignKey( Country, verbose_name = _( 'Country' ), blank = True, null = True )

    phone = models.CharField( _( 'Phone' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    fax = models.CharField( _( 'Fax' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    mobile = models.CharField( _( 'Mobile' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    email = models.EmailField( _( 'Email' ), blank = True )
    website = models.URLField( _( 'Website' ), verify_exists = False, blank = True )

    birth = models.DateField( _( 'Birth' ), blank = True, null = True )
    birth_sort_string = models.CharField( max_length = 4, editable = False )
    gender = models.CharField( _( 'Gender' ), max_length = 1, choices = GENDER, blank = True )

    is_active = models.BooleanField( _( 'Active' ), default = True )
    twa_membership_requested = models.DateField( _( 'TWA Membership Request' ), blank = True, null = True )
    twa_membership = models.DateField( _( 'TWA Member' ), blank = True, null = True )
    aikido_since = models.DateField( _( 'Aikido' ), blank = True, null = True )
    dojos = models.ManyToManyField( 'Dojo', verbose_name = _( 'Dojos' ), filter_interface=models.VERTICAL, blank = True, null = True )
    current_rank = models.IntegerField( _( 'Rank' ), choices = RANK, editable = False )

    created = models.DateTimeField( _( 'Created' ), auto_now_add = True )
    last_modified = models.DateTimeField( _( 'Last Modified' ), auto_now = True )

    objects = models.Manager()
    persons = PersonManager()

    def is_license_requested( self ):
        return self.license_set.filter( request__isnull = False, date__isnull = True ).count() > 0

    def is_licensed( self ):
        return self.license_set.filter( date__isnull = False ).count() > 0

    def age( self ):
        if self.birth:
            today = date.today()
            this_years_birthday = date( today.year, self.birth.month, self.birth.day )
            if this_years_birthday <= today:
                return today.year - self.birth.year
            return today.year - self.birth.year - 1
        else:
           return ''
    age.short_description = _( 'Age' )
    age.allow_tags = False

    def days( self ):
        try:
            if self.birth:
                today = date.today()
                this_years_birthday = date( today.year, self.birth.month, self.birth.day )
                if this_years_birthday < today:
                    year = today.year + 1
                    if self.birth.month == 2 and self.birth.day == 29:
                        while not calendar.isleap( year ):
                            year += 1
                    this_years_birthday = date( year, self.birth.month, self.birth.day )
                return ( this_years_birthday - today ).days
            else:
               return 0
        except:
            from django.core.mail import mail_admins
            msg = 'error resolving days to birth %s for %s. today is %s' % ( self.birth, self, date.today() )
            mail_admins( 'Error', msg, fail_silently = True )
            return 9999
    days.short_description = _( 'Days' )
    days.allow_tags = False

    def save( self ):
        if self.birth:
            self.birth_sort_string = self.birth.strftime( '%m%d' )

        if self.photo:
            THUMBNAIL_SIZE = ( 75, 75 )
            SCALE_SIZE = ( 300, 400 )

            if not self.thumbnail:
                self.save_thumbnail_file( self.get_photo_filename(), '' )

            image = Image.open( self.get_photo_filename() )

            if image.mode not in ( 'L', 'RGB' ):
                image = image.convert( 'RGB' )

            image.thumbnail( SCALE_SIZE, Image.ANTIALIAS )
            image.save( self.get_photo_filename() )

            image.thumbnail( THUMBNAIL_SIZE, Image.ANTIALIAS )
            image.save( self.get_thumbnail_filename() )

        super( Person, self ).save()

    def admin_thumb( self ):
        try:
            w = self.get_thumbnail_width()
            h = self.get_thumbnail_height()
            return u'<img src="%s" width="%s" height="%s" />' % ( self.get_thumbnail_url(), w, h )
        except:
            return u''
    admin_thumb.short_description = _( 'Photo' )
    admin_thumb.allow_tags = True

    def get_absolute_url( self ):
        return '/member/%i/' % self.id

    def __cmp__( self, other ):
        return cmp( self.days(), other.days() )

    def __unicode__( self ):
        if self.nickname:
            nick = '"%s"' % self.nickname
        else:
            nick = ''

        if self.name_prefix:
            prefix = self.get_name_prefix_display()
        else:
            prefix = ''
        return u'%s %s %s %s'.strip() % ( prefix, self.firstname, nick, self.lastname )

    class Meta:
        ordering = [ 'firstname', 'lastname' ]
        verbose_name = _( 'Person' )
        verbose_name_plural = _( 'Persons' )

    class Admin:
        ordering = [ 'firstname', 'lastname' ]
        list_display = ( 'id', 'firstname', 'lastname', 'current_rank', 'twa_membership', 'age', 'gender', 'photo', 'is_active', 'admin_thumb' )
        list_display_links = ( 'firstname', 'lastname', 'admin_thumb' )
        list_filter = ( 'current_rank', 'is_active', 'twa_membership' )
        search_fields = [ 'id', 'firstname', 'lastname', 'city' ]

class DojoManager( models.Manager ):
    def get_query_set( self ):
        return super( DojoManager, self ).get_query_set().filter( is_active = True )

class Dojo( models.Model ):
    name = models.CharField( _( 'Name' ), max_length = DEFAULT_MAX_LENGTH, unique = True )
    shortname = models.CharField( _( 'Short Name' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    text = models.TextField( _( 'Text' ), blank = True )

    street = models.CharField( _( 'Street' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    zip = models.CharField( _( 'Zip' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    city = models.CharField( _( 'City' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    country = models.ForeignKey( Country, verbose_name = _( 'Country' ) )

    phone = models.CharField( _( 'Phone' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    fax = models.CharField( _( 'Fax' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    mobile = models.CharField( _( 'Mobile' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    email = models.EmailField( _( 'Email' ), blank = True )
    website = models.URLField( _( 'Website' ), verify_exists = False, blank = True )

    is_active = models.BooleanField( _( 'Active' ), default = True )
    is_twa_member = models.BooleanField( _( 'TWA Member' ), default = False )
    leader = models.ForeignKey( Person, verbose_name = _( 'Dojo Leader' ), related_name = 'dojo_leader', blank = True, null = True )
    association = models.ForeignKey( 'Association', verbose_name = _( 'Association' ), blank = True, null = True )

    created = models.DateTimeField( _( 'Created' ), auto_now_add = True )
    last_modified = models.DateTimeField( _( 'Last Modified' ), auto_now = True )

    objects = models.Manager()
    dojos = DojoManager()

    def get_absolute_url( self ):
        return '/dojo/%i/' % self.id

    def save( self ):
        if self.is_active == False:
            for person in Person.objects.filter( dojos__id = self.id ):
                person.is_active = False
                person.save()
        super( Dojo, self ).save()

    def __unicode__( self ):
        if self.shortname:
            return self.shortname
        elif self.city:
            return self.city
        else:
            return self.name

    class Meta:
        ordering = [ 'country', 'city', 'name' ]
        verbose_name = _( 'Dojo' )
        verbose_name_plural = _( 'Dojos' )

    class Admin:
        ordering = [ 'city', 'name' ]
        list_display = ( 'id', 'city', 'name', 'leader', 'is_active', 'is_twa_member' )
        list_display_links = ( 'name', )
        list_filter = ( 'is_active', 'country', )
        search_fields = [ 'id', 'firstname', 'lastname', 'city' ]

class Association( models.Model ):
    name = models.CharField( _( 'Name' ), max_length = DEFAULT_MAX_LENGTH, unique = True )
    shortname = models.CharField( _( 'Short Name' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    text = models.TextField( _( 'Text' ), blank = True )

    street = models.CharField( _( 'Street' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    zip = models.CharField( _( 'Zip' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    city = models.CharField( _( 'City' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    province = models.CharField( _( 'Province' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    country = models.ForeignKey( Country, verbose_name = _( 'Country' ) )

    phone = models.CharField( _( 'Phone' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    fax = models.CharField( _( 'Fax' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    mobile = models.CharField( _( 'Mobile' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    email = models.EmailField( _( 'Email' ), blank = True )
    website = models.URLField( _( 'Website' ), verify_exists = False, blank = True )

    is_active = models.BooleanField( _( 'Active' ), default = True )
    contact = models.ForeignKey( Person, verbose_name = _( 'Contact' ), related_name = 'association', blank = True, null = True )

    created = models.DateTimeField( _( 'Created' ), auto_now_add = True )
    last_modified = models.DateTimeField( _( 'Last Modified' ), auto_now = True )

    def get_absolute_url( self ):
        return '/association/%i/' % self.id

    def __unicode__( self ):
        return ( '%s - %s' % ( self.province, self.name ) ).strip()

    class Meta:
        ordering = [ 'country', 'province', 'name' ]
        verbose_name = _( 'Association' )
        verbose_name_plural = _( 'Associations' )

    class Admin:
        ordering = [ 'country', 'province', 'name' ]
        list_display = ( 'id', 'name', 'contact', 'is_active' )
        list_display_links = ( 'name', )
        list_filter = ( 'is_active', 'country', )
        search_fields = [ 'id', 'name', 'shortname', 'city', 'text' ]

class SuggestionsManager( models.Manager ):
    def get_query_set( self ):
        return super( SuggestionsManager, self ).get_query_set().filter( is_active = True, is_nomination = True )

class GraduationManager( models.Manager ):
    def get_query_set( self ):
        return super( GraduationManager, self ).get_query_set().filter( is_active = True, is_nomination = False )

    def get_current( self, person ):
        try:
            return max( Graduation.objects.filter( person__id = person.id, is_active = True, is_nomination = False ).iterator() )
        except:
            return None

    def get_this_years_graduations( self ):
        return self.get_query_set().filter( is_active = True, date__year = date.today().year )

class Graduation( models.Model ):
    person = models.ForeignKey( 'Person', verbose_name = _( 'Person' ), related_name = 'person_related' )
    nominated_by = models.ForeignKey( 'Person', verbose_name = _( 'Nominated By' ), related_name = 'nominated_by_related', blank = True, null = True )
    rank = models.IntegerField( _( 'Rank' ), choices = RANK )
    date = models.DateField( _( 'Date' ), blank = True, null = True )
    text = models.TextField( _( 'Text' ), blank = True )
    is_nomination = models.BooleanField( _( 'Nomination' ), default = False )
    request_doc = models.FileField( _( 'Request Document' ), upload_to = 'docs/', blank = True, null = True )
    is_active = models.BooleanField( _( 'Active' ), default = True )

    created = models.DateTimeField( _( 'Created' ), auto_now_add = True, default = datetime.now() )
    last_modified = models.DateTimeField( _( 'Last Modified' ), auto_now = True )

    objects = models.Manager()
    graduations = GraduationManager()
    suggestions = SuggestionsManager()

    def __unicode__( self ):
        return u'%s %s'.strip() % ( self.rank, self.date )

    def __cmp__( self, other ):
        return cmp( self.rank, other.rank )

    def save( self ):
        super( Graduation, self ).save()
        self.person.current_rank = GraduationManager().get_current( self.person )
        self.person.save()

    class Meta:
        ordering = [ '-rank', '-date' ]
        get_latest_by = "date"
        verbose_name = _( 'Graduation' )
        verbose_name_plural = _( 'Graduations' )

    class Admin:
        ordering = [ '-rank', '-date' ]
        list_display = ( 'id', 'rank', 'person', 'date', 'text', 'is_nomination', 'nominated_by', 'is_active' )
        list_display_links = ( 'person', 'rank', )
        list_filter = ( 'is_active', 'is_nomination', 'rank', 'person' )
        search_fields = [ 'id', 'text' ]

class LicenseManager( models.Manager ):
    def get_requested_licenses( self ):
        #for lic in License.objects.all():
        #    if lic.date:
        #        lic.status = LICENSE_STATUS_LICENSED
        #    else:
        #        if lic.is_active:
        #            lic.status = LICENSE_STATUS_OPEN
        #        else:
        #            lic.status = LICENSE_STATUS_REJECTED
        #    lic.save()

        return License.objects.filter( is_active = True ).exclude( status = LICENSE_STATUS_LICENSED )#.exclude( status = LICENSE_STATUS_REJECTED )

    def get_granted_licenses( self ):
        return License.objects.filter( status = LICENSE_STATUS_LICENSED, is_active = True )

    def get_rejected_licenses( self ):
        return License.objects.filter( status = LICENSE_STATUS_REJECTED, is_active = True )

class License( models.Model ):
    person = models.ForeignKey( Person, verbose_name = _( 'Person' ) )
    status = models.IntegerField( _( 'License Status' ), choices = LICENSE_STATUS, default = LICENSE_STATUS_OPEN )
    date = models.DateField( _( 'License Date' ), blank = True, null = True )
    request = models.DateField( _( 'License Request' ), blank = True, null = True )
    receipt = models.DateField( _( 'License Receipt' ), blank = True, null = True )
    rejected = models.DateField( _( 'License Rejected' ), blank = True, null = True )
    request_doc = models.FileField( _( 'License Request Document' ), upload_to = 'docs/', blank = True, null = True )
    receipt_doc = models.FileField( _( 'License Receipt Document' ), upload_to = 'docs/', blank = True, null = True )
    text = models.TextField( _( 'Text' ), blank = True )
    is_active = models.BooleanField( _( 'Active' ), default = True )

    created = models.DateTimeField( _( 'Created' ), auto_now_add = True )
    last_modified = models.DateTimeField( _( 'Last Modified' ), auto_now = True )

    objects = LicenseManager()

    def get_absolute_url( self ):
        return '/member/%i/' % self.person.id

    def __unicode__( self ):
        return u'%s'.strip() % ( self.person )

    class Meta:
        ordering = [ '-id' ]
        verbose_name = _( 'License' )
        verbose_name_plural = _( 'Licenses' )

    class Admin:
        ordering = [ '-id' ]
        list_display = ( 'id', 'status', 'person', 'date', 'request', 'receipt', 'rejected', 'is_active' )
        list_display_links = ( 'status', 'person' )
        list_filter = [ 'status', 'is_active' ]
        search_fields = [ 'person__firstname', 'person__nickname', 'person__lastname' ]

class Document( models.Model ):
    name = models.CharField( _( 'Name' ), max_length = DEFAULT_MAX_LENGTH, core = True )
    file = models.FileField( _( 'File' ), upload_to = 'docs/', core = True )
    person = models.ForeignKey( Person, verbose_name = _( 'Person' ), blank = True, null = True, edit_inline = models.TABULAR, num_in_admin = 3 )

    created = models.DateTimeField( _( 'Created' ), auto_now_add = True, default = datetime.now() )
    last_modified = models.DateTimeField( _( 'Last Modified' ), auto_now = True )

    def __unicode__( self ):
        return self.name

    class Meta:
        ordering = [ 'name' ]
        verbose_name = _( 'Document' )
        verbose_name_plural = _( 'Documents' )

    class Admin:
        ordering = [ 'name' ]
        list_display = ( 'id', 'name', 'file', 'person' )
        list_display_links = ( 'name', 'file', )
