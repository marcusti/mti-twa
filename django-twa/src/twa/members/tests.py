#-*- coding: utf-8 -*-

import unittest
from datetime import datetime
from twa.members.models import Country, Person, TWAMembership

class TWATestCase( unittest.TestCase ):
    def setUp( self ):
        self.de, created = Country.objects.get_or_create( name = "Deutschland", code = "DE")
        self.heinrich, created = Person.objects.get_or_create( firstname = "Heinrich", lastname = "Heine" )

    def testPerson( self ):
        self.failIf( self.heinrich is None )
        self.assertEquals( self.heinrich.firstname, "Heinrich")
        self.assertEquals( self.heinrich.lastname, "Heine")
        self.assertEquals( self.heinrich.current_rank(), "")

    def testMembership( self ):
        ms = TWAMembership.objects.create( person = self.heinrich )
        self.failIf( ms is None )
        self.failIf( self.heinrich.is_member() )

        ms = TWAMembership.objects.create( person = self.heinrich, status = 5, twa_id_country = self.de, twa_id_number = 1 )
        self.failIf( ms is None )
        self.assertEquals( self.heinrich.twamembership_set.all().count(), 2)
        self.failUnless( ms.person_id == self.heinrich.id )
        self.failUnless( self.heinrich.is_member() )
       
