#-*- coding: utf-8 -*-

import unittest
from datetime import datetime
from twa.members.models import *

class TWATestCase( unittest.TestCase ):
    def setUp( self ):
        self.de, created = Country.objects.get_or_create( name = "Deutschland", code = "DE")
        self.heinrich, created = Person.objects.get_or_create( firstname = "Heinrich", lastname = "Heine", country = self.de )
        self.akz, created = Person.objects.get_or_create( firstname = "Alfons", lastname = "Akzeptiert", country = self.de )

    def testPerson( self ):
        self.failIf( self.heinrich is None )
        self.assertEquals( self.heinrich.firstname, "Heinrich")
        self.assertEquals( self.heinrich.lastname, "Heine")

    def testNonMembership( self ):
        ms = TWAMembership( person = self.heinrich )
        self.failIf( ms is None )
        self.assertTrue( ms.status == MEMBERSHIP_STATUS_OPEN )

    def testMembership( self ):
        ms1 = TWAMembership.objects.create( person = self.heinrich, status = MEMBERSHIP_STATUS_MEMBER )
        self.failIf( ms1 is None )
        self.assertEquals( self.heinrich.twamembership_set.all().count(), 1 )
        self.assertTrue( ms1.person_id == self.heinrich.id )
        self.assertTrue( self.heinrich.is_member() )

