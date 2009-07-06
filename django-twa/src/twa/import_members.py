#-*- coding: utf-8 -*-

from datetime import datetime
from members.csvutf8 import UnicodeReader
from members.models import Country, Dojo, Graduation, Person

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
        pid, firstname, lastname = line[0].strip(), line[1].strip(), line[2].strip()

        try:
            # try to find a person by id
            person = Person.objects.get( id = int( pid ) )
            print 'person found by ID: id=%s, %s' % ( person.id, person )
        except:
            try:
                # try to find a person by name
                person = Person.objects.get( firstname = firstname, lastname = lastname )
                print 'person found by name: id=%s, %s' % ( person.id, person )
            except:
                if pid.strip() == '':
                    person = Person( firstname = firstname, lastname = lastname )
                    person.save()
                    print 'person created: %s' % ( person )
                else:
                    person = None
                    print 'person not found: %s' % ( pid )

        if person is None:
            continue

        person.street = line[3].strip()
        person.zip = line[4].strip()
        person.city = line[5].strip()

        countrycode = line[6].strip()
        try:
            country = Country.objects.get( code = countrycode )
        except:
            country = None
            print 'country not found: %s' % ( countrycode )
        person.country = country

        person.phone = line[7].strip()
        person.fax = line[8].strip()
        person.mobile = line[9].strip()
        person.email = line[10].strip()

        dojo_id = line[11].strip()
        dojo_name = line[12].strip()
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


        aikido_since = convert_date( line[13].strip() )
        if aikido_since and not person.aikido_since == aikido_since:
            person.aikido_since = aikido_since
            print '%s practices aikido since %s' % ( person, aikido_since )

        add_graduation( person, 10, convert_date( line[14].strip() ) )
        add_graduation( person, 20, convert_date( line[15].strip() ) )
        add_graduation( person, 30, convert_date( line[16].strip() ) )
        add_graduation( person, 40, convert_date( line[17].strip() ) )
        add_graduation( person, 50, convert_date( line[18].strip() ) )
        add_graduation( person, 100, convert_date( line[19].strip() ) )
        add_graduation( person, 200, convert_date( line[20].strip() ) )
        add_graduation( person, 300, convert_date( line[21].strip() ) )
        add_graduation( person, 400, convert_date( line[22].strip() ) )
        add_graduation( person, 500, convert_date( line[23].strip() ) )

        person.gender = line[24].strip()
        person.birth = convert_date( line[25].strip() )

        foto = line[26].strip()

        person.save()
        
        print
