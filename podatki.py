import sqlite3
import csv

from modeli import *

def dodaj():
    '''Doda različne podatke.'''

    # Ladje
    dodajLadjo("Reks", 1972, 80)
    dodajLadjo("Titanik", 1920, 400)
    dodajLadjo("Pršec", 1996, 20)
    dodajLadjo("Sinji galeb", 1970, 10)
    dodajLadjo("Volarion", 200, 40)
    dodajLadjo("Nataša", 1995, 30)


    # Dodaj tip kabine
    dodajTip_kabine("predsedniška")
    dodajTip_kabine("ekonomična")
    dodajTip_kabine("plebejska")
    dodajTip_kabine("meščanska")
    dodajTip_kabine("plemiška")

    # Dodaj potovanje
    dodajNacrt_poti("Karibi")

    # Kabino
    dodajKabino("enojna", 4500, 2)

    # Dodaj ceno kabine
    dodajCeno_kabine(500, 3, 1)


    # Pristanišče
    dodajPristanisce("Koper")
    dodajPristanisce("Izola")
    dodajPristanisce("Rimini")
    dodajPristanisce("Livorno")
    dodajPristanisce("Split")
    dodajPristanisce("Zagreb")

    # Potnika
    dodajPotnika(1, "Marina", "Kovač")
    dodajPotnika(2, "Jakob", "Valič")



try:
    print("Dodajam podatke...")
    dodaj()
    print("Dodajanje končano.")
except Exception as e:
    print("Zgodila se je napaka.", e)
