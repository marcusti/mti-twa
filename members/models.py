#-*- coding: utf-8 -*-

from PIL import Image
import calendar
from datetime import date
from datetime import datetime
from django.contrib.syndication.feeds import Feed
from django.core.exceptions import MultipleObjectsReturned
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from django.utils.feedgenerator import Atom1Feed

from twa.members.templatetags.twa_tags import thumbnail
from twa.utils import AbstractModel
from twa.utils import DEFAULT_MAX_LENGTH
from twa.settings import DOCUMENTS_DIR

doc_file_system = FileSystemStorage(location=DOCUMENTS_DIR)

GENDER = [
    ( 'm', _( 'male' ) ),
    ( 'f', _( 'female' ) ),
]

TWA_REGION = [
    ( 1, 'Eckhardt/Marcus' ),
    ( 2, 'Peter' ),
    ( 3, 'Volker' ),
    ( 4, 'Robert/Stephan' ),
    ( 5, 'Milan' ),
    ( 6, 'Tendokan' ),
    ( 7, 'Ludo' ),
    ( 8, 'Tim' ),
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

MEMBERSHIP_STATUS_OPEN = 1
MEMBERSHIP_STATUS_ACCEPTED = 2
MEMBERSHIP_STATUS_REJECTED = 3
MEMBERSHIP_STATUS_VERIFY = 4
MEMBERSHIP_STATUS_CONFIRMED = 5
MEMBERSHIP_STATUS_TO_BE_CONFIRMED = 6
MEMBERSHIP_STATUS_MEMBER = 10
MEMBERSHIP_STATUS_EX = -1

MEMBERSHIP_STATUS = [
    ( MEMBERSHIP_STATUS_OPEN, _( 'open' ) ),
    ( MEMBERSHIP_STATUS_ACCEPTED, _( 'accepted' ) ),
    ( MEMBERSHIP_STATUS_CONFIRMED, _( 'confirmed' ) ),
    ( MEMBERSHIP_STATUS_TO_BE_CONFIRMED, _( 'to be confirmed' ) ),
    ( MEMBERSHIP_STATUS_REJECTED, _( 'rejected' ) ),
    ( MEMBERSHIP_STATUS_VERIFY, _( 'verify' ) ),
    ( MEMBERSHIP_STATUS_MEMBER, _( 'member' ) ),
    ( MEMBERSHIP_STATUS_EX, _( 'exit' ) ),
]

class Country( AbstractModel ):
    name = models.CharField( _( 'Name (en)' ), max_length = DEFAULT_MAX_LENGTH, unique = True )
    code = models.CharField( _( 'Code' ), max_length = 2, unique = True )
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

class AllPersonsManager( models.Manager ):
    use_for_related_fields = True

    def get_query_set( self ):
        SQL_GRAD = "SELECT MAX(rank) FROM members_graduation WHERE members_graduation.is_nomination = false AND members_graduation.person_id=members_person.id"
        SQL_GRAD_DATUM = "SELECT date FROM members_graduation WHERE members_graduation.person_id=members_person.id AND rank=(%s)" % SQL_GRAD
        return super( AllPersonsManager, self ).get_query_set().extra( select = { 'crank': SQL_GRAD } )

class PersonManager( AllPersonsManager ):
    def get_query_set( self ):
        return super( PersonManager, self ).get_query_set().filter( is_active = True, public = True )

    def get_persons_by_rank( self, rank ):
        return self.get_query_set().filter( crank = rank )

    def get_licensed( self ):
        return self.get_query_set().filter( license__status = LICENSE_STATUS_LICENSED )

    def get_by_requested_licenses( self ):
        return self.get_query_set().filter( license__request__isnull = False, license__date__isnull = True )

    def get_by_requested_membership( self ):
        return self.get_query_set().filter( twamembership__request__isnull = False, twamembership__date__isnull = True )

    def get_members( self ):
        return self.get_query_set().filter( twamembership__status = MEMBERSHIP_STATUS_MEMBER )

    def get_next_birthdays( self ):
        liste = []
        persons = self.get_query_set().filter( birth__isnull = False )
        for person in persons:
            if person.days() < 4:
                liste.append( person )
        liste.sort()
        return liste

class Person( AbstractModel ):
    firstname = models.CharField( _( 'First Name' ), max_length = DEFAULT_MAX_LENGTH )
    lastname = models.CharField( _( 'Last Name' ), max_length = DEFAULT_MAX_LENGTH )
    nickname = models.CharField( _( 'Nickname' ), max_length = DEFAULT_MAX_LENGTH, blank = True, null = True )
    firstname_jp = models.CharField( _( 'Japanese First Name' ), max_length = DEFAULT_MAX_LENGTH, blank = True, null = True )
    lastname_jp = models.CharField( _( 'Japanese Last Name' ), max_length = DEFAULT_MAX_LENGTH, blank = True, null = True )
    name_prefix = models.CharField( _( 'Name Prefix' ), max_length = 5, choices = NAME_PREFIX, blank = True, null = True )
    text = models.TextField( _( 'Text' ), blank = True, null = True )
    text_beirat = models.TextField( _( 'Text (Beirat)' ), editable = False, blank = True, null = True )
    photo = models.ImageField( _( 'Photo' ), storage = doc_file_system, upload_to = 'photos/', null = True, blank = True )

    street = models.CharField( _( 'Street' ), max_length = DEFAULT_MAX_LENGTH, blank = True, null = True )
    zip = models.CharField( _( 'Zip' ), max_length = DEFAULT_MAX_LENGTH, blank = True, null = True )
    city = models.CharField( _( 'City' ), max_length = DEFAULT_MAX_LENGTH, blank = True, null = True )
    country = models.ForeignKey( Country, verbose_name = _( 'Country' ) )

    phone = models.CharField( _( 'Phone' ), max_length = DEFAULT_MAX_LENGTH, blank = True, null = True )
    fax = models.CharField( _( 'Fax' ), max_length = DEFAULT_MAX_LENGTH, blank = True, null = True )
    mobile = models.CharField( _( 'Mobile' ), max_length = DEFAULT_MAX_LENGTH, blank = True, null = True )
    email = models.EmailField( _( 'Email' ), blank = True, null = True )
    website = models.URLField( _( 'Website' ), verify_exists = False, blank = True, null = True )

    birth = models.DateField( _( 'Birth' ), blank = True, null = True )
    birth_sort_string = models.CharField( max_length = 4, editable = False, null = True )
    gender = models.CharField( _( 'Gender' ), max_length = 1, choices = GENDER, blank = True, null = True )

    is_active = models.BooleanField( _( 'Active' ), default = True )
    aikido_since = models.DateField( _( 'Aikido' ), blank = True, null = True )
    dojos = models.ManyToManyField( 'Dojo', verbose_name = _( 'Dojos' ), blank = True, null = True )

    objects = AllPersonsManager()
    persons = PersonManager()

    def is_license_requested( self ):
        return self.license_set.filter( request__isnull = False, date__isnull = True ).count() > 0

    def is_licensed( self ):
        return self.license_set.filter( status = LICENSE_STATUS_LICENSED, is_active = True ).count() > 0

    def is_twa_membership_requested( self ):
        return self.twamembership_set.filter( request__isnull = False, date__isnull = True ).count() > 0

    def is_member( self ):
        return self.twamembership_set.filter( status = MEMBERSHIP_STATUS_MEMBER, is_active = True ).count() > 0

    def current_rank( self ):
        try:
            #return self.graduations.get( person__id = self.id, rank = self.crank )
            return Graduation.graduations.filter( person__id = self.id ).latest( 'date' )
        except:
            return ''
    current_rank.short_description = _( 'Rank' )
    current_rank.allow_tags = False

    def get_rank( self, rank ):
        try:
            return self.graduations.get( rank = rank )
        except MultipleObjectsReturned:
            return self.graduations.filter( rank = rank ).latest( 'date' )
        except:
            return ''

    def twa_status( self ):
        try:
            return self.twamembership_set.filter(is_active=True).latest( 'created' ).get_status_display()
        except:
            return ''
    twa_status.short_description = _( 'TWA Status' )
    twa_status.allow_tags = False

    def twa_id( self ):
        try:
            return self.twamembership_set.filter(is_active=True).latest( 'created' ).twa_id()
        except:
            return ''
    twa_id.short_description = _( 'TWA-ID' )
    twa_id.allow_tags = False

    def age( self ):
        try:
            today = date.today()
            if ( self.birth.month < today.month ) or ( self.birth.month == today.month and self.birth.day <= today.day ):
                return today.year - self.birth.year
            return today.year - self.birth.year - 1
        except:
            return ''
    age.short_description = _( 'Age' )
    age.allow_tags = False

    def days( self ):
        try:
            if self.birth:
                today = date.today()
                year = today.year
                if self.birth.month == 2 and self.birth.day == 29:
                    while not calendar.isleap( year ):
                        year += 1
                this_years_birthday = date( year, self.birth.month, self.birth.day )
                if this_years_birthday < today:
                    year = today.year + 1
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

    def save( self, force_insert = False ):
        if self.birth:
            self.birth_sort_string = self.birth.strftime( '%m%d' )
        else:
            self.birth_sort_string = ''

        super( Person, self ).save( force_insert )

        if self.photo:
            SCALE_SIZE = ( 300, 400 )

            image = Image.open( self.photo.path )

            if image.mode not in ( 'L', 'RGB' ):
                image = image.convert( 'RGB' )

            image.thumbnail( SCALE_SIZE, Image.ANTIALIAS )
            image.save( self.photo.path )

    def admin_thumb( self ):
        try:
            return u'<img src="/image/%s/64x64/" />' % ( self.photo.name )
        except:
            return u''
    admin_thumb.short_description = _( 'Photo' )
    admin_thumb.allow_tags = True

    def get_absolute_url( self ):
        return '/member/%i/' % self.id

    def __cmp__( self, other ):
        return cmp( self.days(), other.days() )

    def __unicode__( self ):
        name = u''

        if self.name_prefix:
            name = self.get_name_prefix_display()

        if self.lastname_jp:
            name += ' %s' % self.lastname_jp

        if self.firstname_jp:
            name += ' %s' % self.firstname_jp

        if self.firstname:
            name += ' %s' % self.firstname

        if self.nickname:
            name += ' "%s"' % self.nickname

        if self.lastname:
            name += ' %s' % self.lastname

        return name.strip()

    class Meta:
        ordering = [ 'firstname', 'lastname' ]
        unique_together = ('firstname', 'lastname')
        verbose_name = _( 'Person' )
        verbose_name_plural = _( 'Persons' )

class DojoManager( models.Manager ):
    def get_query_set( self ):
        return super( DojoManager, self ).get_query_set().filter( is_active = True, public = True )

class Dojo( AbstractModel ):
    name = models.CharField( _( 'Name' ), max_length = DEFAULT_MAX_LENGTH, unique = True )
    name_jp = models.CharField( _( 'Japanese Name' ), max_length = DEFAULT_MAX_LENGTH, blank = True, null = True )
    shortname = models.CharField( _( 'Short Name' ), max_length = DEFAULT_MAX_LENGTH, blank = True, null = True )
    text = models.TextField( _( 'Text' ), blank = True, null = True )

    street = models.CharField( _( 'Street' ), max_length = DEFAULT_MAX_LENGTH, blank = True, null = True )
    zip = models.CharField( _( 'Zip' ), max_length = DEFAULT_MAX_LENGTH, blank = True, null = True )
    city = models.CharField( _( 'City' ), max_length = DEFAULT_MAX_LENGTH, blank = True, null = True )
    country = models.ForeignKey( Country, verbose_name = _( 'Country' ) )
    twa_region = models.IntegerField( _( 'TWA Region' ), choices = TWA_REGION, blank = True, null = True )

    phone = models.CharField( _( 'Phone' ), max_length = DEFAULT_MAX_LENGTH, blank = True, null = True )
    fax = models.CharField( _( 'Fax' ), max_length = DEFAULT_MAX_LENGTH, blank = True, null = True )
    mobile = models.CharField( _( 'Mobile' ), max_length = DEFAULT_MAX_LENGTH, blank = True, null = True )
    email = models.EmailField( _( 'Email' ), blank = True, null = True )
    website = models.URLField( _( 'Website' ), verify_exists = False, blank = True, null = True )

    is_active = models.BooleanField( _( 'Active' ), default = True )
    is_twa_member = models.BooleanField( _( 'TWA Member' ), default = False )
    leader = models.ForeignKey( Person, verbose_name = _( 'Dojo Leader' ), related_name = 'dojo_leader', blank = True, null = True )
    association = models.ForeignKey( 'Association', verbose_name = _( 'Association' ), blank = True, null = True )

    objects = models.Manager()
    dojos = DojoManager()

    def get_absolute_url( self ):
        return '/dojo/%i/' % self.id

    def __repr__( self ):
        return self.__unicode__()

    def __unicode__( self ):
        name = u''
        if self.name_jp:
            name = self.name_jp
        if self.shortname:
            name = "%s %s" % ( name, self.shortname )
        elif self.city:
            name = "%s %s" % ( name, self.city )
        else:
            name = "%s %s" % ( name, self.name )
        return name.strip()

    class Meta:
        ordering = [ 'city', 'name' ]
        verbose_name = _( 'Dojo' )
        verbose_name_plural = _( 'Dojos' )

class Association( AbstractModel ):
    name = models.CharField( _( 'Name' ), max_length = DEFAULT_MAX_LENGTH, unique = True )
    shortname = models.CharField( _( 'Short Name' ), max_length = DEFAULT_MAX_LENGTH, blank = True, null = True )
    text = models.TextField( _( 'Text' ), blank = True, null = True )

    street = models.CharField( _( 'Street' ), max_length = DEFAULT_MAX_LENGTH, blank = True, null = True )
    zip = models.CharField( _( 'Zip' ), max_length = DEFAULT_MAX_LENGTH, blank = True, null = True )
    city = models.CharField( _( 'City' ), max_length = DEFAULT_MAX_LENGTH, blank = True, null = True )
    province = models.CharField( _( 'Province' ), max_length = DEFAULT_MAX_LENGTH, blank = True, null = True )
    country = models.ForeignKey( Country, verbose_name = _( 'Country' ) )

    phone = models.CharField( _( 'Phone' ), max_length = DEFAULT_MAX_LENGTH, blank = True, null = True )
    fax = models.CharField( _( 'Fax' ), max_length = DEFAULT_MAX_LENGTH, blank = True, null = True )
    mobile = models.CharField( _( 'Mobile' ), max_length = DEFAULT_MAX_LENGTH, blank = True, null = True )
    email = models.EmailField( _( 'Email' ), blank = True, null = True )
    website = models.URLField( _( 'Website' ), verify_exists = False, blank = True, null = True )

    is_active = models.BooleanField( _( 'Active' ), default = True )
    contact = models.ForeignKey( Person, verbose_name = _( 'Contact' ), related_name = 'association', blank = True, null = True )

    def get_dojos(self):
        return self.dojo_set.filter(public=True, is_active=True)

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
        return super( SuggestionsManager, self ).get_query_set().filter( is_active = True, public = True, person__is_active = True, person__public = True, is_nomination = True )

class GraduationManager( models.Manager ):
    def get_query_set( self ):
        return super( GraduationManager, self ).get_query_set().filter( is_active = True, public = True, person__is_active = True, person__public = True, is_nomination = False )

    def get_current( self, person ):
        try:
            return max( Graduation.objects.filter( person__id = person.id, is_active = True, public = True, is_nomination = False ).iterator() ).rank
        except:
            return None

    def get_this_years_graduations( self ):
        return self.get_query_set().filter( is_active = True, public = True, date__year = date.today().year, rank__gte = 100 )

class Graduation( AbstractModel ):
    person = models.ForeignKey( 'Person', verbose_name = _( 'Person' ), related_name = 'graduations' )
    nominated_by = models.ForeignKey( 'Person', verbose_name = _( 'Nominated By' ), related_name = 'nominations', blank = True, null = True )
    rank = models.IntegerField( _( 'Rank' ), choices = RANK )
    date = models.DateField( _( 'Date' ) )
    text = models.TextField( _( 'Text' ), blank = True, null = True )
    is_nomination = models.BooleanField( _( 'Nomination' ), default = False )
    request_doc = models.FileField( _( 'Request Document' ), storage = doc_file_system, upload_to = 'docs/', blank = True, null = True )
    confirmation_doc = models.FileField( _( 'Confirmation Document' ), storage = doc_file_system, upload_to = 'docs/', blank = True, null = True )
    payment_doc = models.FileField( _( 'Payment Document' ), storage = doc_file_system, upload_to = 'docs/', blank = True, null = True )
    is_active = models.BooleanField( _( 'Active' ), default = True )

    objects = models.Manager()
    graduations = GraduationManager()
    suggestions = SuggestionsManager()

    def __unicode__( self ):
        try:
            return self.get_rank_display()
        except:
            return ''

    def __cmp__( self, other ):
        return cmp( self.rank, other.rank )

    def get_absolute_url( self ):
        return '/member/%i/' % self.person.id

    class Meta:
        ordering = [ '-rank', '-date' ]
        get_latest_by = "date"
        verbose_name = _( 'Graduation' )
        verbose_name_plural = _( 'Graduations' )

class LicenseManager( models.Manager ):
    def get_query_set( self ):
        return super( LicenseManager, self ).get_query_set().filter( is_active = True, public = True, person__is_active = True, person__public = True )

    def get_requested_licenses( self ):
        return self.get_query_set().filter( is_active = True, public = True ).exclude( status = LICENSE_STATUS_LICENSED )#.exclude( status = LICENSE_STATUS_REJECTED )

    def get_granted_licenses( self ):
        return self.get_query_set().filter( status = LICENSE_STATUS_LICENSED, is_active = True, public = True ).order_by('-date')

    def get_public_licenses( self ):
        return self.get_granted_licenses().filter(person__public=True)

    def get_rejected_licenses( self ):
        return self.get_query_set().filter( status = LICENSE_STATUS_REJECTED, is_active = True, public = True )

class License( AbstractModel ):
    person = models.ForeignKey( Person, verbose_name = _( 'Person' ) )
    status = models.IntegerField( _( 'License Status' ), choices = LICENSE_STATUS, default = LICENSE_STATUS_OPEN )
    date = models.DateField( _( 'License Date' ), blank = True, null = True )
    request = models.DateField( _( 'License Request' ), blank = True, null = True )
    receipt = models.DateField( _( 'License Receipt' ), blank = True, null = True )
    rejected = models.DateField( _( 'License Rejected' ), blank = True, null = True )
    request_doc = models.FileField( _( 'License Request Document' ), storage = doc_file_system, upload_to = 'docs/', blank = True, null = True )
    receipt_doc = models.FileField( _( 'License Receipt Document' ), storage = doc_file_system, upload_to = 'docs/', blank = True, null = True )
    text = models.TextField( _( 'Text' ), blank = True, null = True )
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

class TWAMembershipManager( models.Manager ):
    def get_query_set( self ):
        return super( TWAMembershipManager, self ).get_query_set().filter( is_active = True, public = True, person__is_active = True, person__public = True )

    def get_requested_memberships( self ):
        return self.get_query_set().filter(status__gt=MEMBERSHIP_STATUS_EX)

    def get_next_id_for_country( self, country_code ):
        try:
            country = Country.objects.get( code = country_code )
            try:
                member_id = max( self.get_query_set().filter( twa_id_country = country ).values_list( 'twa_id_number', flat = True ) ) + 1
            except:
                member_id = 1
            return member_id
        except:
            return None

class TWAMembership( AbstractModel ):
    person = models.ForeignKey( Person, verbose_name = _( 'Person' ) )
    status = models.IntegerField( _( 'Membership Status' ), choices = MEMBERSHIP_STATUS, default = LICENSE_STATUS_OPEN )
    date = models.DateField( _( 'Membership Date' ), blank = True, null = True )
    passport_date = models.DateField( _( 'Passport Date' ), blank = True, null = True )
    request = models.DateField( _( 'Membership Request' ), blank = True, null = True )
    request_doc = models.FileField( _( 'Membership Request Document' ), storage = doc_file_system, upload_to = 'docs/', blank = True, null = True )
    text = models.TextField( _( 'Text' ), blank = True )
    twa_id_country = models.ForeignKey( Country, blank = True, null = True )
    twa_id_number = models.IntegerField( blank = True, null = True )
    is_active = models.BooleanField( _( 'Active' ), default = True )

    objects = TWAMembershipManager()

    def get_absolute_url( self ):
        return '/member/%i/' % self.person.id

    def payment( self ):
        try:
            return self.twapayment_set.latest( 'date' )
        except:
            return ''
    payment.short_description = _( 'Payment' )
    payment.allow_tags = False

    def twa_id( self ):
        if self.twa_id_country is None or self.twa_id_number is None:
            return ''
        try:
            return u'%s-%s'.strip() % ( self.twa_id_country.code, str( self.twa_id_number ).rjust( 5, '0' ) )
        except:
            return ''
    twa_id.short_description = _( 'TWA ID' )
    twa_id.allow_tags = False

    def __unicode__( self ):
        return u'%s %s'.strip() % ( self.twa_id(), self.person )

    class Meta:
        ordering = [ 'person__firstname', 'person__lastname' ]
        verbose_name = _( 'TWA Membership' )
        verbose_name_plural = _( 'TWA Membership' )

class TWAPaymentManager( models.Manager ):
    def get_query_set( self ):
        return super( TWAPaymentManager, self ).get_query_set().filter( public = True )

class TWAPayment( AbstractModel ):
    twa = models.ForeignKey( TWAMembership, verbose_name = _( 'TWA Membership' ) )
    date = models.DateField( _( 'Payment Date' ) )
    year = models.IntegerField(_('Payment for year'), default=datetime.now().year)
    cash = models.BooleanField( _( 'Cash' ), default = False )
    text = models.TextField( _( 'Text' ), blank = True, null = True )

    objects = TWAPaymentManager()

    def __unicode__( self ):
        return u'%s %s %s'.strip() % ( self.twa.twa_id(), self.twa.person, self.date )

    class Meta:
        ordering = [ 'date' ]
        verbose_name = _( 'TWA Payment' )
        verbose_name_plural = _( 'TWA Payment' )

class Document( AbstractModel ):
    name = models.CharField( _( 'Name' ), max_length = DEFAULT_MAX_LENGTH )
    file = models.FileField( _( 'File' ), storage = doc_file_system, upload_to = 'docs/' )
    person = models.ForeignKey( Person, verbose_name = _( 'Person' ), blank = True, null = True )

    def __unicode__( self ):
        return self.name

    class Meta:
        ordering = [ 'name' ]
        verbose_name = _( 'Document' )
        verbose_name_plural = _( 'Documents' )

class NewsManager( models.Manager ):
    def get_query_set( self ):
        return super( NewsManager, self ).get_query_set().filter( public = True, pub_date__lte = datetime.now() )

class News( AbstractModel ):
    title = models.CharField( _( 'Title' ), max_length = DEFAULT_MAX_LENGTH )
    title_en = models.CharField( _( 'Title' ), max_length = DEFAULT_MAX_LENGTH, blank=True )
    title_ja = models.CharField( _( 'Title' ), max_length = DEFAULT_MAX_LENGTH, blank=True )
    preview = models.TextField( _( 'Preview' ), blank = True )
    preview_en = models.TextField( _( 'Preview' ), blank = True )
    preview_ja = models.TextField( _( 'Preview' ), blank = True )
    text = models.TextField( _( 'Text' ), blank = True )
    text_en = models.TextField( _( 'Text' ), blank = True )
    text_ja = models.TextField( _( 'Text' ), blank = True )
    photo = models.ImageField( _( 'Photo' ), upload_to = 'images/', null = True, blank = True )
    pub_date = models.DateTimeField( _( 'Date' ), default = datetime.now() )

    objects = models.Manager()
    current_objects = NewsManager()

    def get_title(self, language=None):
        return getattr(self, "title_%s" % (language or translation.get_language()[:2]), "") or self.title
    get_title.short_description = _('Title')
    get_title.allow_tags = False

    def get_preview(self, language=None):
        return getattr(self, "preview_%s" % (language or translation.get_language()[:2]), "") or self.preview
    get_preview.short_description = _('Preview')
    get_preview.allow_tags = False

    def get_text(self, language=None):
        return getattr(self, "text_%s" % (language or translation.get_language()[:2]), "") or self.text
    get_text.short_description = _('Text')
    get_text.allow_tags = False

    def __unicode__( self ):
        return self.title

    def get_absolute_url( self ):
        return '/news/%i/' % self.id

    class Meta:
        ordering = [ '-pub_date', 'title' ]
        verbose_name = _( 'News' )
        verbose_name_plural = _( 'News' )

class Attachment( AbstractModel ):
    name = models.CharField( _( 'Name' ), max_length = DEFAULT_MAX_LENGTH )
    file = models.FileField( _( 'File' ), upload_to = 'attachments/' )
    news = models.ForeignKey( News, verbose_name = _( 'News' ), blank = True, null = True )

    def __unicode__( self ):
        return self.name

    class Meta:
        ordering = [ 'name' ]
        verbose_name = _( 'Attachment' )
        verbose_name_plural = _( 'Attachments' )

class DownloadManager( models.Manager ):
    def get_query_set( self ):
        return super( DownloadManager, self ).get_query_set().filter( public = True )

class Download( AbstractModel ):
    name = models.CharField( _( u'Name' ), max_length = DEFAULT_MAX_LENGTH, unique = True )
    text = models.TextField( _( u'Text' ), blank = True, null = True )
    datei = models.FileField( _( u'Path' ), upload_to = 'downloads/' )

    objects = models.Manager()
    public_objects = DownloadManager()

    def neu( self ):
        return ( datetime.now() - self.creation ).days < 14
    neu.short_description = _( u'New' )
    neu.allow_tags = False

    def __unicode__( self ):
        return u'%s %s'.strip() % ( self.name, self.datei )

    def get_absolute_url( self ):
        return '/downloads/'

    class Meta:
        ordering = ['name']
        verbose_name = _( u'Download' )
        verbose_name_plural = _( u'Downloads' )


class NewsFeed(Feed):
    title = 'tendo-world-aikido.de'
    link = '/feed/'
    feed_type = Atom1Feed
    description = _(u'Nachrichten vom Weltverband für Tendoryu Aikido')

    def items(self):
        return News.current_objects.all()[:10]