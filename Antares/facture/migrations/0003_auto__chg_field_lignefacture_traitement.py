# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'LigneFacture.traitement'
        db.alter_column('facture_lignefacture', 'traitement_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fournisseur.Traitement'], null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'LigneFacture.traitement'
        raise RuntimeError("Cannot reverse this migration. 'LigneFacture.traitement' and its values cannot be restored.")

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
        },
        'facture.facture': {
            'Meta': {'object_name': 'Facture'},
            'bproforma': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['client.Client']"}),
            'date_creation': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modification': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interloculteur': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['facture.Interlocuteur']"}),
            'numero': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '12'}),
            'prescription': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['client.Prescription']"}),
            'proforma': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['facture.Facture']", 'null': 'True', 'blank': 'True'})
        },
        'facture.interlocuteur': {
            'Meta': {'object_name': 'Interlocuteur'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'})
        },
        'facture.lignefacture': {
            'Meta': {'object_name': 'LigneFacture'},
            'couleur': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fournisseur.Couleur']", 'null': 'True', 'blank': 'True'}),
            'diametre': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fournisseur.Diametre']"}),
            'facture': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['facture.Facture']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monture': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'oeil': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'tarif': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '0'}),
            'traitement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fournisseur.Traitement']", 'null': 'True', 'blank': 'True'}),
            'vtype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fournisseur.Type']"})
        },
        'facture.option': {
            'Meta': {'object_name': 'Option'},
            'facture': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['facture.Facture']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tarif': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '0'})
        },
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
        }
    }

    complete_apps = ['facture']