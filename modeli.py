import sqlite3
import csv

BAZA = "ladja.db"
con = sqlite3.connect(BAZA)
cur = con.cursor()

# Funkcije iskanja

def poisciVsaPristanisca():
    """Vrne podatke o vseh pristaniščih."""
    cur.execute("""
        SELECT id, pristanisce
        FROM Pristanisce""")
    return cur.fetchall()

def poisciVseLadje():
    '''Vrne podatke o vseh ladjah.'''
    cur.execute("""
        SELECT id, ime, leto_izdelave, nosilnost
        FROM Ladja""")
    return cur.fetchall()

print(poisciVseLadje())


def poisciLadjo(ime):
    """Poišče vse podatke o ladji."""
    cur.execute("""
        SELECT id, ime, leto_izdelave, nosilnost
        FROM Ladja
        WHERE ime LIKE ?""", (ime,))
    print(cur.fetchall())
    return cur.fetchall()

print(poisciLadjo("Reks"))

def poisciPristanisce(pristanisce):
    """Vrne podatke o pristanišču."""
    cur.execute("""
        SELECT id, pristanisce FROM Pristanisce
        WHERE pristanisce LIKE ?""", (pristanisce,))
    return cur.fetchall()[0]





# Funkcije dodajanja

def dodajLadjo(ime, leto_izdelave, nosilnost):
    """Doda novo ladjo v tabelo Ladja"""
    cur.execute("""
        INSERT INTO Ladja (ime, leto_izdelave, nosilnost)
        VALUES (?, ?, ?)
        """, (ime, leto_izdelave, nosilnost))
    con.commit()

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



