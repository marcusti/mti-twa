from datetime import datetime
from models import GENDER, Country, Dojo, Person, Graduation
import csv, os, sys

def convert_date( s ):
    if s == 'None' or s == '':
        return None
    else:
        return datetime.strptime( s, '%Y-%m-%d' )

def convert_date_time( s ):
    if s == 'None' or s == '':
        return None
    else:
        return datetime.strptime( s, '%Y-%m-%d %H:%M:%S' )

def convert_gender( g ):
    if g == 'M':
        return 'm'
    elif g == 'W':
        return 'f'
    else:
        return ''

class Import:
    def __init__( self ):
        filename = os.path.join( os.getcwd(), 'mitglieder.csv' )
        print 'importing...', filename
        for row in csv.DictReader( open( filename ) ):
            p = Person( id = row['id'] )
            p.firstname = row['vorname']
            p.lastname = row['nachname']
            p.street = row['strasse']
            p.zip = row['plz']
            p.city = row['ort']
            p.phone = row['festnetz']
            p.fax = row['fax']
            p.mobile = row['handy']
            p.email = row['email']
            p.website = row['web']
            p.birth = convert_date( row['geburt'] )
            p.gender = convert_gender( row['geschlecht'] )
            p.is_active = row['aktiv']
            p.aikido_since = convert_date( row['aikido_seit'] )
            p.text_beirat = row['text']
            p.photo = row['bild'].replace( 'mitglieder', 'photos' )
            p.save()

        filename = os.path.join( os.getcwd(), 'dojos.csv' )
        print 'importing...', filename
        for row in csv.DictReader( open( filename ) ):
            d = Dojo( id = row['id'] )
            d.name = row['name']
            d.shortname = row['kurz']
            d.street = row['strasse']
            d.zip = row['plz']
            d.city = row['ort']
            d.phone = row['telefon']
            d.email = row['email']
            d.website = row['web']
            d.text = row['text']
            d.created = convert_date_time( row['creation'] )
            d.last_modified = convert_date_time( row['modified'] )
            d.save()

        filename = os.path.join( os.getcwd(), 'members.csv' )
        print 'importing...', filename
        for row in csv.DictReader( open( filename ) ):
            dojo = Dojo.objects.get( id = row['dojo_id'] )
            person = Person.objects.get( id = row['person_id'] )
            person.dojos.add( dojo )
            person.save()

        filename = os.path.join( os.getcwd(), 'graduierungen.csv' )
        print 'importing...', filename
        for row in csv.DictReader( open( filename ) ):
            g = Graduation( id = row['id'] )
            g.rank = row['grad']
            g.date = convert_date( row['datum'] )
            g.person = Person.objects.get( id = row['graduierter'] )
            g.text = row['text']
            g.is_nomination = row['vorschlag']
            g.save()

        deu = Country( name='Deutschland' )
        deu.save()

        for dojo in Dojo.objects.all():
            dojo.country = deu
            dojo.save()
