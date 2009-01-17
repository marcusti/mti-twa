#-*- coding: utf-8 -*-

import unittest
from datetime import datetime
from twa.members.models import *

class TWATestCase( unittest.TestCase ):
    def setUp( self ):
        self.de, created = Country.objects.get_or_create( name = "Deutschland", code = "DE")
        self.heinrich, created = Person.objects.get_or_create( firstname = "Heinrich", lastname = "Heine" )

    def testPerson( self ):
        self.failIf( self.heinrich is None )
        self.assertEquals( self.heinrich.firstname, "Heinrich")
        self.assertEquals( self.heinrich.lastname, "Heine")

    def testNonMembership( self ):
        ms = TWAMembership( person = self.heinrich )
        self.failIf( ms is None )
        self.assertTrue( ms.status == MEMBERSHIP_STATUS_OPEN )

    def testMembership( self ):
        ms = TWAMembership.objects.create( person = self.heinrich, status = MEMBERSHIP_STATUS_MEMBER, twa_id_country = self.de, twa_id_number = 1 )
        self.failIf( ms is None )
        self.assertEquals( self.heinrich.twamembership_set.all().count(), 1 )
        self.assertEquals( TWAMembership.objects.get_next_id_for_country( self.de.code ), 2 )
        self.assertTrue( ms.person_id == self.heinrich.id )
        self.assertTrue( self.heinrich.is_member() )
