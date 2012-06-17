# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'OrganismePayeur'
        db.create_table('client_organismepayeur', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nom', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('contact_nom', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('contact_tel', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('contact_mail', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
        ))
        db.send_create_signal('client', ['OrganismePayeur'])

        # Adding model 'Prescripteur'
        db.create_table('client_prescripteur', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nom', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('telephone', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal('client', ['Prescripteur'])

        # Adding model 'Client'
        db.create_table('client_client', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('date_ajout', self.gf('django.db.models.fields.DateField')()),
            ('nom', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('prenom', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('telephone', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('organisme', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['client.OrganismePayeur'], null=True, blank=True)),
        ))
        db.send_create_signal('client', ['Client'])

        # Adding model 'Prescription'
        db.create_table('client_prescription', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('prescripteur', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['client.Prescripteur'])),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['client.Client'])),
            ('date_realisation', self.gf('django.db.models.fields.DateField')()),
            ('erreur', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sphere', self.gf('django.db.models.fields.DecimalField')(max_digits=4, decimal_places=2)),
            ('cylindre', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=2, blank=True)),
            ('addition', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=2, blank=True)),
            ('axe', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=3, decimal_places=0, blank=True)),
        ))
        db.send_create_signal('client', ['Prescription'])


    def backwards(self, orm):
        # Deleting model 'OrganismePayeur'
        db.delete_table('client_organismepayeur')

        # Deleting model 'Prescripteur'
        db.delete_table('client_prescripteur')

        # Deleting model 'Client'
        db.delete_table('client_client')

        # Deleting model 'Prescription'
        db.delete_table('client_prescription')


    models = {
        'client.client': {
            'Meta': {'object_name': 'Client'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'date_ajout': ('django.db.models.fields.DateField', [], {}),
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