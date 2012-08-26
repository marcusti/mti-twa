#-*- coding: utf-8 -*-

from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from members.csvutf8 import UnicodeReader
from members.models import TWAMembership, TWAPayment, MEMBERSHIP_STATUS_MEMBER

def convert_date( s ):
    if s == 'None' or s == '':
        return None
    else:
        # return datetime.strptime( s, '%d.%m.%Y' )
        return datetime.strptime( s, '%Y-%m-%d' )

def import_payments():
    existing_payments = 0
    new_payments = 0
    new_members = 0
    YEAR = 2010

    for line in UnicodeReader( open( 'payments.csv' ) ):
        rid, twaid, member_date_string, payment_date_string = line[0], line[2], line[12], line[14]
        #countrycode, tid = twaid.split( '-' )

        try:
            #twa = TWAMembership.objects.get( twa_id_country__code = countrycode, twa_id_number = int( tid ) )
            twa = TWAMembership.objects.get( id = int( rid ) )
        except:
            twa = None
            #print 'twa id nicht gefunden: %s' % ( twaid )
            print 'rid nicht gefunden: %s' % ( rid )

        try:
            payment_date = convert_date( payment_date_string )
        except Exception, ex:
            payment_date = None
            print ex

        if twa and payment_date:
            try:
                TWAPayment.objects.get( twa = twa, date = payment_date, year = YEAR )
                existing_payments += 1
                print '[Zahlung existiert schon: %s %s]' % ( twa, payment_date )
            except MultipleObjectsReturned:
                existing_payments += 1
                print '[es existieren schon mehrere Zahlungen: %s %s]' % ( twa, payment_date )
            except ObjectDoesNotExist:
                p = TWAPayment()
                p.twa = twa
                p.date = payment_date
                p.year = YEAR
                p.save()
                new_payments += 1
                print 'Zahlung gespeichert: %s' % p

        try:
            member_date = convert_date( member_date_string )
        except Exception, ex:
            member_date = None
            print ex

        if twa and member_date:
            if not twa.date == member_date.date():
                twa.date = member_date
                twa.status = MEMBERSHIP_STATUS_MEMBER
                twa.save()
                new_members += 1
                print '%s ist nun Mitglied seit %s' % ( twa.person, member_date )

    print
    print '%s neue Zahlungen importiert' % ( new_payments )
    print '%s neue MEMBER_SINCE-Daten importiert' % ( new_members )
