import modeli as modeli
from bottle import *
from datetime import datetime



@get('/')
def glavniMenu():
    return template('glavna.html')

@get('/ladja')
def prikaziLadje():
    vse_ladje = modeli.poisciVseLadje()
    return template('ladja.html', ladje = vse_ladje)

@get('/pristanisca')
def prikaziPristanisca():
    pristanisca = modeli.poisciVsaPristanisca()
    return template('pristanisca.html', pristanisca = pristanisca)


@get('/potovanje')
def prikaziPotovanja():
    return template('potovanje.html')


# Poženemo strežnik na vhodu 8080, glej http://localhost:8080/
run(host='localhost', port=8080, reloader=True, debug=True)
