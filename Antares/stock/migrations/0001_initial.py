# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LigneStock'
        db.create_table('stock_lignestock', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fournisseur', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fournisseur.Fournisseur'])),
            ('vtype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fournisseur.Type'])),
            ('diametre', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fournisseur.Diametre'])),
            ('sphere', self.gf('django.db.models.fields.DecimalField')(max_digits=4, decimal_places=2)),
            ('cylindre', self.gf('django.db.models.fields.DecimalField')(max_digits=4, decimal_places=2)),
            ('traitement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fournisseur.Traitement'], null=True)),
            ('couleur', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fournisseur.Couleur'], null=True)),
            ('quantite', self.gf('django.db.models.fields.IntegerField')()),
            ('seuil', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('stock', ['LigneStock'])


    def backwards(self, orm):
        # Deleting model 'LigneStock'
        db.delete_table('stock_lignestock')


    models = {
        'fournisseur.couleur': {
            'Meta': {'ordering': "['nom']", 'unique_together': "(('fournisseur', 'nom'),)", 'object_name': 'Couleur'},
            'fournisseur': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fournisseur.Fournisseur']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'remise_monture': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '0', 'blank': 'True'}),
            'transition': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'fournisseur.diametre': {
            'Meta': {'ordering': "['nom']", 'unique_together': "(('fournisseur', 'nom'),)", 'object_name': 'Diametre'},
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
            'Meta': {'ordering': "['nom']", 'unique_together': "(('fournisseur', 'nom'),)", 'object_name': 'Traitement'},
            'fournisseur': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fournisseur.Fournisseur']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'remise_monture': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '0', 'blank': 'True'}),
            'tarif': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '0'})
        },
        'fournisseur.type': {
            'Meta': {'ordering': "['nom']", 'unique_together': "(('fournisseur', 'nom'),)", 'object_name': 'Type'},
            'couleurs': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['fournisseur.Couleur']", 'null': 'True', 'blank': 'True'}),
            'diametres': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['fournisseur.Diametre']", 'symmetrical': 'False'}),
            'fournisseur': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fournisseur.Fournisseur']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'progressif': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'remise_monture': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '0', 'blank': 'True'}),
            'stock': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tarif_blanc': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '0'}),
            'tarif_couleur': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '0', 'blank': 'True'}),
            'tarif_transition': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '0', 'blank': 'True'}),
            'traitements': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['fournisseur.Traitement']", 'null': 'True', 'blank': 'True'})
        },
        'stock.lignestock': {
            'Meta': {'object_name': 'LigneStock'},
            'couleur': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fournisseur.Couleur']", 'null': 'True'}),
            'cylindre': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '2'}),
            'diametre': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fournisseur.Diametre']"}),
            'fournisseur': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fournisseur.Fournisseur']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quantite': ('django.db.models.fields.IntegerField', [], {}),
            'seuil': ('django.db.models.fields.IntegerField', [], {}),
            'sphere': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '2'}),
            'traitement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fournisseur.Traitement']", 'null': 'True'}),
            'vtype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fournisseur.Type']"})
        }
    }

    complete_apps = ['stock']