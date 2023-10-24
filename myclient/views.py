from django.shortcuts import render, redirect, get_object_or_404
from .models import Pojistenci, Smlouva, Bydliste
from .forms import PojistenciForm, ConfirmDeleteForm, BydlisteForm, SmlouvyForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from datetime import date, datetime
from django.db.models import Q
from django.db import IntegrityError, DatabaseError
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
import logging

logger = logging.getLogger(__name__)






@login_required
def index(request):
    """
    Zobrazuje hlavní stránku aplikace.

    Args:
        request (HttpRequest): Objekt obsahující data o HTTP požadavku.

    Returns:
        HttpResponse: Renderovaná stránka 'index.html'.
    """
    return render(request, 'index.html')



@login_required
def vyhledat_pojistence(request):
    """
    Umožňuje uživatelům vyhledat pojištěnce podle jména, příjmení nebo čísla pojistného.

    Args:
        request (HttpRequest): Objekt obsahující data o HTTP požadavku.

    Returns:
        HttpResponse: Renderovaná stránka s výsledky vyhledávání nebo vyhledávacím formulářem.
    """
    vysledky = []  # Seznam pro uložení výsledků vyhledávání.

    # Kontroluje, zda byl formulář odeslán pomocí metody POST.
    if request.method == "POST":
        # Získává hodnoty z formuláře.
        jmeno = request.POST.get('jmeno', '')
        prijmeni = request.POST.get('prijmeni', '')
        cislo_pojistence = request.POST.get('cislo_pojistence', '')

        # Vytvoříme prázdnou Q instanci.
        query = Q()

        # Přidáváme podmínky do Q objektu podle toho, jaké hodnoty byly zadané.
        if jmeno:
            query |= Q(jmeno__contains=jmeno)
        if prijmeni:
            query |= Q(prijmeni__contains=prijmeni)
        if cislo_pojistence:
            query |= Q(cislo_pojistence=cislo_pojistence)

        # Pokud byla zadána alespoň jedna hodnota, provádíme vyhledávání v databázi.
        if jmeno or prijmeni or cislo_pojistence:
            vysledky = Pojistenci.objects.select_related('bydliste').filter(query)

        # Vrací stránku s výsledky vyhledávání.
        return render(request, 'vysledky_vyhledavani.html', {'vysledky': vysledky})

    # Vrací vyhledávací formulář, pokud nebyl formulář odeslán.
    return render(request, 'vyhledat_pojistence.html')






@login_required
def vytvor_pojistence(request):
    """
    Tato funkce zobrazuje a zpracovává formulář pro vytvoření nového pojistníka.
    Pokud je metoda požadavku POST a formulář je platný, uloží nového pojistníka do databáze 
    a přesměruje uživatele k dalšímu kroku - vytvoření bydliště pro tohoto pojistníka.
    """
    if request.method == "POST":
        form = PojistenciForm(request.POST)
        if form.is_valid():
            try:
                pojistenec = form.save()
                return redirect('vytvor_bydliste_pro_klienta', pojistenec_id=pojistenec.id)
            
            except IntegrityError:
                # Chyba spojená s omezeními integrity databáze.
                messages.error(request, 'Došlo k chybě při ukládání pojistníka. Zkuste to znovu.')
            
                       
            except DatabaseError:
                # Obecná chyba databáze.
                messages.error(request, 'Došlo k chybě databáze. Kontaktujte správce.')
            
            
    else:
        form = PojistenciForm()

    return render(request, 'vytvor_pojistence.html', {'form': form})


    
    



def vytvor_bydliste_pro_klienta(request, pojistenec_id):
    """
    Tato funkce zobrazuje a zpracovává formulář pro vytvoření bydliště pro zadaného pojistníka.
    Pokud je metoda požadavku POST a formulář je platný, uloží nové bydliště do databáze 
    a přiřadí je k danému pojistníkovi.
    """
    # Získání pojistníka podle zadaného ID.
    try:
        pojistenec = Pojistenci.objects.get(id=pojistenec_id)
    except Pojistenci.DoesNotExist:
        messages.error(request, 'Pojistenec nebyl nalezen.')
        return redirect('index')  # Přesměrujte na vhodnou chybovou stránku nebo na úvodní stránku.

    if request.method == "POST":
        bydliste_form = BydlisteForm(request.POST)  # Načtení dat z odeslaného formuláře.
        if bydliste_form.is_valid():
            try:
                bydliste = bydliste_form.save()  # Uložení nového bydliště do databáze.
                pojistenec.bydliste = bydliste  # Přiřazení nového bydliště k pojistníkovi.
                pojistenec.save()  # Uložení aktualizovaného pojistníka do databáze.
                return redirect('vytvor_smlouvy', pojistenec_id=pojistenec.id)  # Přesměrování uživatele.
            except IntegrityError:
                messages.error(request, 'Došlo k chybě integrity. Zkontrolujte zadané údaje a zkuste to znovu.')
            except DatabaseError:
                messages.error(request, 'Došlo k problému s databází. Zkuste to prosím později.')
    else:
        bydliste_form = BydlisteForm()  # Inicializace prázdného formuláře pro vytvoření bydliště.
    
    return render(request, 'vytvor_bydliste_pro_klienta.html', {'klient': pojistenec, 'bydliste_form': bydliste_form})







