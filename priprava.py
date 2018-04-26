# Ustvarimo bazo in tabele

import sqlite3


IME_BAZE = "ladja.db"

# POZOR!!!
# Najprej pobrišemo staro datoteko, da nimamo težav s tabelami, ki že obastajajo
# Nevarnost je, da hkrati pobrišemo tudi podatke
import os
if os.path.exists(IME_BAZE):
    os.remove(IME_BAZE)

con = sqlite3.connect(IME_BAZE)
cur = con.cursor()

def ustvariTabeloLadja():
    cur.execute("""
        CREATE TABLE Ladja (
        id                  INTEGER PRIMARY KEY,
        ime                 CHAR NOT NULL UNIQUE,
        leto_izdelave       INTEGER,
        nosilnost           INTEGER NOT NULL);
        """)

def ustvariTabeloPotnik():
    cur.execute("""
        CREATE TABLE Potnik (
        emso                INTEGER PRIMARY KEY,
        ime                 CHAR    NOT NULL,
        priimek             CHAR    NOT NULL);
        """)

def ustvariTabeloKabina():
    cur.execute("""
        CREATE TABLE Kabina (
        id                  INTEGER PRIMARY KEY AUTOINCREMENT,
        tip                 CHAR NOT NULL,
        stevilo_lezisc      INTEGER NOT NULL,
        id_ladje            INTEGER NOT NULL,
        FOREIGN KEY(id_ladje)  REFERENCES Ladja(id),
        UNIQUE (id, id_ladje));
        """)

def ustvariTabeloIma_kabino():
    cur.execute("""
        CREATE TABLE Ima_kabino (
        id_kabine           INTEGER REFERENCES Kabina(id),
        id_ladje            INTEGER REFERENCES Ladja(id),
        UNIQUE (id, id_ladje);
        """)

def ustvariTabeloPristanisce():
    cur.execute("""
        CREATE TABLE Pristanisce (
        id                  INTEGER PRIMARY KEY AUTOINCREMENT,
        pristanisce         CHAR NOT NULL);
        """)

def ustvariTabeloOdsek():
    cur.execute("""
        CREATE TABLE Odsek (
        id                  INTEGER PRIMARY KEY AUTOINCREMENT,
        id_zacetnega_pristanisca    REFERENCES Pristanisce (id),
        id_koncnega_pristanisca     REFERENCES Pristanisce (id),
        cas_potovanja       INTEGER NOT NULL,
        UNIQUE (id_zacetnega_pristanisca, id_koncnega_pristanisca, cas_potovanja)
        );
        """)

def ustvariTabeloIma_odsek():
    cur.execute("""
        CREATE TABLE Ima_odsek (
        odhod         DATE,
        id_nacrta_poti      REFERENCES Nacrt_poti (id),
        id_odseka_poti      REFERENCES Odsek (id)
        );
        """)

def ustvariTabeloPot():
    cur.execute("""
        CREATE TABLE Pot (
        id                  INTEGER PRIMARY KEY AUTOINCREMENT,
        zacetek             INTEGER NOT NULL,
        konec               INTEGER NOT NULL,
        trajanje            INTEGER NOT NULL,
        UNIQUE (zacetek, konec, trajanje),
        FOREIGN KEY(zacetek) REFERENCES Pristanisce(id),
        FOREIGN KEY(konec) REFERENCES Pristanisce(id));
        """)

def ustvariTabeloNacrt_poti():
    cur.execute("""
        CREATE TABLE Nacrt_poti (
        id                  INTEGER PRIMARY KEY AUTOINCREMENT,
        naziv_potovanja     CHAR NOT NULL UNIQUE);
        """)



def ustvariTabeloTip_kabine():
    cur.execute("""
        CREATE TABLE Tip_kabine (
        id                  INTEGER PRIMARY KEY AUTOINCREMENT,
        tip                 CHAR NOT NULL UNIQUE
        );
    """)

def ustvariTabeloCena_kabine():
    cur.execute("""
    CREATE TABLE Cena_kabine (
    cena                    INTEGER PRIMARY KEY,
    id_tip_kabine           REFERENCES Tip_kabine(id),
    id_nacrt_poti           REFERENCES Nacrt_poti(id),
    UNIQUE(id_tip_kabine, id_nacrt_poti)
    );
    """)

def ustvariTabeloIzvedba_potovanja():
    cur.execute("""
    CREATE TABLE Izvedba_potovanja (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    datum_zacetka           DATE,
    id_nacrta_poti          REFERENCES Nacrt_poti(id),
    id_ladje                REFERENCES Ladja(id),
    UNIQUE (id_ladje, datum_zacetka)
    );
    """)

def ustvariTabeloVozovnica():
    cur.execute("""
    CREATE TABLE Vozovnica (
    emso_potnika            REFERENCES Potnik(emso),
    id_kabine               REFERENCES Kabina(id),
    id_izvedbe_potovanja    REFERENCES Izvedba_potovanja(id),
    UNIQUE (emso_potnika, id_kabine, id_izvedbe_potovanja)
    );
    """)


for tabela in ["Ladja", "Potnik", "Pristanisce", "Kabina", "Pot", "Nacrt_poti", "Tip_kabine", "Cena_kabine", "Odsek", "Ima_odsek", "Izvedba_potovanja", "Vozovnica"]:
    eval("ustvariTabelo{0}()".format(tabela))

import podatki


