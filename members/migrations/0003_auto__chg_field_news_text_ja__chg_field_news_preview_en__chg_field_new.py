# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'News.text_ja'
        db.alter_column('members_news', 'text_ja', self.gf('django.db.models.fields.TextField')(blank=True))

        # Changing field 'News.preview_en'
        db.alter_column('members_news', 'preview_en', self.gf('django.db.models.fields.TextField')(blank=True))

        # Changing field 'News.preview_ja'
        db.alter_column('members_news', 'preview_ja', self.gf('django.db.models.fields.TextField')(blank=True))

        # Changing field 'News.title_en'
        db.alter_column('members_news', 'title_en', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True))

        # Changing field 'News.text_en'
        db.alter_column('members_news', 'text_en', self.gf('django.db.models.fields.TextField')(blank=True))

        # Changing field 'News.text'
        db.alter_column('members_news', 'text', self.gf('django.db.models.fields.TextField')(blank=True))

        # Changing field 'News.preview'
        db.alter_column('members_news', 'preview', self.gf('django.db.models.fields.TextField')(blank=True))

        # Changing field 'News.title_ja'
        db.alter_column('members_news', 'title_ja', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True))


    def backwards(self, orm):
        
        # Changing field 'News.text_ja'
        db.alter_column('members_news', 'text_ja', self.gf('django.db.models.fields.TextField')(null=True, blank=True))

        # Changing field 'News.preview_en'
        db.alter_column('members_news', 'preview_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True))

        # Changing field 'News.preview_ja'
        db.alter_column('members_news', 'preview_ja', self.gf('django.db.models.fields.TextField')(null=True, blank=True))

        # Changing field 'News.title_en'
        db.alter_column('members_news', 'title_en', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True))

        # Changing field 'News.text_en'
        db.alter_column('members_news', 'text_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True))

        # Changing field 'News.text'
        db.alter_column('members_news', 'text', self.gf('django.db.models.fields.TextField')(null=True, blank=True))

        # Changing field 'News.preview'
        db.alter_column('members_news', 'preview', self.gf('django.db.models.fields.TextField')(null=True, blank=True))

        # Changing field 'News.title_ja'
        db.alter_column('members_news', 'title_ja', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True))


    models = {
        'members.association': {
            'Meta': {'object_name': 'Association'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'association'", 'blank': 'True', 'null': 'True', 'to': "orm['members.Person']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['members.Country']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': 'True'}),
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
            'Meta': {'object_name': 'Country'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'unique': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': 'True'}),
            'name_de': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'name_ja': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'})
        },
        'members.document': {
            'Meta': {'object_name': 'Document'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['members.Person']", 'null': 'True', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'})
        },
        'members.dojo': {
            'Meta': {'object_name': 'Dojo'},
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
            'leader': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dojo_leader'", 'blank': 'True', 'null': 'True', 'to': "orm['members.Person']"}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': 'True'}),
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
            'Meta': {'object_name': 'Download'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'datei': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'members.graduation': {
            'Meta': {'object_name': 'Graduation'},
            'confirmation_doc': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_nomination': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'nominated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nominations'", 'blank': 'True', 'null': 'True', 'to': "orm['members.Person']"}),
            'payment_doc': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'graduations'", 'to': "orm['members.Person']"}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'rank': ('django.db.models.fields.IntegerField', [], {}),
            'request_doc': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'members.license': {
            'Meta': {'object_name': 'License'},
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
            'Meta': {'object_name': 'News'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'preview': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'preview_en': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'preview_ja': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 6, 5, 10, 4, 2, 161188)'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'text_en': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'text_ja': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'title_ja': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        'members.person': {
            'Meta': {'unique_together': "(('firstname', 'lastname'),)", 'object_name': 'Person'},
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
            'Meta': {'object_name': 'TWAMembership'},
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
            'Meta': {'object_name': 'TWAPayment'},
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
