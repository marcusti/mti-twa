#-*- coding: utf-8 -*-

from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from members.csvutf8 import UnicodeReader
from members.models import TWAMembership, TWAPayment

def convert_date( s ):
    if s == 'None' or s == '':
        return None
    else:
        return datetime.strptime( s, '%d.%m.%Y' )

def import_payments():
    for line in UnicodeReader( open( 'payment.csv' ) ):
        rid, twaid, date_string = line[0], line[1], line[8]
        #countrycode, tid = twaid.split( '-' )

        try:
            #twa = TWAMembership.objects.get( twa_id_country__code = countrycode, twa_id_number = int( tid ) )
            twa = TWAMembership.objects.get( id = int( rid ) )
        except:
            twa = None
            print 'twa id nicht gefunden: %s' % ( twaid )

        try:
            date = convert_date( date_string )
        except Exception, ex:
            date = None
            print ex

        if twa and date:
            try:
                TWAPayment.objects.get( twa = twa, date = date )
                print 'Zahlung existiert schon: %s %s' % ( twa, date )
            except MultipleObjectsReturned:
                print 'es existieren schon mehrere Zahlungen: %s %s' % ( twa, date )
            except ObjectDoesNotExist:
                p = TWAPayment()
                p.twa = twa
                p.date = date
                p.save()
                print 'Zahlung gespeichert: %s' % p
