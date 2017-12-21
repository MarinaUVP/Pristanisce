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
        zasedena            BOOLEAN,
        cena                INTEGER NOT NULL,
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
        id_ladje            INTEGER NOT NULL,
        id_poti             INTEGER NOT NULL,
        datum               DATE NOT NULL,
        UNIQUE (id_ladje, id_poti, datum),
        FOREIGN KEY (id_ladje) REFERENCES Ladja(id),
        FOREIGN KEY (id_poti)  REFERENCES Pot(id));
        """)


def ustvariTabeloPotovanje():
    """Tu lahko id_ladje in id_poti nadomestimo z id_nacrta_poti."""

    cur.execute("""
        CREATE TABLE Potovanje (
        emso                INTEGER NOT NULL,
        id_nacrta_poti      INTEGER NOT NULL,
        id_kabine           INTEGER NOT NULL,
        FOREIGN KEY (emso) REFERENCES Potnik (emso),
        FOREIGN KEY (id_nacrta_poti) REFERENCES Nacrt_poti(id),
        FOREIGN KEY (id_kabine) REFERENCES Kabina(id),
        PRIMARY KEY (emso, id_nacrta_poti, id_kabine));
        """)

for tabela in ["Ladja", "Potnik", "Pristanisce", "Kabina", "Pot", "Nacrt_poti", "Potovanje"]:
    eval("ustvariTabelo{0}()".format(tabela))

import podatki


