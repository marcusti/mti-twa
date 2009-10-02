#-*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.utils.translation import ugettext_lazy as _
from twa.members.models import *

admin.site.disable_action( 'delete_selected' )

class TranslationAdmin( admin.ModelAdmin ):
    ordering = [ 'name' ]

class CountryAdmin( admin.ModelAdmin ):
    ordering = [ 'name' ]
    list_display = ( 'id', 'name', 'name_de', 'name_ja', 'code' )
    list_display_links = ( 'name', 'name_de', 'name_ja' )

class GraduationInline( admin.StackedInline ):
    model = Graduation
    fk_name = 'person'
    extra = 1

class TWAPaymentInline( admin.StackedInline ):
    model = TWAPayment
    fk_name = 'twa'
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
    search_fields = [ 'id', 'city', 'name', 'leader__firstname' ]

class AssociationAdmin( admin.ModelAdmin ):
    ordering = [ 'country', 'province', 'name' ]
    list_display = ( 'id', 'name', 'contact', 'is_active' )
    list_display_links = ( 'name', )
    list_filter = ( 'is_active', 'country', )
    search_fields = [ 'id', 'name', 'shortname', 'city', 'text' ]

class GraduationAdmin( admin.ModelAdmin ):
    ordering = [ '-date', '-rank' ]
    list_display = ( 'id', 'rank', 'person', 'date', 'text', 'is_nomination', 'nominated_by', 'is_active', 'last_modified' )
    list_display_links = ( 'person', 'rank', )
    list_filter = ( 'is_active', 'is_nomination', 'rank', 'person' )
    date_hierarchy = 'date'
    search_fields = [ 'id', 'text' ]

class LicenseAdmin( admin.ModelAdmin ):
    ordering = [ '-id' ]
    list_display = ( 'id', 'status', 'person', 'date', 'request', 'receipt', 'rejected', 'is_active' )
    list_display_links = ( 'status', 'person' )
    list_filter = [ 'status', 'is_active' ]
    date_hierarchy = 'date'
    search_fields = [ 'person__firstname', 'person__nickname', 'person__lastname' ]

class MembershipAdmin( admin.ModelAdmin ):
    ordering = [ '-id' ]
    list_display = ( 'id', 'twa_id', 'status', 'person', 'date', 'request', 'request_doc', 'is_active' )
    list_display_links = ( 'status', 'person' )
    list_filter = [ 'status', 'is_active', 'twa_id_country' ]
    date_hierarchy = 'request'
    search_fields = [ 'person__firstname', 'person__nickname', 'person__lastname', 'person__country__name' ]
    inlines = [ TWAPaymentInline, ]
    actions = [ 'set_status_open','set_status_accepted','set_status_confirmed','set_status_to_be_confirmed','set_status_rejected',
               'set_status_verify','set_status_member' ]

    def set_status_open( self, request, queryset ):
        queryset.update( status = MEMBERSHIP_STATUS_OPEN )
    set_status_open.short_description = _( 'Set selected members to status "open"' )

    def set_status_accepted( self, request, queryset ):
        queryset.update( status = MEMBERSHIP_STATUS_ACCEPTED )
    set_status_accepted.short_description = _( 'Set selected members to status "accepted"' )

    def set_status_confirmed( self, request, queryset ):
        queryset.update( status = MEMBERSHIP_STATUS_CONFIRMED )
    set_status_confirmed.short_description = _( 'Set selected members to status "confirmed"' )

    def set_status_to_be_confirmed( self, request, queryset ):
        queryset.update( status = MEMBERSHIP_STATUS_TO_BE_CONFIRMED )
    set_status_to_be_confirmed.short_description = _( 'Set selected members to status "to be confirmed"' )

    def set_status_rejected( self, request, queryset ):
        queryset.update( status = MEMBERSHIP_STATUS_REJECTED )
    set_status_rejected.short_description = _( 'Set selected members to status "rejected"' )

    def set_status_verify( self, request, queryset ):
        queryset.update( status = MEMBERSHIP_STATUS_VERIFY )
    set_status_verify.short_description = _( 'Set selected members to status "verify"' )

    def set_status_member( self, request, queryset ):
        queryset.update( status = MEMBERSHIP_STATUS_MEMBER )
    set_status_member.short_description = _( 'Set selected members to status "member"' )

class TWAPaymentAdmin( admin.ModelAdmin ):
    ordering = [ '-date' ]
    list_display = ( 'id', 'twa', 'date', 'cash', 'text' )
    list_display_links = ( 'twa', 'date' )
    list_filter = [ 'date' ]
    date_hierarchy = 'date'
    search_fields = [ 'twa__twa_id_number', 'twa__person__firstname', 'twa__person__nickname', 'twa__person__lastname', 'text' ]

class DocumentAdmin( admin.ModelAdmin ):
    ordering = [ 'name' ]
    list_display = ( 'id', 'name', 'file', 'person' )
    list_display_links = ( 'name', 'file', )

class NewsAdmin( admin.ModelAdmin ):
    ordering = [ '-pub_date', 'title' ]
    list_display = ( 'id', 'title', 'pub_date', 'last_modified', 'public' )
    list_display_links = ( 'title', )
    date_hierarchy = 'pub_date'
    search_fields = [ 'title', 'text' ]

class DownloadAdmin( admin.ModelAdmin ):
    ordering = [ 'name' ]
    list_display = ( 'id', 'name', 'datei', 'public', 'last_modified' )
    list_display_links = ( 'name', )
    search_fields = [ 'name', 'text', 'datei' ]

class LogEntryAdmin( admin.ModelAdmin ):
    ordering = [ '-action_time' ]
    list_display = ( 'action_time', 'user', 'content_type', 'object_repr', 'change_message', 'is_addition', 'is_change', 'is_deletion' )
    list_filter = [ 'user' ]

admin.site.register( Document, DocumentAdmin )
admin.site.register( License, LicenseAdmin )
admin.site.register( TWAMembership, MembershipAdmin )
admin.site.register( TWAPayment, TWAPaymentAdmin )
admin.site.register( Graduation, GraduationAdmin )
admin.site.register( Association, AssociationAdmin )
admin.site.register( Dojo, DojoAdmin )
admin.site.register( Person, PersonAdmin )
admin.site.register( Country, CountryAdmin )
#admin.site.register( Translation, TranslationAdmin )
admin.site.register( News, NewsAdmin )
admin.site.register( Download, DownloadAdmin )
admin.site.register( LogEntry, LogEntryAdmin )
