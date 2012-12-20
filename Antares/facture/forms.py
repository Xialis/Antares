# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.forms import ModelChoiceField, RadioSelect, ChoiceField
from facture.models import LigneFacture, Monture, Option, Facture
from fournisseur.models import Type, Diametre, Couleur, Traitement


class LigneForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    diametre = ModelChoiceField(queryset=Diametre.objects.none())
    couleur = ModelChoiceField(queryset=Couleur.objects.none())
    traitement = ModelChoiceField(queryset=Traitement.objects.none(), required=False)

    class Meta:
        model = LigneFacture
        exclude = ('facture', 'monture', 'oeil', 'tarif')

    def __init__(self, *args, **kwargs):
        super(LigneForm, self).__init__(*args, **kwargs)
        self.fields['vtype'].choices = categorie_vtype()

    def filtre_vtype(self, vtype):
        self.fields['diametre'].queryset = Diametre.objects.filter(type=vtype)
        self.fields['couleur'].queryset = Couleur.objects.filter(type=vtype)
        self.fields['traitement'].queryset = Traitement.objects.filter(type=vtype)
        return self


def categorie_vtype():
    liste = []
    unifocaux = []
    progressifs = []
    req = Type.objects.order_by('nom')
    for vtype in req:
        if vtype.progressif == True:
            progressifs.append([vtype.id, vtype.nom])
        else:
            unifocaux.append([vtype.id, vtype.nom])

    liste.append(['', '----------'])
    liste.append([u"Unifocaux", unifocaux])
    liste.append([u"Progressifs", progressifs])
    return liste


class MontureForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = Monture
        exclude = ('facture', 'numero',)
        widgets = {
                   'oeil': RadioSelect(),
                   }

    def choixvpvl(self):
        VISION = (
            ('', '----------'),
              ('P', 'Près'),
              ('L', 'Loin'),
          )
        self.fields['vision'] = ChoiceField(choices=VISION)


class OptionForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = Option
        exclude = ('facture', )


class ChoixFactureForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = Facture
        fields = ('bproforma', 'organisme', )
