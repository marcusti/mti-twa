#-*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.admin.models import LogEntry
from twa.members.models import *

class TranslationAdmin( admin.ModelAdmin):
    ordering = [ 'name' ]
    
class CountryAdmin( admin.ModelAdmin ):
    ordering = [ 'name' ]
    list_display = ( 'name', 'name_de', 'name_ja', 'code' )
    list_display_links = ( 'name', 'name_de', 'name_ja' )

class GraduationInline( admin.StackedInline ):
    model = Graduation
    fk_name = 'person'
    extra = 1

class PersonAdmin( admin.ModelAdmin ):
    ordering = [ 'firstname', 'lastname' ]
    list_display = ( 'id', 'firstname', 'lastname', 'current_rank', 'age', 'days', 'gender', 'photo', 'is_active', 'admin_thumb' )
    list_display_links = ( 'firstname', 'lastname', 'admin_thumb' )
    list_filter = ( 'is_active', 'dojos' )
    search_fields = [ 'id', 'firstname', 'lastname', 'city' ]
    filter_horizontal = ( 'dojos', )
    inlines = [ GraduationInline, ]

class DojoAdmin( admin.ModelAdmin ):
    ordering = [ 'shortname', 'city', 'name' ]
    list_display = ( 'id', 'city', 'name', 'leader', 'is_active', 'is_twa_member' )
    list_display_links = ( 'name', )
    list_filter = ( 'is_active', 'country', )
    search_fields = [ 'id', 'firstname', 'lastname', 'city' ]

class AssociationAdmin( admin.ModelAdmin ):
    ordering = [ 'country', 'province', 'name' ]
    list_display = ( 'id', 'name', 'contact', 'is_active' )
    list_display_links = ( 'name', )
    list_filter = ( 'is_active', 'country', )
    search_fields = [ 'id', 'name', 'shortname', 'city', 'text' ]

class GraduationAdmin( admin.ModelAdmin ):
    ordering = [ '-date', '-rank' ]
    list_display = ( 'id', 'rank', 'person', 'date', 'text', 'is_nomination', 'nominated_by', 'is_active' )
    list_display_links = ( 'person', 'rank', )
    list_filter = ( 'is_active', 'is_nomination', 'rank', 'person' )
    search_fields = [ 'id', 'text' ]

class LicenseAdmin( admin.ModelAdmin ):
    ordering = [ '-id' ]
    list_display = ( 'id', 'status', 'person', 'date', 'request', 'receipt', 'rejected', 'is_active' )
    list_display_links = ( 'status', 'person' )
    list_filter = [ 'status', 'is_active' ]
    search_fields = [ 'person__firstname', 'person__nickname', 'person__lastname' ]

class MembershipAdmin( admin.ModelAdmin ):
    ordering = [ '-id' ]
    list_display = ( 'id', 'status', 'person', 'date', 'request', 'receipt', 'rejected', 'is_active' )
    list_display_links = ( 'status', 'person' )
    list_filter = [ 'status', 'is_active' ]
    search_fields = [ 'person__firstname', 'person__nickname', 'person__lastname' ]

class DocumentAdmin( admin.ModelAdmin ):
    ordering = [ 'name' ]
    list_display = ( 'id', 'name', 'file', 'person' )
    list_display_links = ( 'name', 'file', )

class LogEntryAdmin( admin.ModelAdmin ):
    ordering = [ '-action_time' ]
    list_display = ( 'action_time', 'user', 'content_type', 'object_repr', 'change_message', 'is_addition', 'is_change', 'is_deletion' )
    list_filter = [ 'user' ]

admin.site.register( Document, DocumentAdmin )
admin.site.register( License, LicenseAdmin )
admin.site.register( TWAMembership, MembershipAdmin )
admin.site.register( Graduation, GraduationAdmin )
admin.site.register( Association, AssociationAdmin )
admin.site.register( Dojo, DojoAdmin )
admin.site.register( Person, PersonAdmin )
admin.site.register( Country, CountryAdmin )
#admin.site.register( Translation, TranslationAdmin )
admin.site.register( LogEntry, LogEntryAdmin )
