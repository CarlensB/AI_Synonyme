import sqlite3
import traceback

CHEMIN_BD = 'cooccurrences.db'
FK_ON = 'PRAGMA foreign_keys = 1'

NOM_TABLE = "mot_synonyme"

CREER_COOCCURENCES = '''
    CREATE TABLE IF NOT EXISTS cooccurences (
        rangee INTEGER NOT NULL,
        colonne INTEGER NOT NULL,
        fenetre INTEGER NOT NULL,
        valeur INTEGER NOT NULL,
        
        PRIMARY KEY(rangee,colonne,fenetre)
        FOREIGN KEY(rangee)
            REFERENCES mots (id)
        FOREIGN KEY(colonne)
            REFERENCES mots (id)
    );
'''

CREER_MOTS = '''
    CREATE TABLE IF NOT EXISTS mots(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mot TEXT UNIQUE NOT NULL
    );
'''
INSERT_COOCCURENCES = ''' INSERT OR REPLACE INTO cooccurences (rangee,colonne,fenetre,valeur) VALUES(?,?,?,?)'''

INSERT_MOT = '''
    INSERT INTO mots(mot,id) VALUES(?,?)
'''

COUNT_MOTS = '''SELECT COUNT(*) FROM mots'''

DROP_TABLE = '''
    DROP TABLE IF EXISTS mot_synonyme
'''

SELECT_ID = "SELECT id FROM mots WHERE mot = ?"

SELECT_MOTS = "SELECT * FROM mots"

SELECT_COOCCURENCES = "SELECT rangee,colonne,valeur FROM cooccurences WHERE fenetre = ?"

DETRUIRE_COOCCURENCES = "DROP TABLE IF EXISTS cooccurences"
DETRUIRE_MOTS = "DROP TABLE IF EXISTS mots"


class Dao:
    __detruire = [
        DETRUIRE_COOCCURENCES,
        DETRUIRE_MOTS
    ]
    __creer = [
        CREER_COOCCURENCES,
        CREER_MOTS
    ]

    def __init__(self):
        # self.curseur = None
        # self.connexion = None
        self.chemin = CHEMIN_BD

    def __enter__(self):
        self.connecter()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.deconnecter()
        if isinstance(exc_value, Exception):
            trace = traceback.format_exception(exc_type, exc_value, exc_tb)
            print(''.join(trace))
            return False
        return True

    def connecter(self):
        self.connexion = sqlite3.connect(self.chemin)
        self.curseur = self.connexion.cursor()
        self.curseur.execute(FK_ON)

    def deconnecter(self):
        self.curseur.close()
        self.connexion.close()

    def creer_bd(self):
        for i in Dao.__detruire:
            self.curseur.execute(i)

        for i in Dao.__creer:
            self.curseur.execute(i)

        self.curseur.execute(FK_ON)

    def ajouter_mots(self, mots: list):

        self.curseur.executemany(INSERT_MOT, mots)
        self.connexion.commit()

    def select_mots(self):
        return self.curseur.execute(SELECT_MOTS).fetchall()

    def select_id(self, mot):
        self.curseur.execute(SELECT_ID, (mot,))
        return self.curseur.fetchone()

    def select_cooccurences(self, fenetre):
        self.curseur.execute(SELECT_COOCCURENCES, (fenetre,))
        return self.curseur.fetchall()

    def ajouter_cooccurences(self, cooccurences):
        self.curseur.executemany(INSERT_COOCCURENCES, cooccurences)
        self.connexion.commit()

    def count_mots(self):
        return self.curseur.execute(COUNT_MOTS).fetchone()
