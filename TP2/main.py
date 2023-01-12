import argparse
from time import time
from traceback import print_exc

from numpy import array

from dao import Dao
from entrainement import Entrainement
from prediction import Prediction

QUITTER = 'q'

MESS = f'''
Entrez un mot, le nombre de synonymes que vous voulez et la méthode de calcul,
i.e. produit scalaire: 0, least-squares: 1, city-block: 2

Tapez "{QUITTER}" pour quitter.

'''

# argparse
parser = argparse.ArgumentParser()

subparser = parser.add_subparsers(dest='options')
entrainement = subparser.add_parser('e')
recherche = subparser.add_parser('r')
subparser.add_parser('b')

entrainement.add_argument('-t', type=int, required=True)
entrainement.add_argument('--enc', type=str, required=True)
entrainement.add_argument('--chemin', type=str, required=True)

recherche.add_argument('-t', type=int, required=True)


def imprimer(scores: list) -> None:
    print()
    for mot, score in scores:
        print(f'{mot} --> {score}')


def demander(d: dict, m: array, verbose: bool) -> None:
    reponse = input(MESS)
    while reponse != QUITTER:
        mot, n, fonc = reponse.split()
        t = time()
        scores = Prediction.predire(d, m, mot, int(n), int(fonc))
        if verbose:
            print(f"Prédiction en {time() - t} secondes.")
        imprimer(scores)
        reponse = input(MESS)


def main() -> int:
    try:
        # argparse
        opts = parser.parse_args()
        with Dao() as dao:
            if opts.options == 'b':
                # regenerer bd
                dao.creer_bd()
            else:

                e = Entrainement(opts.t, dao)
                e.get_ancien_dict()
                e.init_vocabulaire()

                if opts.options == 'e':
                    # entrainer
                    e.entrainer(opts.enc, opts.chemin)
                elif opts.options == 'r':
                    # rechercher
                    e.construire_matrice()
                    print(e.matrice)
                    demander(e.vocabulaire, e.matrice, False)
    except EOFError:
        print_exc()
        return 1
    return 0


if __name__ == '__main__':
    quit(main())
