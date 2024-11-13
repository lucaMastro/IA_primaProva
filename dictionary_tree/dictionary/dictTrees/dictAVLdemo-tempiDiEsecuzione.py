"""
    File name: dictAVLdemo-tempiDiEsecuzione.py
    Author: Luca Mastrobattista
    Python Version: 3.4.3

    Questo modulo calcola i tempi di esecuzione della funzione "concatenate" esaminando la funzione in tutti i casi.

"""


from dictBinaryTree import DictBinaryTree
from dictionaryAVL import DictAVL
from time import time
import random
from funzioneAusiliaria import *


if __name__=='__main__':

    totalTime = 0  # tempo totale delle concatenazioni

    #CASO 1: l'albero con chiavi minori ha un solo elemento.

    end = 0
    for i in range(100):
        dictionaries = creaDicts(1, 10)

        dictMin = dictionaries[0]
        dictMax = dictionaries[1]

        start=time()
        newt= dictMin.concatenate(dictMax)
        elapsed=time()-start

        end += elapsed

    print("tempo per la concatenazione nel caso 1: %4.10f" %((end) / 100))
    totalTime += end

    #CASO 2: dopo la concatenazione, l'albero è bilanciato senza alcuna rotazione

    end=0
    for i in range(100):
        dictionaries = creaDicts(10, 10)
        dictMin = dictionaries[0]
        dictMax = dictionaries[1]

        start = time()
        newt = dictMin.concatenate(dictMax)
        elapsed = time() - start
        end += elapsed

    print("\ntempo per la concatenazione nel caso 2: %4.10f" % ((end) / 100))
    totalTime += (end)

    #CASO3: sono necessarie concatenazioni

    end = 0
    for i in range(100):
        dictionaries = creaDicts(5, 50)
        dictMin = dictionaries[0]
        dictMax = dictionaries[1]

        start = time()
        newt = dictMin.concatenate(dictMax)
        elapsed = time() - start
        end += elapsed

    print("\ntempo per la concatenazione nel caso 3: %4.10f" % (end / 100))

    totalTime += end

    print("\n\ntempo di esecuzione per 300 concatenazioni: {}".format(totalTime))
    print("tempo medio di una concatenazione: {}".format(totalTime/300))
