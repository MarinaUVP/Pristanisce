import sqlite3
import csv

from modeli import *

def dodaj():
    '''Doda različne podatke.'''

    # Dadje
    dodajLadjo("Reks", 1972, 80)
    dodajLadjo("Titanik", 1920, 400)
    dodajLadjo("Pršec", 1996, 20)
    dodajLadjo("Sinji galeb", 1970, 10)
    dodajLadjo("Volarion", 200, 40)
    dodajLadjo("Nataša", 1995, 30)


    # Kabino
    dodajKabino("enojna", 4500, 2)

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
