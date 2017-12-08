import sqlite3
import csv

BAZA = "ladja.db"
con = sqlite3.connect(BAZA)
cur = con.cursor()

def dodajLadjo(ime, leto_izdelave, nosilnost):
    """Doda novo ladjo v tabelo Ladja"""
    cur.execute("""
        INSERT INTO Ladja (ime, leto_izdelave, nosilnost)
        VALUES (?, ?, ?)
        """, (ime, leto_izdelave, nosilnost))
    con.commit()

def poisciLadjo(ime):
    """Poišče podatke o ladji."""
    cur.execute("""
        SELECT id, ime, leto_izdelave, nosilnost
        FROM Ladja
        WHERE ime LIKE ?""", (ime,))
    return cur.fetchall()[0]

def dodajKabino(tip, stevilo_lezisc, cena, ime_ladje, zasedena=False):
    """Doda kabino v ladjo. Dobi ime ladje in se pozanima za id ladje."""
    id_ladje, _, _, _ = poisciLadjo(ime_ladje)
    cur.execute("""
        INSERT INTO Kabina (tip, stevilo_lezisc, zasedena, cena, id_ladje)
        VALUES (?, ?, ?, ?, ?)
        """, (tip, stevilo_lezisc, zasedena, cena, id_ladje))
    con.commit()

def dodajPristanisce(pristanisce):
    """Doda seznam pristanišč."""
    cur.execute("""
        INSERT INTO Pristanisce (pristanisce)
        VALUES (?)
        """, (pristanisce,))
    con.commit()

def dodajPotnika(emso, ime, priimek):
    """Doda potnika."""
    cur.execute("""
        INSERT INTO Potnik (emso, ime, priimek)
        VALUES (?, ?, ?)
        """, (emso, ime, priimek))
    con.commit()

def poisciPristanisce(pristanisce):
    """Vrne podatke o pristanišču."""
    cur.execute("""
        SELECT id, pristanisce FROM Pristanisce
        WHERE pristanisce LIKE ?""", (pristanisce,))
    return cur.fetchall()[0]

def dodajPot(zacetno_pristanisce, koncno_pristanisce, trajanje):
    """Doda pot. Pozanima se za id začetnega in končnega pristanišča."""
    zacetek, _ = poisciPristanisce(zacetno_pristanisce)
    konec, _ = poisciPristanisce(koncno_pristanisce)
    cur.execute("""
        INSERT INTO Pot (zacetek, konec, trajanje)
        VALUES (?, ?, ?)
        """, (zacetek, konec, trajanje))
    con.commit()

def dodajNacrt_poti(id_ladje, id_poti):
    """Povezuje ladjo s potjo."""
    cur.execute("""
        INSERT INTO Nacrt_Poti (id_ladje, id_poti)
        VALUES (?, ?);
        """, (id_ladje, id_poti))
    con.commit()

def dodajPotovanje(emso, id_ladje, id_poti, id_kabine, datum):
    """Poveže tabelo Osebe z Ladjo, Potjo in Kabino."""
    cur.execute("""
        INSERT INTO Potovanje (emso, id_ladje, id_poti, id_kabine, datum)
        VALUES (?, ?, ?, ?, ?);
        """, (emso, id_ladje, id_poti, id_kabine, datum))
    con.commit()




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
    dodajNacrt_poti(1, 1)

    # Potovanje
    dodajPotovanje(1, 1, 1, 1, "2017-12-08") # Kako dodati, če vemo ime potnika, ladje, od kam do kam, datum

try:
    dodaj()
except:
    pass