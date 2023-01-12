import numpy as np


class Training:
    def __init__(self, fichier="textes/DonQuichotteUTF8.txt", encodage="utf-8", nb_fenetre=5):
        self.fichier = fichier
        self.encodage = encodage
        self.nb_fenetre = nb_fenetre
        self.tous_les_mots = []
        self.mots_uniques = {}
        self.matrice = None
        self.ouvrir_fichier()
        self.compter_synonyme()

    def ouvrir_fichier(self):

        counter = 0
        with open(self.fichier, encoding=self.encodage) as f:
            for line in f:
                for word in line.replace('.', ' ').replace(',', ' ').replace('?', ' ').replace('!', ' ').replace('_',
                                                                                                                 ' ').replace(
                    '»', ' ').replace('«', ' ').replace('(', ' ').replace(')', ' ').replace(';', ' ').replace(':',
                                                                                                              ' ').split():
                    self.tous_les_mots.append(word.lower())
                    if word.lower() not in self.mots_uniques:
                        self.mots_uniques[word.lower()] = counter
                        counter += 1
        self.matrice = self.create_matrix()

    def create_matrix(self):
        taille = len(self.mots_uniques)
        return np.zeros((taille, taille))

    def compter_synonyme(self):
        voisin = int((self.nb_fenetre - 1) / 2)
        for i in range(len(self.tous_les_mots)):
            for j in range(i - voisin, i + voisin + 1):
                if 0 <= j < len(self.tous_les_mots) and j != i:
                    index_y = self.mots_uniques[self.tous_les_mots[j]]
                    index_x = self.mots_uniques[self.tous_les_mots[i]]
                    self.matrice[index_x, index_y] += 1
