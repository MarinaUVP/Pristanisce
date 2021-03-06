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
    potovanje = modeli.poisciVsaPotovanja()
    return template('potovanje.html', potovanje=potovanje)

@post('/nakup_vozovnice')
def kupiVozovnico():
    stevilo_lezisc = request.forms.stevilo_lezisc
    if int(stevilo_lezisc) == 0:
        redirect('/potovanje')
    id_izvedbe_potovanja = request.forms.id_izvedbe_potovanja
    id_kabine = request.forms.id_kabine
    return template('nakup_vozovnice.html',stevilo_lezisc=stevilo_lezisc,
                    id_izvedbe_potovanja=id_izvedbe_potovanja, id_kabine=id_kabine)

@get('/administrator/kupljene_vozovnice')
def prikaziKupljeneVozovnice():
    vozovnice = modeli.poisciVseVozovnice()
    return template('kupljene_vozovnice.html', vozovnice=vozovnice)

@post('/administrator/dodaj_vozovnico_v_bazo')
def dodajVozovnico():
    stevilo_lezisc = request.forms.stevilo_lezisc
    id_izvedbe_potovanja = request.forms.id_izvedbe_potovanja
    id_kabine = request.forms.id_kabine
    ime = request.forms.ime
    priimek = request.forms.priimek
    emso = request.forms.emso
    try:
        modeli.dodajVozovnico(stevilo_lezisc, id_izvedbe_potovanja, id_kabine, ime, priimek, emso)
        return template('potrdilo_nakupa.html')
    except Exception as e:
        print("Zgodila se je napaka {} pri nakupu vozovnice.".format(e))
    redirect('/potovanje')


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
        print("Zgodila se je napaka {} pri dodajanju ladje {}".format(e, ime))
    redirect('/administrator/dodaj_ladjo')


# Načrt poti
@get('/administrator/dodaj_nacrt_poti')
def prikaziDodajNacrtPoti():
    '''Prikaže stran za dodajanje načrta poti.'''
    odseki = modeli.poisciVseOdseke()
    pristanisca = modeli.poisciVsaPristanisca()
    vsi_nacrti_poti = modeli.poisciVseNacrtePoti()
    return template('dodaj_nacrt_poti.html', vsi_nacrti_poti=vsi_nacrti_poti, odseki=odseki, pristanisca=pristanisca)


@post('/administrator/dodaj_nacrt_poti_v_bazo')
def dodajNacrtPoti():
    naziv_potovanja = request.forms.naziv_potovanja
    try:
        modeli.dodajNacrt_poti(naziv_potovanja)
    except Exception as e:
        print("Zgodila se je napaka {} pri dodajanju načrta poti: {}".format(e, naziv_potovanja))
    redirect('/administrator/dodaj_nacrt_poti')


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
        print("Zgodila se je napaka {} pri dodajanju pristanišča {}".format(e, pristanisce))
    redirect('/administrator/dodaj_pristanisce')


@post('/administrator/dodaj_odsek_v_bazo')
def dodajOdsek():
    id_zacetnega_pristanisca = request.forms.id_zacetnega_pristanisca
    id_koncnega_pristanisca = request.forms.id_koncnega_pristanisca
    cas_potovanja = request.forms.cas_potovanja
    try:
        modeli.dodajOdsek(id_zacetnega_pristanisca, id_koncnega_pristanisca, cas_potovanja)
    except Exception as e:
        print("Zgodila se je napaka {} pri dodajanju odseka {}".format((e, (id_zacetnega_pristanisca, id_koncnega_pristanisca))))
    redirect('/administrator/dodaj_nacrt_poti')


# Ima odsek
@post('/administrator/dodaj_ima_odsek_v_bazo')
def dodajImaOdsek():
    id_nacrta_poti = request.forms.id_nacrta_poti
    id_odseka = request.forms.id_odseka
    odhod = request.forms.odhod
    try:
        modeli.dodajIma_odsek(odhod, id_nacrta_poti, id_odseka)
    except Exception as e:
        print(e)
    redirect('/administrator/dodaj_nacrt_poti')


# Izvedba potovanja
@get('/administrator/dodaj_izvedbo_potovanja')
def prikaziDodajPotovanje():
    '''Prikaže stran za dodajanje izvedbe potovanja.'''
    nacrti_poti = modeli.poisciVseNacrtePoti()
    ladje = modeli.poisciVseLadje()
    return template('dodaj_izvedbo_potovanja', nacrti_poti=nacrti_poti, ladje=ladje)


@post('/administrator/dodaj_izvedbo_potovanja_v_bazo')
def dodajIzvedboPotovanja():
    id_ladje = request.forms.id_ladje
    id_nacrta_poti = request.forms.id_nacrta_poti
    datum_zacetka = request.forms.datum_zacetka
    try:
        modeli.dodajIzvedbo_potovanja(datum_zacetka, id_nacrta_poti, id_ladje)
    except Exception as e:
        print(e)
    redirect('/administrator/dodaj_izvedbo_potovanja')



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
    vse_cene_kabin = modeli.poisciVseCeneKabin()
    nedolocene_cene_kabin = modeli.potrebnoDolocitiCeno()
    return template('dodaj_ceno_kabine.html', tipi_kabin = vsi_tipi_kabin, potovanja = vsa_potovanja, cene_kabin=vse_cene_kabin, nedolocene_cene_kabin=nedolocene_cene_kabin)

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

@get('/prikazi_prijavo')
def priakzi_admin():
    # return template('prijava_admin.html')
    redirect('/administrator')

@post("/prijavi_administratorja")
def preveriAdministratorja():
    uporabnisko_ime = request.forms.UI
    geslo = request.forms.geslo
    # /preveri identiteto v bazi
    redirect('/administrator')

#=================================================


# Poženemo strežnik na vhodu 8080, glej http://localhost:8080/
run(host='localhost', port=8080, reloader=True, debug=True)