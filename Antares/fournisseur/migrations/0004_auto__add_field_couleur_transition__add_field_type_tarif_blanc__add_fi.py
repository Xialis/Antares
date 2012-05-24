# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Couleur.transition'
        db.add_column('fournisseur_couleur', 'transition',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Type.tarif_blanc'
        db.add_column('fournisseur_type', 'tarif_blanc',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=0),
                      keep_default=False)

        # Adding field 'Type.tarif_couleur'
        db.add_column('fournisseur_type', 'tarif_couleur',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=0),
                      keep_default=False)

        # Adding field 'Type.tarif_transition'
        db.add_column('fournisseur_type', 'tarif_transition',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=0),
                      keep_default=False)

        # Adding field 'Traitement.tarif'
        db.add_column('fournisseur_traitement', 'tarif',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Couleur.transition'
        db.delete_column('fournisseur_couleur', 'transition')

        # Deleting field 'Type.tarif_blanc'
        db.delete_column('fournisseur_type', 'tarif_blanc')

        # Deleting field 'Type.tarif_couleur'
        db.delete_column('fournisseur_type', 'tarif_couleur')

        # Deleting field 'Type.tarif_transition'
        db.delete_column('fournisseur_type', 'tarif_transition')

        # Deleting field 'Traitement.tarif'
        db.delete_column('fournisseur_traitement', 'tarif')


    models = {
        'fournisseur.couleur': {
            'Meta': {'object_name': 'Couleur'},
            'fournisseur': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fournisseur.Fournisseur']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'transition': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tarif': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '0'})
        },
        'fournisseur.type': {
            'Meta': {'object_name': 'Type'},
            'couleurs': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['fournisseur.Couleur']", 'symmetrical': 'False'}),
            'diametres': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['fournisseur.Diametre']", 'symmetrical': 'False'}),
            'fournisseur': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fournisseur.Fournisseur']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'progressif': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tarif_blanc': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '0'}),
            'tarif_couleur': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '0'}),
            'tarif_transition': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '0'}),
            'traitements': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['fournisseur.Traitement']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['fournisseur']