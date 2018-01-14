import sqlite3
import csv

BAZA = "ladja.db"
con = sqlite3.connect(BAZA)
cur = con.cursor()
cur.execute("PRAGMA foreign_keys = ON")

############### POIZVEDBE ################

def poisciVsaPristanisca():
    """Vrne podatke o vseh pristaniščih."""
    cur.execute("""
        SELECT id, pristanisce
        FROM Pristanisce""")
    return cur.fetchall()

def poisciVsePotnike():
    """Vrne podatke o vseh potnikih."""
    cur.execute("""
        SELECT *
        FROM Potnik""")
    return cur.fetchall()

def poisciVseVozovnice():
    """Vrne podatke o vseh vozovnicah."""
    cur.execute("""
        SELECT *
        FROM Vozovnica""")
    return cur.fetchall()

def poisciVseOdseke():
    """Vrne podatke o vseh odsekih poti."""
    cur.execute("""
        SELECT Odsek.id, x.pristanisce, y.pristanisce, cas_potovanja
        FROM Odsek
        JOIN Pristanisce AS x ON Odsek.id_zacetnega_pristanisca = x.id
        JOIN Pristanisce AS y ON Odsek.id_koncnega_pristanisca = y.id
        ;""")
    return cur.fetchall()

def poisciVseLadje():
    '''Vrne podatke o vseh ladjah.'''
    cur.execute("""
        SELECT id, ime, leto_izdelave, nosilnost
        FROM Ladja""")
    return cur.fetchall()


def poisciVseKabine():
    '''Vrne podatke o vseh kabinah.
    Namesto Id ladje vrne ime ladje, ki ji kabina pripada.'''
    cur.execute("""
        SELECT Ladja.ime, tip, stevilo_lezisc
        FROM Kabina
        JOIN Ladja ON Kabina.id_ladje = Ladja.id""")
    return sorted(cur.fetchall(), key=lambda nabor:nabor[0]) # Kabine z iste ladje izpišemo skupaj

def poisciVseTipeKabin():
    """Poišče vse tipe kabin."""
    cur.execute("""
        SELECT id, tip FROM Tip_kabine;
        """)
    return cur.fetchall()

def poisciVseNacrtePoti():
    """Poišče vse načrte poti."""
    cur.execute("""
        SELECT id, naziv_potovanja FROM Nacrt_poti;
    """)
    return cur.fetchall()

def poisciVseCeneKabin():
    """Poišče vse cene kabin glede na tip kabine in potovanje."""
    cur.execute("""
        SELECT Nacrt_poti.naziv_potovanja, Tip_kabine.tip, cena FROM Cena_kabine
        JOIN Tip_kabine ON Cena_kabine.id_tip_kabine = Tip_kabine.id
        JOIN Nacrt_poti ON Cena_kabine.id_nacrt_poti = Nacrt_poti.id;
    """)
    return sorted(cur.fetchall(), key=lambda lastnost: lastnost[0])

def poisciLadjo(ime):
    """Poišče podatke o ladji na podlagi njenega imena."""
    cur.execute("""
        SELECT id, ime, leto_izdelave, nosilnost
        FROM Ladja
        WHERE ime LIKE ?""", (ime,))
    return cur.fetchone()

def poisciPristanisce(pristanisce):
    """Vrne podatke o pristanišču na podlagi njegovega imena."""
    cur.execute("""
        SELECT id, pristanisce FROM Pristanisce
        WHERE pristanisce LIKE ?""", (pristanisce,))
    return cur.fetchone()

def poisciPotnika(ime, priimek):
    """Vrne podatke o potniku na podlagi njegovega imena in priimka."""
    cur.execute("""
        SELECT emso, ime, priimek FROM Potnik
        WHERE ime = ? AND PRIIMEK = ?;""", (ime, priimek))
    return cur.fetchone()




################ DODAJANJE #####################

def dodajLadjo(ime, leto_izdelave, nosilnost):
    """Doda novo ladjo v tabelo Ladja"""
    cur.execute("""
        INSERT INTO Ladja (ime, leto_izdelave, nosilnost)
        VALUES (?, ?, ?)
        """, (ime, leto_izdelave, nosilnost))
    con.commit()

def dodajKabino(tip, stevilo_lezisc, id_ladje):
    """Doda kabino v ladjo. Dobi ime ladje in se pozanima za id ladje."""
    cur.execute("""
        INSERT INTO Kabina (tip, stevilo_lezisc, id_ladje)
        VALUES (?, ?, ?)
        """, (tip, stevilo_lezisc, id_ladje))
    con.commit()

def dodajPristanisce(pristanisce):
    """Doda seznam pristanišč."""
    cur.execute("""
        INSERT INTO Pristanisce (pristanisce)
        VALUES (?)
        """, (pristanisce,))
    con.commit()

def dodajOdsek(id_zacetnega_pristanisca, id_koncnega_pristanisca, cas_potovanja):
    cur.execute("""
        INSERT INTO Odsek (id_zacetnega_pristanisca, id_koncnega_pristanisca, cas_potovanja)
        VALUES (?, ?, ?)
        """, (id_zacetnega_pristanisca, id_koncnega_pristanisca, cas_potovanja))
    con.commit()

def dodajIma_odsek(postanek, id_nacrta_poti, id_odseka):
    cur.execute("""
        INSERT INTO Ima_odsek (postanek, id_nacrta_poti, id_odseka_poti)
        VALUES (?, ?, ?);
        """, (postanek, id_nacrta_poti, id_odseka))
    con.commit()

def dodajIzvedbo_potovanja(datum_zacetka, id_nacrta_poti, id_ladje):
    cur.execute("""
        INSERT INTO Izvedba_potovanja (datum_zacetka, id_nacrta_poti, id_ladje)
        VALUES (?, ?, ?);
        """, (datum_zacetka, id_nacrta_poti, id_ladje))
    con.commit()

def dodajPotnika(emso, ime, priimek):
    """Doda potnika."""
    cur.execute("""
        INSERT INTO Potnik (emso, ime, priimek)
        VALUES (?, ?, ?)
        """, (emso, ime, priimek))
    con.commit()

def dodajTip_kabine(tip):
    """Doda tip kabine."""
    cur.execute("""
        INSERT INTO Tip_kabine(tip)
        VALUES (?)
        """, (tip,))
    con.commit()

def dodajCeno_kabine(cena_kabine, id_tip_kabine, id_nacrt_poti):
    """Doda ceno kabine."""
    cur.execute("""
        INSERT INTO Cena_kabine(cena, id_tip_kabine, id_nacrt_poti)
        VALUES (?, ?, ?)
        """, (cena_kabine, id_tip_kabine, id_nacrt_poti))
    con.commit()

def dodajNacrt_poti(naziv_potovanja):
    """Povezuje ladjo s potjo."""
    cur.execute("""
        INSERT INTO Nacrt_Poti (naziv_potovanja)
        VALUES (?);
        """, (naziv_potovanja,))
    con.commit()




