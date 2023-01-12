import numpy as np


class Prediction:
    def __init__(self, mot, nb_synonymes, methode, training):
        self.mot = mot
        self.nb_synonymes = nb_synonymes
        self.training = training
        self.index_mot = self.training.mots_uniques[self.mot]
        self.methode = methode
        self.mots_stop = self.ouvrir_stop()
        self.predire()

    def predire(self):
        total = 0

        resultat = {}
        maliste = list(self.training.mots_uniques.keys())

        mon_mot = self.training.matrice[self.index_mot]

        for i in range(len(self.training.matrice[self.index_mot])):
            position_synonyme = self.training.mots_uniques[maliste[i]]

            my_array = self.training.matrice[position_synonyme]
            if self.methode == '0':
                total = np.sum((mon_mot * my_array))
            elif self.methode == '1':
                total = np.sum((mon_mot - my_array) ** 2)
            elif self.methode == '2':
                total = np.sum(abs(mon_mot - my_array))

            if maliste[i] not in self.mots_stop and maliste[i] != self.mot:
                resultat[maliste[i]] = total

        sort_orders = None

        if self.methode == '0':
            sort_orders = sorted(resultat.items(), key=lambda x: x[1], reverse=True)

        elif self.methode == '1' or self.methode == '2':
            sort_orders = sorted(resultat.items(), key=lambda x: x[1])

        for i in range(int(self.nb_synonymes)):
            print(f"{sort_orders[i][0]} --> {sort_orders[i][1]}")

    def ouvrir_stop(self):
        liste_stop = []
        with open("textes/StopWords.txt", encoding="utf-8") as f:
            for line in f:
                for word in line.replace('.', ' ').replace(',', ' ').replace('?', ' ').replace('!', ' ').replace('_',
                                                                                                                 ' ').replace(
                    '»', ' ').replace('«', ' ').replace('(', ' ').replace(')', ' ').replace(';', ' ').replace(':',
                                                                                                              ' ').split():
                    liste_stop.append(word.lower())

            return dict.fromkeys(liste_stop, None)
