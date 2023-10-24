from django import forms
from .models import Pojistenci, Bydliste, Smlouva

class PojistenciForm(forms.ModelForm):
    class Meta:
        model = Pojistenci
        fields = ['jmeno', 'prijmeni', 'cislo_pojistence', 'datum_narozeni', 'telefon', 'email']

    def __init__(self, *args, **kwargs):
        super(PojistenciForm, self).__init__(*args, **kwargs)
        self.fields['jmeno'].widget.attrs.update({'class': 'form-control'})
        self.fields['prijmeni'].widget.attrs.update({'class': 'form-control'})
        self.fields['cislo_pojistence'].widget.attrs.update({'class': 'form-control'})
        self.fields['datum_narozeni'].widget.attrs.update({'class': 'form-control'})
        self.fields['telefon'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        
        
class ConfirmDeleteForm(forms.Form):
    confirm_delete = forms.BooleanField(label="Potvrďte smazání", required=False)
    
    
class BydlisteForm(forms.ModelForm):
    class Meta:
        model = Bydliste
        fields = ['ulice', 'cislo_popisne', 'mesto', 'psc']

    def __init__(self, *args, **kwargs):
        super(BydlisteForm, self).__init__(*args, **kwargs)
        self.fields['ulice'].widget.attrs.update({'class': 'form-control'})
        self.fields['cislo_popisne'].widget.attrs.update({'class': 'form-control'})
        self.fields['mesto'].widget.attrs.update({'class': 'form-control'})
        self.fields['psc'].widget.attrs.update({'class': 'form-control'})
        
class SmlouvyForm(forms.ModelForm):
    class Meta:
        model = Smlouva
        fields = ['cislo_smlouvy', 'datum_pocatek', 'datum_vyroci', 'typ_smlouvy']

    def __init__(self, *args, **kwargs):
        super(SmlouvyForm, self).__init__(*args, **kwargs)
        self.fields['cislo_smlouvy'].widget.attrs.update({'class': 'form-control'})
        self.fields['datum_pocatek'].widget.attrs.update({'class': 'form-control'})
        self.fields['datum_vyroci'].widget.attrs.update({'class': 'form-control'})
        self.fields['typ_smlouvy'].widget.attrs.update({'class': 'form-control'})
    
class VyhledatPojistenceForm(forms.Form):
    jmeno = forms.CharField(label="Jméno", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    prijmeni = forms.CharField(label="Příjmení", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    cislo_pojistence = forms.CharField(label="Číslo pojištěnce", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))   
    
