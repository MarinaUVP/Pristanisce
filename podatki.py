import sqlite3
import csv

from modeli import *

def dodaj():
    '''Doda različne podatke.'''

    # Dodamo ladjo
    dodajLadjo("Reks", 1972, 80)
    dodajLadjo("Titanik", 1920, 400)

    # Kabino
    dodajKabino("enojna", 1, 80, "Reks")

    # Pristanišče
    dodajPristanisce("Koper")
    dodajPristanisce("Izola")

    # Potnika
    dodajPotnika(1, "Marina", "Kovač")
    dodajPotnika(2, "Jakob", "Valič")

    # Pot
    dodajPot("Koper", "Izola", 1)
    dodajPot("Izola", "Koper", 1.4)

    # Načrt poti
    dodajNacrt_poti(1, 1, "2017-12-08")

    # Potovanje
    dodajPotovanje(1, 1, 1, 1) # Kako dodati, če vemo ime potnika, ladje, od kam do kam, datum

try:
    print("Dodajam podatke")
    dodaj()
except Exception as e:
    print("Zgodila se je napaka.", e)
