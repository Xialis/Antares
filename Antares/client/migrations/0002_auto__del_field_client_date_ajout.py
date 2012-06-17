# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Client.date_ajout'
        db.delete_column('client_client', 'date_ajout')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Client.date_ajout'
        raise RuntimeError("Cannot reverse this migration. 'Client.date_ajout' and its values cannot be restored.")

    models = {
        'client.client': {
            'Meta': {'object_name': 'Client'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'organisme': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['client.OrganismePayeur']", 'null': 'True', 'blank': 'True'}),
            'prenom': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'client.organismepayeur': {
            'Meta': {'object_name': 'OrganismePayeur'},
            'contact_mail': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'contact_nom': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'contact_tel': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'client.prescripteur': {
            'Meta': {'object_name': 'Prescripteur'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'client.prescription': {
            'Meta': {'object_name': 'Prescription'},
            'addition': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            'axe': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '3', 'decimal_places': '0', 'blank': 'True'}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['client.Client']"}),
            'cylindre': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            'date_realisation': ('django.db.models.fields.DateField', [], {}),
            'erreur': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prescripteur': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['client.Prescripteur']"}),
            'sphere': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '2'})
        }
    }

    complete_apps = ['client']