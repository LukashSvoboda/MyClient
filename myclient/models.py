from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


# Definuje model adresy bydliště
class Bydliste(models.Model):
    ulice = models.CharField(max_length=100)
    cislo_popisne = models.CharField(max_length=10, null=True, blank=True)
    mesto = models.CharField(max_length=100)
    psc = models.IntegerField()
    
    def __str__(self):
        return f"{self.ulice}, {self.cislo_popisne}, {self.mesto} {self.psc}"


# Validátor pro ověření správného formátu e-mailu
def validate_email_format(value):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, value):
        raise ValidationError('E-mail nemá správný formát.')


# Validátor pro kontrolu, zda jméno obsahuje číslice
def validate_name(value):
    if any(char.isdigit() for char in value):
        raise ValidationError('Jméno nesmí obsahovat číslice.')


# Validátor pro ověření správného formátu čísla pojištěnce
def validate_cislo_pojistence(value):
    if not re.match(r'^\d{10}$', str(value)):
        raise ValidationError('Neplatný formát čísla pojištěnce.')


# Definuje model pojištěnce
class Pojistenci(models.Model):
    jmeno = models.CharField(max_length=100, validators=[validate_name])
    prijmeni = models.CharField(max_length=100, validators=[validate_name])
    cislo_pojistence = models.IntegerField(validators=[validate_cislo_pojistence], unique=True, error_messages={'unique': "Pojištěnec s tímto číslem již existuje."})
    datum_narozeni = models.DateField()
    telefon = models.CharField(max_length=20)
    email = models.EmailField(validators=[validate_email_format])
    bydliste = models.ForeignKey(Bydliste, on_delete=models.CASCADE, default=None, null=True)
    
    def __str__(self):
        return self.jmeno


# Validátor pro ověření správného formátu čísla smlouvy
def validate_cislo_smlouvy(value):
    if not re.match(r'^\d{9}$', str(value)):
        raise ValidationError('Číslo smlouvy musí mít 9 číslic.')


# Definuje model pojistné smlouvy
class Smlouva(models.Model):
    cislo_smlouvy = models.IntegerField(validators=[validate_cislo_smlouvy], unique=True, error_messages={'unique': "Smlouva s tímto číslem již existuje."})
    datum_pocatek = models.DateField()
    datum_vyroci = models.DateField()
    
    TYPE_CHOICES = (
        ('majetek', 'Majetek'),
        ('auto', 'Auto'),
        ('zivot', 'Život'),
        ('investice', 'Investice'),
        ('mojefirma', 'Moje Firma'),
        ('podnikatele', 'Podnikatelé'),
        ('prumysl', 'Průmysl'),
        ('drony', 'Drony'),
        ('flotila', 'Flotila'),
    )
    
    typ_smlouvy = models.CharField(max_length=20, choices=TYPE_CHOICES)
    pojistenec = models.ForeignKey(Pojistenci, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return f"Cislo smlouvy: {self.cislo_smlouvy}, Pojisteni: {self.datum_pocatek} {self.datum_vyroci} {self.typ_smlouvy}"    


# Formulář pro registraci uživatele
class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


# Formulář pro přihlášení uživatele
class LoginForm(AuthenticationForm):
    class Meta:
        fields = ('username', 'password')
