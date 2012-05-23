# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Traitement', fields ['nom']
        db.delete_unique('fournisseur_traitement', ['nom'])

        # Removing unique constraint on 'Type', fields ['nom']
        db.delete_unique('fournisseur_type', ['nom'])

        # Removing unique constraint on 'Diametre', fields ['nom']
        db.delete_unique('fournisseur_diametre', ['nom'])

        # Removing unique constraint on 'Couleur', fields ['nom']
        db.delete_unique('fournisseur_couleur', ['nom'])


    def backwards(self, orm):
        # Adding unique constraint on 'Couleur', fields ['nom']
        db.create_unique('fournisseur_couleur', ['nom'])

        # Adding unique constraint on 'Diametre', fields ['nom']
        db.create_unique('fournisseur_diametre', ['nom'])

        # Adding unique constraint on 'Type', fields ['nom']
        db.create_unique('fournisseur_type', ['nom'])

        # Adding unique constraint on 'Traitement', fields ['nom']
        db.create_unique('fournisseur_traitement', ['nom'])


    models = {
        'fournisseur.couleur': {
            'Meta': {'object_name': 'Couleur'},
            'fournisseur': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fournisseur.Fournisseur']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'fournisseur.diametre': {
            'Meta': {'object_name': 'Diametre'},
            'fournisseur': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fournisseur.Fournisseur']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'fournisseur.fournisseur': {
            'Meta': {'object_name': 'Fournisseur'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'fournisseur.traitement': {
            'Meta': {'object_name': 'Traitement'},
            'fournisseur': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fournisseur.Fournisseur']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'fournisseur.type': {
            'Meta': {'object_name': 'Type'},
            'couleurs': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['fournisseur.Couleur']", 'symmetrical': 'False'}),
            'diametres': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['fournisseur.Diametre']", 'symmetrical': 'False'}),
            'fournisseur': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fournisseur.Fournisseur']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'progressif': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'traitements': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['fournisseur.Traitement']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['fournisseur']