#-*- coding: utf-8 -*-

from PIL import Image
from datetime import date, datetime, timedelta
from django.contrib import admin
from django.db import models
from django.db.models import Q
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
import calendar
from twa.utils import DEFAULT_MAX_LENGTH, AbstractModel

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

class Country( AbstractModel ):
    name = models.CharField( _( 'Name (en)' ), max_length = DEFAULT_MAX_LENGTH, unique = True )
    name_de = models.CharField( _( 'Name (de)' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    name_ja = models.CharField( _( 'Name (ja)' ), max_length = DEFAULT_MAX_LENGTH, blank = True )

    def get_name( self, language = None ):
        return getattr( self, "name_%s" % ( language or translation.get_language()[:2] ), "" ) or self.name

    def __unicode__( self ):
        return self.name

    class Meta:
        ordering = [ 'name' ]
        verbose_name = _( 'Country' )
        verbose_name_plural = _( 'Countries' )

class PersonManager( models.Manager ):
    def get_query_set( self ):
        return super( PersonManager, self ).get_query_set().filter( is_active = True, public = True )

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

class Person( AbstractModel ):
    firstname = models.CharField( _( 'First Name' ), max_length = DEFAULT_MAX_LENGTH )
    lastname = models.CharField( _( 'Last Name' ), max_length = DEFAULT_MAX_LENGTH )
    nickname = models.CharField( _( 'Nickname' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
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
    dojos = models.ManyToManyField( 'Dojo', verbose_name = _( 'Dojos' ), blank = True, null = True )
    current_rank = models.IntegerField( _( 'Rank' ), choices = RANK, editable = False, blank = True, null = True )

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
        else:
            self.birth_sort_string = ''

        if self.photo:
            THUMBNAIL_SIZE = ( 75, 75 )
            SCALE_SIZE = ( 300, 400 )

            if not self.thumbnail:
                self.thumbnail.save( self.photo.path, self.photo, save = True )

            image = Image.open( self.photo.path )

            if image.mode not in ( 'L', 'RGB' ):
                image = image.convert( 'RGB' )

            image.thumbnail( SCALE_SIZE, Image.ANTIALIAS )
            image.save( self.photo.path )

            image.thumbnail( THUMBNAIL_SIZE, Image.ANTIALIAS )
            image.save( self.thumbnail.path )

        super( Person, self ).save()

    def admin_thumb( self ):
        try:
            w = self.thumbnail.width
            h = self.thumbnail.height
            return u'<img src="%s" width="%s" height="%s" />' % ( self.thumbnail.url, w, h )
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
        name = u'%s %s %s %s' % ( prefix, self.firstname, nick, self.lastname )
        return name.strip()

    class Meta:
        ordering = [ 'firstname', 'lastname' ]
        verbose_name = _( 'Person' )
        verbose_name_plural = _( 'Persons' )

class DojoManager( models.Manager ):
    def get_query_set( self ):
        return super( DojoManager, self ).get_query_set().filter( is_active = True, public = True )

class Dojo( AbstractModel ):
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

    objects = models.Manager()
    dojos = DojoManager()

    def get_absolute_url( self ):
        return '/dojo/%i/' % self.id

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

class Association( AbstractModel ):
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

    def get_absolute_url( self ):
        return '/association/%i/' % self.id

    def __unicode__( self ):
        return ( '%s - %s' % ( self.province, self.name ) ).strip()

    class Meta:
        ordering = [ 'country', 'province', 'name' ]
        verbose_name = _( 'Association' )
        verbose_name_plural = _( 'Associations' )

class SuggestionsManager( models.Manager ):
    def get_query_set( self ):
        return super( SuggestionsManager, self ).get_query_set().filter( is_active = True, public = True, is_nomination = True )

class GraduationManager( models.Manager ):
    def get_query_set( self ):
        return super( GraduationManager, self ).get_query_set().filter( is_active = True, public = True, is_nomination = False )

    def get_current( self, person ):
        try:
            return max( Graduation.objects.filter( person__id = person.id, is_active = True, public = True, is_nomination = False ).iterator() ).rank
        except:
            return None

    def get_this_years_graduations( self ):
        return self.get_query_set().filter( is_active = True, public = True, date__year = date.today().year )

class Graduation( AbstractModel ):
    person = models.ForeignKey( 'Person', verbose_name = _( 'Person' ), related_name = 'person_related' )
    nominated_by = models.ForeignKey( 'Person', verbose_name = _( 'Nominated By' ), related_name = 'nominated_by_related', blank = True, null = True )
    rank = models.IntegerField( _( 'Rank' ), choices = RANK )
    date = models.DateField( _( 'Date' ), blank = True, null = True )
    text = models.TextField( _( 'Text' ), blank = True )
    is_nomination = models.BooleanField( _( 'Nomination' ), default = False )
    request_doc = models.FileField( _( 'Request Document' ), upload_to = 'docs/', blank = True, null = True )
    confirmation_doc = models.FileField( _( 'Confirmation Document' ), upload_to = 'docs/', blank = True, null = True )
    payment_doc = models.FileField( _( 'Payment Document' ), upload_to = 'docs/', blank = True, null = True )
    is_active = models.BooleanField( _( 'Active' ), default = True )

    objects = models.Manager()
    graduations = GraduationManager()
    suggestions = SuggestionsManager()

    def __unicode__( self ):
        return u'%s %s'.strip() % ( self.rank, self.date )

    def __cmp__( self, other ):
        return cmp( self.rank, other.rank )

    def get_absolute_url( self ):
        return '/member/%i/' % self.person.id

    def save( self ):
        super( Graduation, self ).save()
        self.person.current_rank = GraduationManager().get_current( self.person )
        self.person.save()

    class Meta:
        ordering = [ '-rank', '-date' ]
        get_latest_by = "date"
        verbose_name = _( 'Graduation' )
        verbose_name_plural = _( 'Graduations' )

class LicenseManager( models.Manager ):
    def get_requested_licenses( self ):
        return License.objects.filter( is_active = True, public = True ).exclude( status = LICENSE_STATUS_LICENSED )#.exclude( status = LICENSE_STATUS_REJECTED )

    def get_granted_licenses( self ):
        return License.objects.filter( status = LICENSE_STATUS_LICENSED, is_active = True, public = True )

    def get_rejected_licenses( self ):
        return License.objects.filter( status = LICENSE_STATUS_REJECTED, is_active = True, public = True )

class License( AbstractModel ):
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

    objects = LicenseManager()

    def get_absolute_url( self ):
        return '/member/%i/' % self.person.id

    def __unicode__( self ):
        return u'%s'.strip() % ( self.person )

    class Meta:
        ordering = [ '-id' ]
        verbose_name = _( 'License' )
        verbose_name_plural = _( 'Licenses' )

class Document( AbstractModel ):
    name = models.CharField( _( 'Name' ), max_length = DEFAULT_MAX_LENGTH )
    file = models.FileField( _( 'File' ), upload_to = 'docs/' )
    person = models.ForeignKey( Person, verbose_name = _( 'Person' ), blank = True, null = True )

    def __unicode__( self ):
        return self.name

    class Meta:
        ordering = [ 'name' ]
        verbose_name = _( 'Document' )
        verbose_name_plural = _( 'Documents' )
