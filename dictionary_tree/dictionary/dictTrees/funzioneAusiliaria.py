"""
    File name: funzioneAusiliaria.py
    Author: Luca Mastrobattista
    Python Version: 3.4.3

    Questo modulo implementa una funzione utile per l'esecuzione di entrambe le demo.

"""

import random
from dictionaryAVL import DictAVL


alfabeto = [['A', 1], ['B', 2], ['C', 3], ['D', 4], ['E', 5], ['F', 6], ['G', 7], ['H', 8], ['I', 9], ['J', 10],
                ['K', 11], ['L', 12], ['M', 13],
                ['N', 14], ['O', 15], ['P', 16], ['Q', 17], ['R', 18], ['S', 19], ['T', 20], ['U', 21], ['V', 22],
                ['W', 23], ['X', 24], ['Y', 25], ['Z', 26]]


def creaDicts(n, m):
    """crea due alberi A e B di n ed m nodi rispettivamente in modo casuale."""

    keyMax = random.randint(0, 24)

    dictMin = DictAVL()
    dictMax = DictAVL()

    for i in range(n):
        item = random.choice(alfabeto[:keyMax + 1])
        dictMin.insert(item[0], item[1])

    for j in range(m):
        item = random.choice(alfabeto[keyMax + 1:])
        dictMax.insert(item[0], item[1])

    return dictMin, dictMax