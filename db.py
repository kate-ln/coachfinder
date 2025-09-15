'''
Tietokantamoduuli, jonka kautta voidaan suorittaa tietokantakomentoja, ilman,
että tarvitaan muodostaa jokaiselle sivulle erillinen tietokantayhteys.
'''
import sqlite3
from flask import g

def get_connection():
    '''Muodostaa ja palauttaa yhteyden tietokantaan. Tätä funktiota kutsutaan muissa funktioissa ennen tietokannan käyttämistä.'''
    con = sqlite3.connect("database.db")
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    return con

def execute(sql, params=[]):
    '''Suorittaa komennon, joka muuttaa tietokantaa (kuten INSERT, UPDATE tai DELETE). Funktiolle annetaan parametrina mahdolliset komentoon tulevat parametrit. Funktio kutsuu metodia commit, jolloin muutos viedään pysyvästi tietokantaan.'''
    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    g.last_insert_id = result.lastrowid
    con.close()

def last_insert_id():
    return g.last_insert_id    
    
def query(sql, params=[]):
    '''Suorittaa tietoa hakevan SELECT-komennon. Funktio hakee kaikki kyselyn tulokset metodilla fetchall ja palauttaa ne.'''
    con = get_connection()
    result = con.execute(sql, params).fetchall()
    con.close()
    return result
