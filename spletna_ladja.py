import modeli as modeli
from bottle import *
from datetime import datetime



@get('/')
def glavniMenu():
    kuzkiTrije = ['Fifo', 'Reks', 'Floki']
    ladje = ['Reks', 'Titanik', 'Ribič']
    t = modeli.poisciLadjo('Reks')
    ladje += [t]
    return template('glavna.html', ladje=ladje+kuzkiTrije, ime_ladje="FlokiII")


@post('/dodaj')
def dodaj():
    ime = 'Reksona'
    leto_izdelave = 1991
    nosilnost = 12
    try:
        modeli.dodajLadjo(ime, leto_izdelave, nosilnost)
    except Exception as e:
        print(e)
    redirect('/')

@get('/ladja')
def prikaziLadje():
    return template('ladja.html')

@get('/pristanisca')
def prikaziPristanisca():
    return template('pristanisca.html')


@get('/potovanje')
def prikaziPotovanja():
    return template('potovanje.html')


# Poženemo strežnik na vhodu 8080, glej http://localhost:8080/
run(host='localhost', port=8080, reloader=True, debug=True)
