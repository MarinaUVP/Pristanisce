import sqlite3
import csv

baza = "ladja.db"
con = sqlite3.connect(baza)
cur = con.cursor()


def poisciLadjo(ime):
    """Poišče podatke o ladji."""
    cur.execute("""
        SELECT id, ime, leto_izdelave, nosilnost
        FROM Ladja
        WHERE ime LIKE ?""", (ime,))
    return cur.fetchall()[0]

def dodajLadjo(ime, leto_izdelave, nosilnost):
    """Doda novo ladjo v tabelo Ladja"""
    cur.execute("""
        INSERT INTO Ladja (ime, leto_izdelave, nosilnost)
        VALUES (?, ?, ?)
        """, (ime, leto_izdelave, nosilnost))
    con.commit()