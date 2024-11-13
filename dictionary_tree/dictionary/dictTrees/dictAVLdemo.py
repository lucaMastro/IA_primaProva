"""
    File name: dictAVLdemo.py
    Author: Luca Mastrobattista
    Python Version: 3.4.3

    Questo modulo mostra esempi di esecuzione della funzione "concatenate" passando parametri generati casualmente.

"""


from dictBinaryTree import DictBinaryTree
from dictionaryAVL import DictAVL
from time import time
import random
from funzioneAusiliaria import *



if __name__ == '__main__':

    #eseguo la concatenazione su input casuali

    for i in range(50):     #il range credo basti, ma non si è costretti a vederle tutte

        n = random.randint(1, 20) #i valori finali del range possono essere cambiati in base a quanto grande si
        m = random.randint(1, 20) #vuole avere gli alberi.
        dictionaries = creaDicts(n, m)

        dictMin = dictionaries[0]
        dictMax = dictionaries[1]

        # ho creato due AVL che rispettano le condizioni richieste dall'esercizio ed hanno caratteristiche stabilite a
        # caso. li stampo:
        print("L'albero con chiavi minori (dictMin) di {} elementi è:\n".format(n))
        dictMin.tree.stampa()

        print("\nL'albero con chiavi maggiori (dictMax) di {} elementi è:\n".format(m))
        dictMax.tree.stampa()

        # ora concateno:

        newt = dictMax.concatenate(dictMin)
        print("\nL'albero risultante dalla concatenazione di dicMin e dictMax è:\n")
        newt.tree.stampa()

        if i < 49: #se i == 49, abbiamo comunque finito!!
            comm=input("\nPremere un tasto per continuare, 0 per interrompere.\n")
            if comm=='0':
                break

        print('\n\nNuova concatenazione.\n')

