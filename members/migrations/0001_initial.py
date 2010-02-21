#-*- coding: utf-8 -*-

from south.db import db
from django.db import models
from twa.members.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'TWAMembership'
        db.create_table('members_twamembership', (
            ('id', orm['members.TWAMembership:id']),
            ('public', orm['members.TWAMembership:public']),
            ('created', orm['members.TWAMembership:created']),
            ('last_modified', orm['members.TWAMembership:last_modified']),
            ('person', orm['members.TWAMembership:person']),
            ('status', orm['members.TWAMembership:status']),
            ('date', orm['members.TWAMembership:date']),
            ('request', orm['members.TWAMembership:request']),
            ('request_doc', orm['members.TWAMembership:request_doc']),
            ('text', orm['members.TWAMembership:text']),
            ('twa_id_country', orm['members.TWAMembership:twa_id_country']),
            ('twa_id_number', orm['members.TWAMembership:twa_id_number']),
            ('is_active', orm['members.TWAMembership:is_active']),
        ))
        db.send_create_signal('members', ['TWAMembership'])
        
        # Adding model 'Association'
        db.create_table('members_association', (
            ('id', orm['members.Association:id']),
            ('public', orm['members.Association:public']),
            ('created', orm['members.Association:created']),
            ('last_modified', orm['members.Association:last_modified']),
            ('name', orm['members.Association:name']),
            ('shortname', orm['members.Association:shortname']),
            ('text', orm['members.Association:text']),
            ('street', orm['members.Association:street']),
            ('zip', orm['members.Association:zip']),
            ('city', orm['members.Association:city']),
            ('province', orm['members.Association:province']),
            ('country', orm['members.Association:country']),
            ('phone', orm['members.Association:phone']),
            ('fax', orm['members.Association:fax']),
            ('mobile', orm['members.Association:mobile']),
            ('email', orm['members.Association:email']),
            ('website', orm['members.Association:website']),
            ('is_active', orm['members.Association:is_active']),
            ('contact', orm['members.Association:contact']),
        ))
        db.send_create_signal('members', ['Association'])
        
        # Adding model 'Document'
        db.create_table('members_document', (
            ('id', orm['members.Document:id']),
            ('public', orm['members.Document:public']),
            ('created', orm['members.Document:created']),
            ('last_modified', orm['members.Document:last_modified']),
            ('name', orm['members.Document:name']),
            ('file', orm['members.Document:file']),
            ('person', orm['members.Document:person']),
        ))
        db.send_create_signal('members', ['Document'])
        
        # Adding model 'News'
        db.create_table('members_news', (
            ('id', orm['members.News:id']),
            ('public', orm['members.News:public']),
            ('created', orm['members.News:created']),
            ('last_modified', orm['members.News:last_modified']),
            ('title', orm['members.News:title']),
            ('preview', orm['members.News:preview']),
            ('text', orm['members.News:text']),
            ('photo', orm['members.News:photo']),
            ('pub_date', orm['members.News:pub_date']),
        ))
        db.send_create_signal('members', ['News'])
        
        # Adding model 'Person'
        db.create_table('members_person', (
            ('id', orm['members.Person:id']),
            ('public', orm['members.Person:public']),
            ('created', orm['members.Person:created']),
            ('last_modified', orm['members.Person:last_modified']),
            ('firstname', orm['members.Person:firstname']),
            ('lastname', orm['members.Person:lastname']),
            ('nickname', orm['members.Person:nickname']),
            ('firstname_jp', orm['members.Person:firstname_jp']),
            ('lastname_jp', orm['members.Person:lastname_jp']),
            ('name_prefix', orm['members.Person:name_prefix']),
            ('text', orm['members.Person:text']),
            ('text_beirat', orm['members.Person:text_beirat']),
            ('photo', orm['members.Person:photo']),
            ('street', orm['members.Person:street']),
            ('zip', orm['members.Person:zip']),
            ('city', orm['members.Person:city']),
            ('country', orm['members.Person:country']),
            ('phone', orm['members.Person:phone']),
            ('fax', orm['members.Person:fax']),
            ('mobile', orm['members.Person:mobile']),
            ('email', orm['members.Person:email']),
            ('website', orm['members.Person:website']),
            ('birth', orm['members.Person:birth']),
            ('birth_sort_string', orm['members.Person:birth_sort_string']),
            ('gender', orm['members.Person:gender']),
            ('is_active', orm['members.Person:is_active']),
            ('aikido_since', orm['members.Person:aikido_since']),
        ))
        db.send_create_signal('members', ['Person'])
        
        # Adding model 'Download'
        db.create_table('members_download', (
            ('id', orm['members.Download:id']),
            ('public', orm['members.Download:public']),
            ('created', orm['members.Download:created']),
            ('last_modified', orm['members.Download:last_modified']),
            ('name', orm['members.Download:name']),
            ('text', orm['members.Download:text']),
            ('datei', orm['members.Download:datei']),
        ))
        db.send_create_signal('members', ['Download'])
        
        # Adding model 'Country'
        db.create_table('members_country', (
            ('id', orm['members.Country:id']),
            ('public', orm['members.Country:public']),
            ('created', orm['members.Country:created']),
            ('last_modified', orm['members.Country:last_modified']),
            ('name', orm['members.Country:name']),
            ('code', orm['members.Country:code']),
            ('name_de', orm['members.Country:name_de']),
            ('name_ja', orm['members.Country:name_ja']),
        ))
        db.send_create_signal('members', ['Country'])
        
        # Adding model 'Graduation'
        db.create_table('members_graduation', (
            ('id', orm['members.Graduation:id']),
            ('public', orm['members.Graduation:public']),
            ('created', orm['members.Graduation:created']),
            ('last_modified', orm['members.Graduation:last_modified']),
            ('person', orm['members.Graduation:person']),
            ('nominated_by', orm['members.Graduation:nominated_by']),
            ('rank', orm['members.Graduation:rank']),
            ('date', orm['members.Graduation:date']),
            ('text', orm['members.Graduation:text']),
            ('is_nomination', orm['members.Graduation:is_nomination']),
            ('request_doc', orm['members.Graduation:request_doc']),
            ('confirmation_doc', orm['members.Graduation:confirmation_doc']),
            ('payment_doc', orm['members.Graduation:payment_doc']),
            ('is_active', orm['members.Graduation:is_active']),
        ))
        db.send_create_signal('members', ['Graduation'])
        
        # Adding model 'License'
        db.create_table('members_license', (
            ('id', orm['members.License:id']),
            ('public', orm['members.License:public']),
            ('created', orm['members.License:created']),
            ('last_modified', orm['members.License:last_modified']),
            ('person', orm['members.License:person']),
            ('status', orm['members.License:status']),
            ('date', orm['members.License:date']),
            ('request', orm['members.License:request']),
            ('receipt', orm['members.License:receipt']),
            ('rejected', orm['members.License:rejected']),
            ('request_doc', orm['members.License:request_doc']),
            ('receipt_doc', orm['members.License:receipt_doc']),
            ('text', orm['members.License:text']),
            ('is_active', orm['members.License:is_active']),
        ))
        db.send_create_signal('members', ['License'])
        
        # Adding model 'Dojo'
        db.create_table('members_dojo', (
            ('id', orm['members.Dojo:id']),
            ('public', orm['members.Dojo:public']),
            ('created', orm['members.Dojo:created']),
            ('last_modified', orm['members.Dojo:last_modified']),
            ('name', orm['members.Dojo:name']),
            ('name_jp', orm['members.Dojo:name_jp']),
            ('shortname', orm['members.Dojo:shortname']),
            ('text', orm['members.Dojo:text']),
            ('street', orm['members.Dojo:street']),
            ('zip', orm['members.Dojo:zip']),
            ('city', orm['members.Dojo:city']),
            ('country', orm['members.Dojo:country']),
            ('twa_region', orm['members.Dojo:twa_region']),
            ('phone', orm['members.Dojo:phone']),
            ('fax', orm['members.Dojo:fax']),
            ('mobile', orm['members.Dojo:mobile']),
            ('email', orm['members.Dojo:email']),
            ('website', orm['members.Dojo:website']),
            ('is_active', orm['members.Dojo:is_active']),
            ('is_twa_member', orm['members.Dojo:is_twa_member']),
            ('leader', orm['members.Dojo:leader']),
            ('association', orm['members.Dojo:association']),
        ))
        db.send_create_signal('members', ['Dojo'])
        
        # Adding model 'TWAPayment'
        db.create_table('members_twapayment', (
            ('id', orm['members.TWAPayment:id']),
            ('public', orm['members.TWAPayment:public']),
            ('created', orm['members.TWAPayment:created']),
            ('last_modified', orm['members.TWAPayment:last_modified']),
            ('twa', orm['members.TWAPayment:twa']),
            ('date', orm['members.TWAPayment:date']),
            ('year', orm['members.TWAPayment:year']),
            ('cash', orm['members.TWAPayment:cash']),
            ('text', orm['members.TWAPayment:text']),
        ))
        db.send_create_signal('members', ['TWAPayment'])
        
        # Adding ManyToManyField 'Person.dojos'
        db.create_table('members_person_dojos', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm.Person, null=False)),
            ('dojo', models.ForeignKey(orm.Dojo, null=False))
        ))
        
        # Creating unique_together for [firstname, lastname] on Person.
        db.create_unique('members_person', ['firstname', 'lastname'])
        
    
    
    def backwards(self, orm):
        
        # Deleting unique_together for [firstname, lastname] on Person.
        db.delete_unique('members_person', ['firstname', 'lastname'])
        
        # Deleting model 'TWAMembership'
        db.delete_table('members_twamembership')
        
        # Deleting model 'Association'
        db.delete_table('members_association')
        
        # Deleting model 'Document'
        db.delete_table('members_document')
        
        # Deleting model 'News'
        db.delete_table('members_news')
        
        # Deleting model 'Person'
        db.delete_table('members_person')
        
        # Deleting model 'Download'
        db.delete_table('members_download')
        
        # Deleting model 'Country'
        db.delete_table('members_country')
        
        # Deleting model 'Graduation'
        db.delete_table('members_graduation')
        
        # Deleting model 'License'
        db.delete_table('members_license')
        
        # Deleting model 'Dojo'
        db.delete_table('members_dojo')
        
        # Deleting model 'TWAPayment'
        db.delete_table('members_twapayment')
        
        # Dropping ManyToManyField 'Person.dojos'
        db.delete_table('members_person_dojos')
        
    
    
    models = {
        'members.association': {
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'association'", 'null': 'True', 'to': "orm['members.Person']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['members.Country']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'shortname': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'members.country': {
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'name_de': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'name_ja': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'})
        },
        'members.document': {
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['members.Person']", 'null': 'True', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'})
        },
        'members.dojo': {
            'association': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['members.Association']", 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['members.Country']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_twa_member': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'leader': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'dojo_leader'", 'null': 'True', 'to': "orm['members.Person']"}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'name_jp': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'shortname': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'twa_region': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'members.download': {
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'datei': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'members.graduation': {
            'confirmation_doc': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_nomination': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'nominated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'nominations'", 'null': 'True', 'to': "orm['members.Person']"}),
            'payment_doc': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'graduations'", 'to': "orm['members.Person']"}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'rank': ('django.db.models.fields.IntegerField', [], {}),
            'request_doc': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'members.license': {
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['members.Person']"}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'receipt': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'receipt_doc': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'rejected': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'request': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'request_doc': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'members.news': {
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'preview': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 2, 21, 22, 20, 25, 611766)'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'members.person': {
            'Meta': {'unique_together': "(('firstname', 'lastname'),)"},
            'aikido_since': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'birth_sort_string': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['members.Country']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dojos': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['members.Dojo']", 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'firstname_jp': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'lastname_jp': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name_prefix': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'text_beirat': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'members.twamembership': {
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['members.Person']"}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'request': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'request_doc': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'twa_id_country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['members.Country']", 'null': 'True', 'blank': 'True'}),
            'twa_id_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'members.twapayment': {
            'cash': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'twa': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['members.TWAMembership']"}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '2010'})
        }
    }
    
    complete_apps = ['members']
