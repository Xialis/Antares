# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Prescripteur', fields ['nom', 'telephone']
        db.create_unique('client_prescripteur', ['nom', 'telephone'])

        # Adding unique constraint on 'Client', fields ['nom', 'prenom', 'telephone']
        db.create_unique('client_client', ['nom', 'prenom', 'telephone'])

        # Adding unique constraint on 'Client', fields ['nom', 'prenom', 'email']
        db.create_unique('client_client', ['nom', 'prenom', 'email'])

        # Deleting field 'Prescription.cylindre'
        db.delete_column('client_prescription', 'cylindre')

        # Deleting field 'Prescription.sphere'
        db.delete_column('client_prescription', 'sphere')

        # Deleting field 'Prescription.axe'
        db.delete_column('client_prescription', 'axe')

        # Deleting field 'Prescription.addition'
        db.delete_column('client_prescription', 'addition')

        # Adding field 'Prescription.sphere_od'
        db.add_column('client_prescription', 'sphere_od',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=4, decimal_places=2),
                      keep_default=False)

        # Adding field 'Prescription.cylindre_od'
        db.add_column('client_prescription', 'cylindre_od',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=2, blank=True),
                      keep_default=False)

        # Adding field 'Prescription.addition_od'
        db.add_column('client_prescription', 'addition_od',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=2, blank=True),
                      keep_default=False)

        # Adding field 'Prescription.axe_od'
        db.add_column('client_prescription', 'axe_od',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=3, decimal_places=0, blank=True),
                      keep_default=False)

        # Adding field 'Prescription.sphere_og'
        db.add_column('client_prescription', 'sphere_og',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=4, decimal_places=2),
                      keep_default=False)

        # Adding field 'Prescription.cylindre_og'
        db.add_column('client_prescription', 'cylindre_og',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=2, blank=True),
                      keep_default=False)

        # Adding field 'Prescription.addition_og'
        db.add_column('client_prescription', 'addition_og',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=2, blank=True),
                      keep_default=False)

        # Adding field 'Prescription.axe_og'
        db.add_column('client_prescription', 'axe_og',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=3, decimal_places=0, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Removing unique constraint on 'Client', fields ['nom', 'prenom', 'email']
        db.delete_unique('client_client', ['nom', 'prenom', 'email'])

        # Removing unique constraint on 'Client', fields ['nom', 'prenom', 'telephone']
        db.delete_unique('client_client', ['nom', 'prenom', 'telephone'])

        # Removing unique constraint on 'Prescripteur', fields ['nom', 'telephone']
        db.delete_unique('client_prescripteur', ['nom', 'telephone'])

        # Adding field 'Prescription.cylindre'
        db.add_column('client_prescription', 'cylindre',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=2, blank=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Prescription.sphere'
        raise RuntimeError("Cannot reverse this migration. 'Prescription.sphere' and its values cannot be restored.")
        # Adding field 'Prescription.axe'
        db.add_column('client_prescription', 'axe',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=3, decimal_places=0, blank=True),
                      keep_default=False)

        # Adding field 'Prescription.addition'
        db.add_column('client_prescription', 'addition',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=2, blank=True),
                      keep_default=False)

        # Deleting field 'Prescription.sphere_od'
        db.delete_column('client_prescription', 'sphere_od')

        # Deleting field 'Prescription.cylindre_od'
        db.delete_column('client_prescription', 'cylindre_od')

        # Deleting field 'Prescription.addition_od'
        db.delete_column('client_prescription', 'addition_od')

        # Deleting field 'Prescription.axe_od'
        db.delete_column('client_prescription', 'axe_od')

        # Deleting field 'Prescription.sphere_og'
        db.delete_column('client_prescription', 'sphere_og')

        # Deleting field 'Prescription.cylindre_og'
        db.delete_column('client_prescription', 'cylindre_og')

        # Deleting field 'Prescription.addition_og'
        db.delete_column('client_prescription', 'addition_og')

        # Deleting field 'Prescription.axe_og'
        db.delete_column('client_prescription', 'axe_og')


    models = {
        'client.client': {
            'Meta': {'ordering': "['code']", 'unique_together': "(('nom', 'prenom', 'telephone'), ('nom', 'prenom', 'email'))", 'object_name': 'Client'},
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
            'Meta': {'ordering': "['nom']", 'unique_together': "(('nom', 'telephone'),)", 'object_name': 'Prescripteur'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'client.prescription': {
            'Meta': {'object_name': 'Prescription'},
            'addition_od': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            'addition_og': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            'axe_od': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '3', 'decimal_places': '0', 'blank': 'True'}),
            'axe_og': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '3', 'decimal_places': '0', 'blank': 'True'}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['client.Client']"}),
            'cylindre_od': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            'cylindre_og': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            'date_realisation': ('django.db.models.fields.DateField', [], {}),
            'erreur': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prescripteur': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['client.Prescripteur']"}),
            'sphere_od': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '2'}),
            'sphere_og': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '2'})
        }
    }

    complete_apps = ['client']