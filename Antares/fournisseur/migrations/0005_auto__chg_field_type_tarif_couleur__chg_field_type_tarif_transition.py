# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Type.tarif_couleur'
        db.alter_column('fournisseur_type', 'tarif_couleur', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=0))

        # Changing field 'Type.tarif_transition'
        db.alter_column('fournisseur_type', 'tarif_transition', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=0))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Type.tarif_couleur'
        raise RuntimeError("Cannot reverse this migration. 'Type.tarif_couleur' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Type.tarif_transition'
        raise RuntimeError("Cannot reverse this migration. 'Type.tarif_transition' and its values cannot be restored.")

    models = {
        'fournisseur.couleur': {
            'Meta': {'ordering': "['nom']", 'object_name': 'Couleur'},
            'fournisseur': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fournisseur.Fournisseur']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'transition': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'fournisseur.diametre': {
            'Meta': {'ordering': "['nom']", 'object_name': 'Diametre'},
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
            'Meta': {'ordering': "['nom']", 'object_name': 'Traitement'},
            'fournisseur': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fournisseur.Fournisseur']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tarif': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '0'})
        },
        'fournisseur.type': {
            'Meta': {'ordering': "['nom']", 'object_name': 'Type'},
            'couleurs': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['fournisseur.Couleur']", 'null': 'True', 'blank': 'True'}),
            'diametres': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['fournisseur.Diametre']", 'symmetrical': 'False'}),
            'fournisseur': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fournisseur.Fournisseur']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'progressif': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tarif_blanc': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '0'}),
            'tarif_couleur': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '0', 'blank': 'True'}),
            'tarif_transition': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '0', 'blank': 'True'}),
            'traitements': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['fournisseur.Traitement']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['fournisseur']