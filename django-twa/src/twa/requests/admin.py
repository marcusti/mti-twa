#-*- coding: utf-8 -*-

from django.contrib import admin
from twa.requests.models import *

class RequestAdmin( admin.ModelAdmin):
    ordering = [ '-created' ]
    list_display = ( 'user_agent', 'user', 'path', 'remote', 'created' )
    list_display_links = ( 'user_agent', 'user' )
    
admin.site.register( Request, RequestAdmin )
