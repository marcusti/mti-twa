#-*- coding: utf-8 -*-

from datetime import datetime
from members.csvutf8 import UnicodeReader
from members.models import Country, Dojo, Graduation, Person

COL = ['ID', 'FIRSTNAME', 'LASTNAME', 'FIRSTNAME_JP', 'LASTNAME_JP', 'STREET', 'ZIP', 'CITY', 'COUNTRY', 'PHONE', 'FAX', 'MOBILE', 'EMAIL',
       'DOJO_ID', 'DOJO', 'AIKIDO_SINCE', 'KYU_5', 'KYU_4', 'KYU_3', 'KYU_2', 'KYU_1', 'DAN_1', 'DAN_2', 'DAN_3', 'DAN_4', 'DAN_5','DAN_6',
       'GENDER', 'BIRTH', 'PHOTO', 'TEXT']

def convert_date( s ):
    if s == 'None' or s == '':
        return None
    else:
        return datetime.strptime( s, '%Y-%m-%d' ).date()

def add_graduation( person, rank, date ):
    if date is None:
        return

    try:
        grad = person.graduations.filter( rank = rank ).latest()
        if not grad.date == date:
            grad.date = date
            grad.save()
            print 'graduation saved: %s, %s, %s' % ( person, grad, date )
    except:
        grad = Graduation( rank = rank, person = person, date = date )
        grad.save()
        print 'graduation created: %s, %s, %s' % ( person, grad, date )

def import_members():
    for line in UnicodeReader( open( 'members.csv' ) ):
        pid = line[COL.index( 'ID' )].strip()
        firstname = line[COL.index( 'FIRSTNAME' )].strip()
        lastname = line[COL.index( 'LASTNAME' )].strip()
        firstname_jp = line[COL.index( 'FIRSTNAME_JP' )].strip()
        lastname_jp = line[COL.index( 'LASTNAME_JP' )].strip()

        try:
            # try to find a person by id
            person = Person.objects.get( id = int( pid ) )
            print 'person found by ID: id=%s, %s' % ( person.id, person )
        except:
            try:
                # try to find a person by name
                person = Person.objects.get( firstname = firstname, lastname = lastname, firstname_jp = firstname_jp, lastname_jp = lastname_jp )
                print 'person found by name: id=%s, %s' % ( person.id, person )
            except:
                if pid.strip() == '':
                    person = Person( firstname = firstname, lastname = lastname, firstname_jp = firstname_jp, lastname_jp = lastname_jp )
                    person.save()
                    print 'person created: %s' % ( person )
                else:
                    person = None
                    print 'person not found: %s' % ( pid )
                    continue

        person.street = line[COL.index( 'STREET' )].strip()
        person.zip = line[COL.index( 'ZIP' )].strip()
        person.city = line[COL.index( 'CITY' )].strip()

        countrycode = line[COL.index( 'COUNTRY' )].strip()
        try:
            country = Country.objects.get( code = countrycode )
        except:
            country = None
            print 'country not found: %s' % ( countrycode )
        person.country = country

        person.phone = line[COL.index( 'PHONE' )].strip()
        person.fax = line[COL.index( 'FAX' )].strip()
        person.mobile = line[COL.index( 'MOBILE' )].strip()
        person.email = line[COL.index( 'EMAIL' )].strip()

        dojo_id = line[COL.index( 'DOJO_ID' )].strip()
        dojo_name = line[COL.index( 'DOJO' )].strip()
        try:
            dojo = Dojo.dojos.get( id = int( dojo_id ) )
        except:
            try:
                dojo = Dojo.dojos.get( name = dojo_name )
            except:
                dojo = Dojo( name = dojo_name )
                if country:
                    dojo.country = country
                dojo.save()
                print 'dojo created: %s, %s' % ( dojo.id, dojo.name )

        if not dojo in person.dojos.all():
            person.dojos.add( dojo )
            print '%s added to dojo %s' % ( person, dojo )


        aikido_since = convert_date( line[COL.index( 'AIKIDO_SINCE' )].strip() )
        if aikido_since and not person.aikido_since == aikido_since:
            person.aikido_since = aikido_since
            print '%s practices aikido since %s' % ( person, aikido_since )

        add_graduation( person, 10, convert_date( line[COL.index( 'KYU_5' )].strip() ) )
        add_graduation( person, 20, convert_date( line[COL.index( 'KYU_4' )].strip() ) )
        add_graduation( person, 30, convert_date( line[COL.index( 'KYU_3' )].strip() ) )
        add_graduation( person, 40, convert_date( line[COL.index( 'KYU_2' )].strip() ) )
        add_graduation( person, 50, convert_date( line[COL.index( 'KYU_1' )].strip() ) )
        add_graduation( person, 100, convert_date( line[COL.index( 'DAN_1' )].strip() ) )
        add_graduation( person, 200, convert_date( line[COL.index( 'DAN_2' )].strip() ) )
        add_graduation( person, 300, convert_date( line[COL.index( 'DAN_3' )].strip() ) )
        add_graduation( person, 400, convert_date( line[COL.index( 'DAN_4' )].strip() ) )
        add_graduation( person, 500, convert_date( line[COL.index( 'DAN_5' )].strip() ) )
        add_graduation( person, 600, convert_date( line[COL.index( 'DAN_6' )].strip() ) )

        person.gender = line[COL.index( 'GENDER' )].strip()
        person.birth = convert_date( line[COL.index( 'BIRTH' )].strip() )

        foto = line[COL.index( 'PHOTO' )].strip()

        person.save()

        print
