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
        SELECT Potnik.ime, Potnik.priimek, Tip_kabine.tip, cena, Vozovnica.stevilo_lezisc, Nacrt_poti.naziv_potovanja, Izvedba_potovanja.datum_zacetka
        FROM Ima_vozovnico
        JOIN Potnik ON (Potnik.emso = Ima_vozovnico.emso_potnika)
        JOIN Vozovnica ON (Vozovnica.id = Ima_vozovnico.id_vozovnice)
        JOIN Izvedba_potovanja ON (Vozovnica.id_izvedbe_potovanja = Izvedba_potovanja.id)
        JOIN Nacrt_poti ON (Nacrt_poti.id = Izvedba_potovanja.id_nacrta_poti)
        JOIN Ladja ON (Izvedba_potovanja.id_ladje = Ladja.id)
        JOIN Kabina ON (Vozovnica.id_kabine = Kabina.id) --pridružiš kabino, ki je vezana na vozovnico
        JOIN Tip_kabine ON (Kabina.tip = Tip_kabine.id)
        LEFT JOIN Cena_kabine ON (Cena_kabine.id_nacrt_poti = Nacrt_poti.id)
        WHERE Cena_kabine.id_tip_kabine = Tip_kabine.id
        ORDER BY Potnik.emso, Izvedba_potovanja.datum_zacetka;
        """)
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
        FROM Ladja
        ORDER BY nosilnost;
        """)
    return sorted(cur.fetchall(), key=lambda x:x[3])


def poisciVseKabine():
    '''Vrne podatke o vseh kabinah.
    Namesto Id ladje vrne ime ladje, ki ji kabina pripada.'''
    cur.execute("""
        SELECT Ladja.ime, Tip_kabine.tip, stevilo_lezisc
        FROM Kabina
        JOIN Ladja ON Kabina.id_ladje = Ladja.id
        JOIN Tip_kabine ON Kabina.tip = Tip_kabine.id
        """)
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

def poisciVsaPotovanja():
    """Poišče vse podatke o potovanjih."""
    cur.execute("""
        SELECT Izvedba_potovanja.id, Kabina.id, naziv_potovanja, datum_zacetka, Ladja.ime, Tip_kabine.tip, cena, Kabina.stevilo_lezisc, 
              coalesce((SELECT SUM(Vozovnica.stevilo_lezisc)
                    FROM Vozovnica
                    JOIN Izvedba_potovanja AS x ON (Vozovnica.id_izvedbe_potovanja = x.id)
                    JOIN Kabina AS y ON (Vozovnica.id_kabine = y.id)
                    WHERE x.id = Izvedba_potovanja.id AND y.id = Kabina.id
              GROUP BY y.id, x.id),0) AS 'zasedenost'
        FROM Izvedba_potovanja
        JOIN Ladja ON (Ladja.id = Izvedba_potovanja.id_ladje)
        JOIN Nacrt_poti ON (Nacrt_poti.id = Izvedba_potovanja.id_nacrta_poti)
        JOIN Kabina ON (Kabina.id_ladje = Ladja.id)
        JOIN Tip_kabine ON (Tip_kabine.id = Kabina.tip)
        JOIN Cena_kabine ON (Cena_kabine.id_nacrt_poti = Nacrt_poti.id)
        WHERE Cena_kabine.id_tip_kabine = Tip_kabine.id
    """)
    return cur.fetchall()

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

def dodajVozovnico(stevilo_lezisc, id_izvedbe_potovanja, id_kabine, ime, priimek, emso):
    '''Doda vozovnico. Doda potnika, če ta še ne obstaja.'''
    # Najprej dodamo potnika, če ta še ne obstaja v bazi
    if poisciPotnika(ime, priimek) is None or str(poisciPotnika(ime, priimek)[0]) != str(emso):
        # Tega potnika še nimamo v bazi, zato ga moramo dodati
        cur.execute("""
            INSERT INTO Potnik (emso, ime, priimek)
            VALUES (?, ?, ?);
            """, (emso, ime, priimek))
        con.commit()
    # Sedaj ustvarimo vozovnico
    print(id_kabine, id_izvedbe_potovanja, stevilo_lezisc)
    cur.execute("""
        INSERT INTO Vozovnica (id_kabine, id_izvedbe_potovanja, stevilo_lezisc)
            VALUES (?, ?, ?);
        """, (id_kabine, id_izvedbe_potovanja, stevilo_lezisc))
    cur.execute("""
        SELECT last_insert_rowid();""")
    id_vozovnice = cur.fetchone()[0];
    print("Vozovnica, ki smo jo dodali ima id {}".format(id_vozovnice))
    # Povežemo še potnika z vozovnico.
    cur.execute("""
        INSERT INTO Ima_vozovnico (emso_potnika, id_vozovnice)
        VALUES (?, ?);
    """, (emso, id_vozovnice))
    con.commit()



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

def dodajIma_odsek(odhod, id_nacrta_poti, id_odseka):
    cur.execute("""
        INSERT INTO Ima_odsek (odhod, id_nacrta_poti, id_odseka_poti)
        VALUES (?, ?, ?);
        """, (odhod, id_nacrta_poti, id_odseka))
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

############### RAZNO ################

def potrebnoDolocitiCenoV1():
    """Izpis kombinacij, za katere še nismo določili cene kabin."""
    # Problem je, da spodnja koda ne deluje. Javi sytax error near ",". V SQLiteStudio pa dela.
    cur.execute("""
        SELECT naziv_potovanja, tip FROM Nacrt_poti
        JOIN Tip_kabine
        WHERE (Nacrt_poti.id, Tip_kabine.id) NOT IN
        (SELECT Cena_kabine.id_nacrt_poti, Cena_kabine.id_tip_kabine FROM Cena_kabine);
    """)
    cur.fetchall()


def potrebnoDolocitiCeno():
    """IZPIS kombinacij, za katere še NISMO DOLOČILI CENE KABIN."""
    cur.execute("""SELECT Cena_kabine.id_nacrt_poti, Cena_kabine.id_tip_kabine FROM Cena_kabine""")
    doloceneKabine = cur.fetchall()
    cur.execute("""
        SELECT naziv_potovanja, tip, Nacrt_poti.id, Tip_kabine.id FROM Nacrt_poti
        JOIN Tip_kabine;
        """)
    vseKabine = cur.fetchall()
    nedoloceneKabine = []
    for naziv_potovanja, tip, nacrt_poti_id, tip_kabine_id in vseKabine:
        if (nacrt_poti_id, tip_kabine_id) not in doloceneKabine:
            nedoloceneKabine.append((naziv_potovanja, tip))
    return nedoloceneKabine