def vytvor_smlouvu(request, pojistenec_id):
    try:
        # Získání pojištěnce podle ID
        pojistenec = Pojistenci.objects.get(id=pojistenec_id)
    except Pojistenci.DoesNotExist:
        messages.error(request, 'Pojištěnec nebyl nalezen.')
        return redirect('index')  # Přesměrujte na vhodnou chybovou stránku nebo na úvodní stránku.

    # Inicializace prázdného formuláře
    smlouva_form = SmlouvyForm()

    if request.method == "POST":
        # Zpracování formuláře pro vytvoření smlouvy
        smlouva_form = SmlouvyForm(request.POST)
        if smlouva_form.is_valid():
            try:
                # Začátek transakce
                with transaction.atomic():
                    # Vytvoření instance smlouvy, ale neukládání do databáze (commit=False)
                    smlouva = smlouva_form.save(commit=False)
                    # Přiřazení pojištěnce k smlouvě
                    smlouva.pojistenec = pojistenec
                    # Uložení smlouvy do databáze
                    smlouva.save()
                    # Získání akce z formuláře
                    action = request.POST.get("action")
                    if action == "opakovat":
                        # Pokud je vybráno opakování, přesměrovat zpět na stejnou stránku
                        return redirect('vytvor_smlouvy', pojistenec_id=pojistenec_id)
                    else:
                        # Jinak přesměrovat na hlavní stránku
                        return redirect('index')
            except IntegrityError:
                messages.error(request, 'Došlo k chybě integrity. Zkontrolujte zadané údaje a zkuste to znovu.')
            except DatabaseError:
                messages.error(request, 'Došlo k problému s databází. Zkuste to prosím později.')
        else:
            # Vypíše chyby formuláře, pokud není platný
            print(smlouva_form.errors)

    return render(request, 'vytvor_smlouvy.html', {'klient': pojistenec, 'smlouva_form': smlouva_form})





@login_required
def vysledky_vyhledavani(request):
    """
    Zpracování vyhledávání pojištěnců na základě zadaného jména, příjmení nebo čísla pojištěnce.
    
    Pokud je metoda požadavku POST, filtruje databázi pojištěnců podle zadaných kritérií.
    Výsledky vyhledávání obsahují i informace o bydlišti pojištěnce a smlouvách, které má uzavřené.
    """
    
    if request.method == "POST":
        # Získání dat z formuláře.
        jmeno = request.POST.get('jmeno')
        prijmeni = request.POST.get('prijmeni')
        cislo_pojistence = request.POST.get('cislo_pojistence')
        
        # Filtrace databáze pojištěnců na základě zadaných kritérií.
        vysledky = Pojistenci.objects.select_related('bydliste').prefetch_related('smlouva').filter(
            jmeno__contains=jmeno, 
            prijmeni__contains=prijmeni, 
            cislo_pojistence=cislo_pojistence
        )

        return render(request, 'vysledky_vyhledavani.html', {'vysledky': vysledky})

    # Pokud není metoda POST, zobrazí se stránka pro vyhledávání.
    return render(request, 'vysledky_vyhledavani.html')  

def login_view(request):
    """
    Zobrazení a zpracování přihlašovacího formuláře.

    Pokud je metoda požadavku POST a přihlašovací údaje jsou správné, uživatel je přihlášen a přesměrován na indexovou stránku.
    Pokud údaje nejsou správné, zobrazí se chybová zpráva.
    Pokud je metoda jiná než POST, zobrazí se přihlašovací formulář.
    """
    
    if request.method == 'POST':
        # Zpracování odeslaného přihlašovacího formuláře.
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  

    else:
        # Pokud není metoda POST, zobrazí se přihlašovací formulář.
        form = AuthenticationForm()

    return render(request, 'index.html', {'form': form})



