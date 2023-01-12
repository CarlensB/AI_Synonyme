import re
import numpy as np

REMOTS = '\w+'


class Entrainement:
    def __init__(self, tfen: int, dao) -> None:
        self.ancien_dict = {}
        self.matrice = None
        self.vocabulaire = None
        self.tfen = tfen
        self.dao = dao

    def get_ancien_dict(self):
        result = self.dao.select_cooccurences(self.tfen)
        for i in result:
            self.ancien_dict[(i[0], i[1])] = i[2]

        self.dao.select_cooccurences(5)

    # def insert_coocurences(self):
    #     self.dao.insert_coocurences(self.nouveau_dict)

    def entrainer(self, enc: str, ch: str) -> None:
        texte = self.parser(ch, enc)
        self.indexer(texte)
        self.cooccurrences(texte)

    def parser(self, ch: str, enc: str) -> list:
        with open(ch, 'r', encoding=enc) as f:
            return re.findall(REMOTS, f.read().lower())

    def init_vocabulaire(self):
        self.vocabulaire = {}

        for i in self.dao.select_mots():
            self.vocabulaire[i[1]] = i[0]

    def indexer(self, texte: list) -> None:

        liste = []
        for mot in texte:
            if mot not in self.vocabulaire:
                liste.append((mot, len(self.vocabulaire)))
                self.vocabulaire[mot] = len(self.vocabulaire)

        self.dao.ajouter_mots(liste)

    def cooccurrences(self, texte: list) -> None:

        for i in range(len(texte)):
            i_mot = self.vocabulaire[texte[i]]
            for j in range(1, self.tfen // 2 + 1):

                if i - j >= 0:
                    j_coocurence = self.vocabulaire[texte[i - j]]

                    if (i_mot, j_coocurence) not in self.ancien_dict:
                        self.ancien_dict[(i_mot, j_coocurence)] = 1
                    else:
                        self.ancien_dict[(i_mot, j_coocurence)] += 1

                if i + j < len(texte):

                    j_coocurence = self.vocabulaire[texte[i + j]]
                    if (i_mot, j_coocurence) not in self.ancien_dict:
                        self.ancien_dict[(i_mot, j_coocurence)] = 1
                    else:
                        self.ancien_dict[(i_mot, j_coocurence)] += 1

        liste_query = []

        for key, val in self.ancien_dict.items():
            id_rangee = key[0]
            id_colonne = key[1]
            liste_query.append((id_rangee, id_colonne, self.tfen, val))

        self.dao.ajouter_cooccurences(liste_query)

    def construire_matrice(self):
        taille = int(self.dao.count_mots()[0])
        self.matrice = np.zeros((taille, taille))

        for rangee, colonne, valeur in self.dao.select_cooccurences(self.tfen):
            self.matrice[rangee, colonne] = valeur
