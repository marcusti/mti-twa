#-*- coding: utf-8 -*-

from django.core import mail
from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client

from twa.members.models import *

class TWATestCase( TestCase ):
    def setUp( self ):
        self.de, created = Country.objects.get_or_create( name = "Deutschland", code = "DE" )
        self.heinrich, created = Person.objects.get_or_create( firstname = "Heinrich", lastname = "Heine", email='heinrich@example.com', country = self.de )
        self.akz, created = Person.objects.get_or_create( firstname = "Alfons", lastname = "Akzeptiert", country = self.de )
        self.client = Client()

    def testPerson( self ):
        self.failIf( self.heinrich is None )
        self.assertEquals( self.heinrich.firstname, "Heinrich" )
        self.assertEquals( self.heinrich.lastname, "Heine" )

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

    def testConfirmationEmail(self):
        user = User.objects.create_user('foo', '', 'bar')
        user.is_superuser = True
        user.save()

        # login
        self.assertTrue(self.client.login(username='foo', password='bar'))

        # create membership request
        member = TWAMembership(person=self.heinrich)
        member.status = MEMBERSHIP_STATUS_ACCEPTED
        member.save()

        # create twa ids
        response = self.client.get('/member-requests/twa-ids/')
        self.failUnlessEqual(response.status_code, 200)

        # send email
        response = self.client.get('/member-requests/confirmation-email/')
        self.failUnlessEqual(response.status_code, 200)

        self.assertEquals(len(mail.outbox), 1)

        for email in mail.outbox:
            print email.body