@login_required
def smazat_pojistence(request, cislo_pojistence):
    """
    Funkce umožňuje uživateli smazat pojištěnce na základě čísla pojištěnce.
    
    Nejdříve hledáme pojištěnce podle čísla pojištěnce. Pokud je nalezen, zobrazí se formulář
    pro potvrzení smazání. Pokud uživatel potvrdí smazání a je metoda požadavku POST,
    smaže se i bydliště spojené s tímto pojištěncem (pokud existuje) a poté se smaže samotný pojištěnec.
    """

    try:
        # Najděte pojištěnce podle čísla pojištěnce
        pojistenec = Pojistenci.objects.filter(cislo_pojistence=cislo_pojistence).first()
    except DatabaseError:
        messages.error(request, 'Došlo k problému s databází. Zkuste to prosím později.')
        return redirect('index')  # Přesměrujte na vhodnou chybovou stránku nebo na úvodní stránku.

    if request.method == "POST":
        # Zpracování formuláře pro potvrzení smazání
        confirm_form = ConfirmDeleteForm(request.POST)

        if confirm_form.is_valid() and confirm_form.cleaned_data['confirm_delete']:
            try:
                # Uživatel potvrdil smazání
                if pojistenec:
                    # Smazání bydliště spojeného s pojištěncem, pokud existuje
                    if pojistenec.bydliste:
                        pojistenec.bydliste.delete()
                    # Smazání pojištěnce
                    pojistenec.delete()
            except IntegrityError:
                messages.error(request, 'Došlo k chybě integrity při mazání pojištěnce. Zkuste to prosím znovu.')
                return redirect('smazat_pojistence', cislo_pojistence=cislo_pojistence)
            except DatabaseError:
                messages.error(request, 'Došlo k problému s databází při mazání pojištěnce. Zkuste to prosím později.')
                return redirect('smazat_pojistence', cislo_pojistence=cislo_pojistence)

            return redirect('vyhledat_pojistence')

    else:
        # Zobrazení formuláře pro potvrzení smazání
        confirm_form = ConfirmDeleteForm()

    return render(request, 'smazat_pojistence.html', {'pojistenec': pojistenec, 'confirm_form': confirm_form})


def index(request):
    """
    Hlavní stránka, která zobrazuje informace o aktuálně přihlášeném uživateli.
    """
    
    user = request.user  # Získání přihlášeného uživatele
    return render(request, 'index.html', {'user': user})






@login_required
def narozeniny_dnes(request):
    """
    Funkce zobrazuje seznam pojištěnců, kteří mají narozeniny dnes, a zobrazuje také jejich věk.
    """

    def vek_na_zaklade_datum_narozeni(datum_narozeni):
        """
        Vrátí věk osoby na základě jejího data narození.
        """
        dnes = date.today()
        vek = dnes.year - datum_narozeni.year - ((dnes.month, dnes.day) < (datum_narozeni.month, datum_narozeni.day))
        return vek
    
    # Získání aktuálního data
    dnes = date.today()
    
    # Filtrace pojištěnců, kteří mají dnes narozeniny
    pojistenci_dnes = Pojistenci.objects.filter(datum_narozeni__day=dnes.day, datum_narozeni__month=dnes.month)
    
    # Vytvoření seznamu dvojic (pojištěnec, věk)
    pojistenci_a_vek = [(pojistenec, vek_na_zaklade_datum_narozeni(pojistenec.datum_narozeni)) for pojistenec in pojistenci_dnes]
    
    return render(request, 'index.html', {'pojistenci_a_vek': pojistenci_a_vek})

@login_required
def vypsat_vse(request):
    pojistenci = Pojistenci.objects.all()
    return render(request, 'vypsat_vse.html', {'pojistenci': pojistenci})

@login_required
def detail_pojistence(request, cislo_pojistence):
    try:
        # Získání pojištěnce podle čísla pojištěnce nebo vrácení 404 chyby pokud není nalezen
        pojistenec = get_object_or_404(Pojistenci, cislo_pojistence=cislo_pojistence)
    except DatabaseError:
        messages.error(request, 'Došlo k problému s databází. Zkuste to prosím později.')
        return redirect('index')  # Přesměrujte na vhodnou chybovou stránku nebo na úvodní stránku.
    except IntegrityError:
        messages.error(request, 'Došlo k chybě integrity při získávání detailu pojištěnce. Zkuste to prosím znovu.')
        return redirect('index')  # Přesměrujte na vhodnou chybovou stránku nebo na úvodní stránku.
    
    return render(request, 'vysledky_vyhledavani.html', {'vysledky': [pojistenec]})

@login_required
def editovat_pojistence(request, cislo_pojistence):
    pojistenec = get_object_or_404(Pojistenci, cislo_pojistence=cislo_pojistence)

    if request.method == 'POST':
        form = PojistenciForm(request.POST, instance=pojistenec)

        # Logujeme data z POST požadavku
        logger.info(f"Data z POST požadavku: {request.POST}")
        
        if form.is_valid():
            try:
                form.save()
                
                # Logování úspěšného uložení
                logger.info(f"Pojištěnec s číslem {cislo_pojistence} byl úspěšně upraven.")
                
                return redirect('detail_pojistence', cislo_pojistence=cislo_pojistence)
            except Exception as e:
                # Logování chyby při ukládání
                logger.error(f"Chyba při ukládání dat: {e}")
        else:
            print(form.errors)
            # Logujeme chyby ve formuláři
            logger.warning(f"Chyby ve formuláři PojistenciForm: {form.errors}")
    else:
        form = PojistenciForm(instance=pojistenec)

    return render(request, 'editovat_pojistence.html', {'form': form, 'pojistenec': pojistenec})





