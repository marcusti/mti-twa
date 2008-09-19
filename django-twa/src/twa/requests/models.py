#-*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

DEFAULT_MAX_LENGTH = 200

class RequestManager( models.Manager ):
    def get_query_set( self ):
        return super( RequestManager, self ).get_query_set()

    def get_user_agents( self ):
        return self.get_query_set().values( 'user_agent' ).distinct()

    def get_user_agents_by_requests( self ):
        agents = []
        for ua in self.get_user_agents():
            agents.append( { 'count': self.get_query_set().filter( user_agent = ua['user_agent'] ).count(), 'user_agent': ua['user_agent'] } )
        #agents.append( { 'user_agent': '[all requests]', 'count': self.get_query_set().count() } )
        return agents

class Request( models.Model ):
    user = models.CharField( 'User', max_length = DEFAULT_MAX_LENGTH, blank = True )
    user_agent = models.CharField( 'User Agent', max_length = 500, blank = True )
    path = models.CharField( 'Path', max_length = DEFAULT_MAX_LENGTH, blank = True )
    remote = models.CharField( 'Remote', max_length = DEFAULT_MAX_LENGTH, blank = True )

    created = models.DateTimeField( _( 'Created' ), auto_now_add = True )
    last_modified = models.DateTimeField( _( 'Last Modified' ), auto_now = True )

    objects = RequestManager()

