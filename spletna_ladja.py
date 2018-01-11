import modeli as modeli
from bottle import *
from datetime import datetime

# Naložimo CSS datoteko
@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='static')

# Glavni meni
@get('/')
def glavniMenu():
    return template('glavna.html')

############  IZPISOVANJE  #############

@get('/izpis_pristanisc')
def prikaziPristanisca():
    pristanisca = modeli.poisciVsaPristanisca()
    return template('izpis_pristanisc.html', pristanisca = pristanisca)

@get('/izpis_ladij')
def prikaziLadje():
    vse_ladje = modeli.poisciVseLadje()
    return template('izpis_ladij.html', ladje = vse_ladje)

@get('/izpis_kabin')
def izpisiKabine():
    vse_kabine = modeli.poisciVseKabine()
    return template('izpis_kabin.html', kabine = vse_kabine)

@get('/potovanje')
def prikaziPotovanja():
    return template('potovanje.html')

############  DODAJANJE  ##############

# Ladjo
@get('/administrator/dodaj_ladjo')
def prikaziDodajLadjo():
    '''Prikaže stran za dodajanje novih ladij.'''
    vse_ladje = modeli.poisciVseLadje()
    return template('dodaj_ladjo.html', ladje=vse_ladje)

@post('/administrator/dodaj_ladjo_v_bazo')
def dodajLadjo():
    ime = request.forms.ime
    leto_izdelave = request.forms.leto_izdelave
    nosilnost = request.forms.nosilnost
    try:
        modeli.dodajLadjo(ime, leto_izdelave, nosilnost)
    except Exception as e:
        print("Zgodila se je napaka {} pri dodajanju ladje {}", e, ime)
    redirect('/administrator/dodaj_ladjo')

# Pristanišče
@get('/administrator/dodaj_pristanisce')
def prikaziDodajPristanisce():
    '''Prikaže stran za dodajanje pristanišč.'''
    pristanisca = modeli.poisciVsaPristanisca()
    return template('dodaj_pristanisce.html', pristanisca=pristanisca)

@post('/administrator/dodaj_pristanisce_v_bazo')
def dodajPristanisce():
    pristanisce = request.forms.pristanisce
    try:
        modeli.dodajPristanisce(pristanisce)
    except Exception as e:
        print("Zgodila se je napaka {} pri dodajanju pristanišča {}", e, pristanisce)
    redirect('/administrator/dodaj_pristanisce')

# Kabino
@get('/administrator/dodaj_kabino')
def prikaziDodajKabino():
    '''Prikaže stran za dodajanje kabine.'''
    ladje = modeli.poisciVseLadje()
    vse_kabine = modeli.poisciVseKabine()
    vsi_tipi_kabin = modeli.poisciVseTipeKabin()
    return template('dodaj_kabino.html', ladje = ladje, kabine=vse_kabine, tipi_kabin= vsi_tipi_kabin)

@post('/administrator/dodaj_kabino_v_bazo')
def dodajKabino():
    '''Dodamo kabinko v bazo.'''
    stevilo_lezisc = request.forms.stevilo_lezisc
    # Rabimo še podatek o ladji
    id_ladje = request.forms.izbira_ladij
    tip_kabine = request.forms.izbira_tipa_kabine
    try:
        modeli.dodajKabino(tip_kabine, stevilo_lezisc, id_ladje)
    except Exception as e:
        print("Zgodila se je napaka {} pri dodajanju sobe s {} ležišči za ladjo {}.".format(e, stevilo_lezisc, id_ladje))
    redirect('/administrator/dodaj_kabino')

# Cena kabine
@get('/administrator/dodaj_ceno_kabine')
def prikaziCenoKabine():
    '''Prikaže stran za dodajanje kabine.'''
    vsi_tipi_kabin = modeli.poisciVseTipeKabin()
    vsa_potovanja = modeli.poisciVseNacrtePoti()
    return template('dodaj_ceno_kabine.html', tipi_kabin = vsi_tipi_kabin, potovanja = vsa_potovanja)

@post('/administrator/dodaj_ceno_kabine_v_bazo')
def dodajCenoKabine():
    """Dodamo ceno kabine v bazo."""
    cena_kabine = request.forms.cena_kabine
    id_tip_kabine = request.forms.izbira_tipa_kabine
    id_potovanje = request.forms.izbira_nacrta_poti
    try:
        modeli.dodajCeno_kabine(cena_kabine, id_tip_kabine, id_potovanje)
    except Exception as e:
        print("Zgodila se je napaka {} pri dodajanju cene kabine {} na potovanju {}.".format(e, id_tip_kabine, id_potovanje))
    redirect('/administrator/dodaj_ceno_kabine')





############  ADMINISTRATOR  ##############
@get('/administrator')
def glavniMenu():
    return template('administrator.html')


#=================================================


# Poženemo strežnik na vhodu 8080, glej http://localhost:8080/
run(host='localhost', port=8080, reloader=True, debug=True)
