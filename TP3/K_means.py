import random

import numpy as np

import prediction


def compute_euclidean(x, y):
    return np.sqrt(np.sum((x - y) ** 2))


class KMeans:
    def __init__(self, taille, nb_centroides, matrice, nb_mots, vocabulaire):
        self.new_k_group = None
        self.nb_mots = nb_mots
        self.old_k_group = None
        self.centroides = None
        self.matrice = matrice
        self.taille_fen = taille
        self.nb_centroides = nb_centroides
        self.vocabulaire = vocabulaire
        # self.initialiser_centroides()
        self.k_means_plus_plus()

        # while not self.calcul_proximite_centroide():
        #     print("recalcule")

    def k_means_plus_plus(self):
        index = int(np.random.uniform(0, len(self.matrice)))
        self.centroides = [self.matrice[index]]
        while len(self.centroides) != self.nb_centroides:
            liste_distance = []
            for i in self.matrice:
                temp = []
                for j in self.centroides:
                    temp.append((np.linalg.norm(i - j)) ** 2)
                # liste_distance.append(min(temp))
                liste_distance.append(sum(temp))

            # probabilite = liste_distance / (np.sum(liste_distance))
            probabilite = np.sum(liste_distance)-liste_distance
            probabilite /= np.sum(probabilite)
            choix = np.random.choice(liste_distance, p=probabilite)
            self.centroides.append(self.matrice[np.where(np.isclose(liste_distance, choix))[0][0]])

        self.calcul_proximite_centroide()

        # print(np.random.choice(arr, p=)
        # compteur = 1
        # while compteur != self.nb_centroides:

    def initialiser_centroides(self):

        self.indice_centroides = np.random.choice(self.matrice.shape[0], size=self.nb_centroides, replace=False)
        self.centroides = self.matrice[self.indice_centroides, :]
        self.calcul_proximite_centroide()

    def calcul_proximite_centroide(self):

        self.new_k_group = []
        for i in range(self.nb_centroides):
            self.new_k_group.append({})

        for idx in range(self.matrice.shape[0]):

            ligne = self.matrice[idx]
            temp = []
            for j in range(self.nb_centroides):
                temp.append(prediction.Prediction.ls(ligne, self.centroides[j]))
            #
            self.new_k_group[temp.index(min(temp))][idx] = ligne

        self.calcul_moyenne_centroides()

    def calcul_moyenne_centroides(self):

        for i in range(len(self.new_k_group)):
            liste_centroide = self.new_k_group[i]

            self.centroides[i] = np.mean(np.array(list(liste_centroide.values())), axis=0)

        self.verif_stabilite()

    def affichage(self):
        pass

    def verif_stabilite(self):
        # print(f"vieux : {self.old_k_group}")
        # print(f"nouveau : {self.new_k_group}")
        compteur = 0

        if self.old_k_group is None:
            print("c'est le premier")
            self.old_k_group = self.new_k_group
            self.calcul_proximite_centroide()
        else:
            for i in range(len(self.new_k_group)):
                arr1 = np.array(list(self.new_k_group[i].keys()))
                arr2 = np.array(list(self.old_k_group[i].keys()))
                if not np.array_equal(arr1, arr2):
                    print(f"difference dans le cluster {i}")
                    compteur += 1

            if compteur > 0:
                print("pas pareil")
                self.old_k_group = self.new_k_group
                self.calcul_proximite_centroide()
            else:
                print("pareil")
                self.afficher_n_mots()

        # if self.old_k_group is None:
        #
        #
        #     # self.calcul_proximite_centroide()
        #     return False
        # else:
        #     ##print(self.old_k_group)
        #     old_group = np.array(self.old_k_group)
        #     new_group = np.array(self.new_k_group)
        #     #a = np.sum(np.not_equal(old_group,new_group))
        #     a = 0
        #     for i in range(len(self.old_k_group)):
        #         for j in range(i):
        #             for k in range(j):
        #                 try:
        #                     if self.old_k_group[i][j][k] != self.new_k_group[i][j][k]:
        #                         a += 1
        #                 except:
        #                     pass
        #
        #             #a += np.sum(np.not_equal(self.old_k_group[i][j], self.new_k_group[i][j]))
        #
        #     #a = np.sum(old_group.(new_group))
        #     print(a)
        #     if a == 0:
        #         print("pareil")
        #         return True
        #     else:
        #         print("pas pareil")
        #         self.old_k_group = self.new_k_group
        #         # self.calcul_proximite_centroide()
        #         return False

    def afficher_n_mots(self):

        for i in range(len(self.new_k_group)):
            print(f"pour le cluster {i} : ")
            temp = {}
            for idx, values in self.new_k_group[i].items():
                temp[idx] = np.linalg.norm(values - self.centroides[i])
                # temp.append(np.linalg.norm(j-self.centroides[i]))

            for idx, val in list(sorted(temp.items(), key=lambda item: item[1]))[:self.nb_mots]:
                print(f"{list(self.vocabulaire.keys())[list(self.vocabulaire.values()).index(idx)]} --> {val}")
            # print(np.argsort(temp)[:self.nb_mots])
