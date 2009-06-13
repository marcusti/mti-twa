#-*- coding: utf-8 -*-

from django.db import connection, models
from django.utils.translation import ugettext_lazy as _
from twa.utils import DEFAULT_MAX_LENGTH, AbstractModel

class RequestManager( models.Manager ):
    def get_query_set( self ):
        return super( RequestManager, self ).get_query_set()

    def get_user_agents_top_10( self ):
        SQL = 'select count(*) as c, user_agent from requests_request group by user_agent order by c desc limit 10'
        cursor = connection.cursor()
        cursor.execute( SQL )
        agents = []
        for i in range( cursor.rowcount ):
            row = cursor.fetchone()
            agents.append( { 'count': row[0], 'user_agent': row[1] } )
        cursor.close()
        return agents

#        Django 1.1
#        from django.db.models import Count
#        return self.get_query_set().values( 'user_agent' ).annotate( agent_count = Count( 'user_agent' ) ).order_by( '-agent_count' )[:10]

class Request( AbstractModel ):
    user = models.CharField( _( 'User' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    user_agent = models.CharField( _( 'User Agent' ), max_length = 500, blank = True )
    path = models.CharField( _( 'Path' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    remote = models.CharField( _( 'Remote' ), max_length = DEFAULT_MAX_LENGTH, blank = True )

    objects = RequestManager()

    def __unicode__( self ):
        return self.user_agent
