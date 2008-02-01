#-*- coding: utf-8 -*-

from datetime import date, datetime, timedelta
from django.db import models
from django.db.models import Q
from django.utils import translation
from django.utils.translation import ugettext_lazy as _

DEFAULT_MAX_LENGTH = 200

GENDER = [
    ( 'm', _( 'male' ) ),
    ( 'f', _( 'female' ) ),
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

def get_next_month( month ):
    if month == 12:
        return 1
    else:
        return month + 1

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
        return super( PersonManager, self ).get_query_set().filter()

    def get_next_birthdays( self ):
        liste = []
        persons = self.get_query_set().filter(birth__isnull = False)
        for person in persons:
            if person.days() < 8:
                liste.append(person)
        liste.sort()
        return liste

class Person( models.Model ):
    firstname = models.CharField( _( 'First Name' ), max_length = DEFAULT_MAX_LENGTH )
    lastname = models.CharField( _( 'Last Name' ), max_length = DEFAULT_MAX_LENGTH )
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
    twa_license_requested = models.DateField( _( 'TWA License Request' ), blank = True, null = True )
    twa_membership = models.DateField( _( 'TWA Member' ), blank = True, null = True )
    twa_license = models.DateField( _( 'TWA License' ), blank = True, null = True )
    aikido_since = models.DateField( _( 'Aikido' ), blank = True, null = True )
    dojos = models.ManyToManyField( 'Dojo', verbose_name = _( 'Dojos' ), filter_interface=models.VERTICAL, blank = True, null = True )

    created = models.DateTimeField( _( 'Created' ), auto_now_add = True )
    last_modified = models.DateTimeField( _( 'Last Modified' ), auto_now = True )

    objects = PersonManager()
    persons = PersonManager()

    def current_rank( self ):
        return GraduationManager().get_current( self ).get_rank_display()
    current_rank.short_description = _( 'Rank' )
    current_rank.allow_tags = False

    def grade_date( self ):
        return GraduationManager().get_current( self ).date
    grade_date.short_description = _( 'Date' )
    grade_date.allow_tags = False

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
        if self.birth:
            today = date.today()
            this_years_birthday = date( today.year, self.birth.month, self.birth.day )
            if this_years_birthday < today:
                this_years_birthday = date(today.year + 1, self.birth.month, self.birth.day)
            return (this_years_birthday - today).days
        else:
           return 0
    days.short_description = _( 'Days' )
    days.allow_tags = False

    def save( self ):
        if self.birth:
            self.birth_sort_string = self.birth.strftime( '%m%d' )

        if self.photo:
            THUMBNAIL_SIZE = ( 75, 75 )
            SCALE_SIZE = ( 800, 600 )

            if not self.thumbnail:
                from PIL import Image

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

    def __cmp__(self, other):
        return cmp( self.days(), other.days() )
    
    def __unicode__( self ):
        return u'%s %s'.strip() % ( self.firstname, self.lastname )

    class Meta:
        ordering = [ 'firstname', 'lastname' ]
        verbose_name = _( 'Person' )
        verbose_name_plural = _( 'Persons' )

    class Admin:
        ordering = [ 'firstname', 'lastname' ]
        list_display = ( 'id', 'firstname', 'lastname', 'age', 'days', 'gender', 'current_rank', 'grade_date', 'is_active', 'admin_thumb' )
        list_display_links = ( 'firstname', 'lastname', 'admin_thumb' )
        #list_filter = ( 'current_rank', )
        search_fields = [ 'id', 'firstname', 'lastname', 'city' ]

class DojoManager( models.Manager ):
    def get_query_set( self ):
        if Person.objects.all().count() == 0:
            from createInitialData import Import
            Import()
        return super( DojoManager, self ).get_query_set()

class Dojo( models.Model ):
    name = models.CharField( _( 'Name' ), max_length = DEFAULT_MAX_LENGTH, unique = True )
    shortname = models.CharField( _( 'Short Name' ), max_length = DEFAULT_MAX_LENGTH )
    text = models.TextField( _( 'Text' ), blank = True )

    street = models.CharField( _( 'Street' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    zip = models.CharField( _( 'Zip' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    city = models.CharField( _( 'City' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    #country = models.CharField( _( 'Country' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    country = models.ForeignKey( Country, verbose_name = _( 'Country' ), blank = True, null = True )

    phone = models.CharField( _( 'Phone' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    fax = models.CharField( _( 'Fax' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    mobile = models.CharField( _( 'Mobile' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    email = models.EmailField( _( 'Email' ), blank = True )
    website = models.URLField( _( 'Website' ), verify_exists = False, blank = True )

    is_twa_member = models.BooleanField( _( 'TWA Member' ), default = False )
    leader = models.ForeignKey( Person, verbose_name = _( 'Dojo Leader' ), related_name = 'dojo_leader', blank = True, null = True )

    created = models.DateTimeField( _( 'Created' ), auto_now_add = True )
    last_modified = models.DateTimeField( _( 'Last Modified' ), auto_now = True )

    objects = DojoManager()

    def get_absolute_url( self ):
        return '/dojo/%i/' % self.id

    def __unicode__( self ):
        return self.name

    class Meta:
        ordering = [ 'country', 'city', 'name' ]
        verbose_name = _( 'Dojo' )
        verbose_name_plural = _( 'Dojos' )

    class Admin:
        ordering = [ 'city', 'name' ]
        list_display = ( 'id', 'city', 'name', 'leader', 'is_twa_member' )
        list_display_links = ( 'name', )
        #list_filter = ( 'city', )
        search_fields = [ 'id', 'firstname', 'lastname', 'city' ]

class GraduationManager( models.Manager ):
    def get_query_set( self ):
        return super( GraduationManager, self ).get_query_set().filter( is_nomination = False )

    def get_current( self, person ):
        graduations = Graduation.objects.filter( person__id = person.id, is_nomination = False ).order_by( '-rank' )
        if graduations:
            return graduations[0]
        else:
            return ''

class Graduation( models.Model ):
    person = models.ForeignKey( Person, verbose_name = _( 'Person' ), edit_inline = models.TABULAR, num_in_admin = 3 )
    rank = models.IntegerField( _( 'Rank' ), choices = RANK, core = True )
    date = models.DateField( _( 'Date' ), blank = True, null = True, core = True )
    text = models.TextField( _( 'Text' ), blank = True )
    is_nomination = models.BooleanField( _( 'Nomination' ), default = False )

    created = models.DateTimeField( _( 'Created' ), auto_now_add = True, default = datetime.now() )
    last_modified = models.DateTimeField( _( 'Last Modified' ), auto_now = True )

    def __unicode__( self ):
        return u'%s %s'.strip() % ( self.rank, self.date )

    class Meta:
        ordering = [ '-rank', '-date' ]
        verbose_name = _( 'Graduation' )
        verbose_name_plural = _( 'Graduations' )

    class Admin:
        ordering = [ '-rank', '-date' ]
        list_display = ( 'id', 'rank', 'date', 'person', 'text', 'is_nomination' )
        list_display_links = ( 'date', 'rank', )
        list_filter = ( 'is_nomination', 'rank', 'person' )
        #search_fields = [ 'id', 'firstname', 'lastname', 'city' ]

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
        ordering = [ 'person_id', 'name' ]
        list_display = ( 'id', 'name', 'file', 'person' )
        list_display_links = ( 'name', 'file', )
