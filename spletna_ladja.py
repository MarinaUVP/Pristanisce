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
@get('/dodaj_ladjo')
def prikaziDodajLadjo():
    '''Prikaže stran za dodajanje novih ladij.'''
    vse_ladje = modeli.poisciVseLadje()
    return template('dodaj_ladjo.html', ladje=vse_ladje)

@post('/dodaj_ladjo_v_bazo')
def dodajLadjo():
    ime = request.forms.ime
    leto_izdelave = request.forms.leto_izdelave
    nosilnost = request.forms.nosilnost
    try:
        modeli.dodajLadjo(ime, leto_izdelave, nosilnost)
    except Exception as e:
        print("Zgodila se je napaka {} pri dodajanju ladje {}", e, ime)
    redirect('/dodaj_ladjo')

# Pristanišče
@get('/dodaj_pristanisce')
def prikaziDodajPristanisce():
    '''Prikaže stran za dodajanje pristanišč.'''
    pristanisca = modeli.poisciVsaPristanisca()
    return template('dodaj_pristanisce.html', pristanisca=pristanisca)

@post('/dodaj_pristanisce_v_bazo')
def dodajPristanisce():
    pristanisce = request.forms.pristanisce
    try:
        modeli.dodajPristanisce(pristanisce)
    except Exception as e:
        print("Zgodila se je napaka {} pri dodajanju pristanišča {}", e, pristanisce)
    redirect('/dodaj_pristanisce')

# Kabino
@get('/dodaj_kabino')
def prikaziDodajKabino():
    '''Prikaže stran za dodajanje kabine.'''
    ladje = modeli.poisciVseLadje()
    vse_kabine = modeli.poisciVseKabine()
    return template('dodaj_kabino.html', ladje = ladje, kabine=vse_kabine)

@post('/dodaj_kabino_v_bazo')
def dodajKabino():
    '''Dodamo kabinko v bazo.'''
    stevilo_lezisc = request.forms.stevilo_lezisc
    # Rabimo še podatek o ladji
    id_ladje = request.forms.izbira_ladij
    try:
        modeli.dodajKabino("udobna", stevilo_lezisc, id_ladje)
    except Exception as e:
        print("Zgodila se je napaka {} pri dodajanju sobe s {} ležišči za ladjo {}.".format(e, stevilo_lezisc, id_ladje))
    redirect('/dodaj_kabino')


############  ADMINISTRATOR  ##############
@get('/administrator')
def glavniMenu():
    return template('administrator.html')


#=================================================


# Poženemo strežnik na vhodu 8080, glej http://localhost:8080/
run(host='localhost', port=8080, reloader=True, debug=True)
