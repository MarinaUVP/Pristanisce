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
    id                  PRIMARY KEY,
    leto_izdelave       INTEGER,
    nosilnost           INTEGER NOT NULL);
    """)

def ustvariTabeloPotnik():
    cur.execute("""
    CREATE TABLE Potnik (
    emso                PRIMARY KEY,
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
    FOREIGN KEY(zacetek) REFERENCES Pristanisce(id),
    FOREIGN KEY(konec) REFERENCES Pristanisce(id));
    """)

def ustvariTabeloNacrt_poti():
    cur.execute("""
    CREATE TABLE Nacrt_poti (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    id_ladje            INTEGER NOT NULL,
    id_poti             INTEGER NOT NULL,
    FOREIGN KEY (id_ladje) REFERENCES Ladja(id),
    FOREIGN KEY (id_poti)  REFERENCES Pot(id));
    """)


def ustvariTabeloPotovanje():
    cur.execute("""
    CREATE TABLE Potovanje (
    emso                INTEGER NOT NULL,
    id_ladje            INTEGER NOT NULL,
    id_poti             INTEGER NOT NULL,
    id_kabine           INTEGER NOT NULL,
    datum               DATE NOT NULL,
    FOREIGN KEY (id_ladje, id_poti, datum) REFERENCES Nacrt_poti(id_ladje, id_poti, datum),
    FOREIGN KEY (id_kabine, id_ladje) REFERENCES Kabina(id, id_ladje),
    PRIMARY KEY (emso, id_poti, datum, id_kabine));
    """)

for tabela in ["Ladja", "Potnik", "Pristanisce", "Kabina", "Pot", "Nacrt_poti", "Potovanje"]:
    eval("ustvariTabelo{0}()".format(tabela))


