from django.forms import ModelForm
from fournisseur.models import *


class TypeForm(ModelForm):
    class Meta:
        model = Type
        

class FourForm(ModelForm):
    class Meta:
        model = Fournisseur


