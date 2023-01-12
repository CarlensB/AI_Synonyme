import sys

from prediction import Prediction
from training import Training

liste_stop_words = []


# python main.py 5 utf-8 textes/GerminalUTF8.txt

def creer_training():
    nb_fenetre = int(sys.argv[1])
    encodage = sys.argv[2]
    fichier = sys.argv[3]
    return Training(fichier, encodage, nb_fenetre)


if __name__ == '__main__':
    t = None
    message = '''
Entrer un mot, le nombre de synonymes que vous voulez et la méthode de calcul,i.e. produit 
scalaire: 0, least-squares: 1, city-block: 2. 

Tapez q pour quitter.\n\n'''

    try:
        t = creer_training()
        val = input(message)
        print('')
        liste_val = [i for i in val.split()]
        prediction = Prediction(liste_val[0], liste_val[1], liste_val[2], t)
        while val != 'q':
            val = input(message)
            liste_val = [i for i in val.split()]
            prediction = Prediction(liste_val[0], liste_val[1], liste_val[2], t)

    except:
        pass

