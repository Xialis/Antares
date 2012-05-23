# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Fournisseur'
        db.create_table('fournisseur_fournisseur', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nom', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('tel', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=100)),
        ))
        db.send_create_signal('fournisseur', ['Fournisseur'])

        # Adding model 'Traitement'
        db.create_table('fournisseur_traitement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fournisseur', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fournisseur.Fournisseur'])),
            ('nom', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('fournisseur', ['Traitement'])

        # Adding model 'Diametre'
        db.create_table('fournisseur_diametre', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fournisseur', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fournisseur.Fournisseur'])),
            ('nom', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('fournisseur', ['Diametre'])

        # Adding model 'Couleur'
        db.create_table('fournisseur_couleur', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fournisseur', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fournisseur.Fournisseur'])),
            ('nom', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('fournisseur', ['Couleur'])

        # Adding model 'Type'
        db.create_table('fournisseur_type', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fournisseur', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fournisseur.Fournisseur'])),
            ('nom', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('progressif', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('fournisseur', ['Type'])

        # Adding M2M table for field traitements on 'Type'
        db.create_table('fournisseur_type_traitements', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('type', models.ForeignKey(orm['fournisseur.type'], null=False)),
            ('traitement', models.ForeignKey(orm['fournisseur.traitement'], null=False))
        ))
        db.create_unique('fournisseur_type_traitements', ['type_id', 'traitement_id'])

        # Adding M2M table for field diametres on 'Type'
        db.create_table('fournisseur_type_diametres', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('type', models.ForeignKey(orm['fournisseur.type'], null=False)),
            ('diametre', models.ForeignKey(orm['fournisseur.diametre'], null=False))
        ))
        db.create_unique('fournisseur_type_diametres', ['type_id', 'diametre_id'])

        # Adding M2M table for field couleurs on 'Type'
        db.create_table('fournisseur_type_couleurs', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('type', models.ForeignKey(orm['fournisseur.type'], null=False)),
            ('couleur', models.ForeignKey(orm['fournisseur.couleur'], null=False))
        ))
        db.create_unique('fournisseur_type_couleurs', ['type_id', 'couleur_id'])


    def backwards(self, orm):
        # Deleting model 'Fournisseur'
        db.delete_table('fournisseur_fournisseur')

        # Deleting model 'Traitement'
        db.delete_table('fournisseur_traitement')

        # Deleting model 'Diametre'
        db.delete_table('fournisseur_diametre')

        # Deleting model 'Couleur'
        db.delete_table('fournisseur_couleur')

        # Deleting model 'Type'
        db.delete_table('fournisseur_type')

        # Removing M2M table for field traitements on 'Type'
        db.delete_table('fournisseur_type_traitements')

        # Removing M2M table for field diametres on 'Type'
        db.delete_table('fournisseur_type_diametres')

        # Removing M2M table for field couleurs on 'Type'
        db.delete_table('fournisseur_type_couleurs')


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
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
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