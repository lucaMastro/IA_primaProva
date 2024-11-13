from trees.binaryTree import BinaryTree
from trees.binaryTree import BinaryNode
from dictBinaryTree import DictBinaryTree
import random


class DictAVL(DictBinaryTree):
    def __init__(self):
        self.tree = BinaryTree()  # Node's info now is a triple [key,value,height]

    def height(self, node):
        """Restituisce l'altezza del sottoalbero che ha come radice node.
        Ovvero il numero di livelli di discendenza di quel nodo."""
        if node == None:
            return -1  # aiuta a calcolare il balance factor
        return node.info[2]

    def setHeight(self, node, h):
        """Metodo per settare l'altezza del nodo node al valore h."""
        if node != None:
            node.info[2] = h

    def balanceFactor(self, node):
        """Permette di calcolare il fattore di bilanciamento del nodo node."""
        if node == None:
            return 0
        return self.height(node.leftSon) - self.height(node.rightSon)

    def updateHeight(self, node):
        """Permette di aggiornare l'altezza del nodo node al valore uguale a:
        massima altezza tra le altezza dei due figli, a cui deve essere aggiunto 1."""
        if node != None:
            self.setHeight(node, max(self.height(node.leftSon), self.height(node.rightSon)) + 1)

    # Balancing

    def rightRotation(self, node):
        leftSon = node.leftSon
        node.info, leftSon.info = leftSon.info, node.info

        rtree = self.tree.cutRight(node)
        ltree = self.tree.cutLeft(node)
        ltree_l = ltree.cutLeft(leftSon)  # leftSon è la radice dell'albero ltree
        ltree_r = ltree.cutRight(leftSon)

        ltree.insertAsRightSubTree(ltree.root, rtree)
        ltree.insertAsLeftSubTree(ltree.root, ltree_r)
        self.tree.insertAsRightSubTree(node, ltree)
        self.tree.insertAsLeftSubTree(node, ltree_l)

        self.updateHeight(node.rightSon)
        self.updateHeight(node)

    def leftRotation(self, node):
        rightSon = node.rightSon
        node.info, rightSon.info = rightSon.info, node.info

        rtree = self.tree.cutRight(node)
        ltree = self.tree.cutLeft(node)
        rtree_l = rtree.cutLeft(rightSon)
        rtree_r = rtree.cutRight(rightSon)

        rtree.insertAsLeftSubTree(rtree.root, ltree)
        rtree.insertAsRightSubTree(rtree.root, rtree_l)
        self.tree.insertAsLeftSubTree(node, rtree)
        self.tree.insertAsRightSubTree(node, rtree_r)

        self.updateHeight(node.leftSon)
        self.updateHeight(node)

    def rotate(self, node):
        """Partendo dal nodo node, riesce a capire quale e' il tipo
        di rotazione da effettuare in base al fattore di bilanciamento
        del nodo e de suoi figli."""
        balFact = self.balanceFactor(node)
        if balFact >= 2:  # altezza figlio sinistro di node e' piu' grande di 2 rispetto al figlio destro
            if self.balanceFactor(node.leftSon) >= 0:  # sbilanciamento SS
                self.rightRotation(node)
            else:  # sbilanciamento SD
                self.leftRotation(node.leftSon)
                self.rightRotation(node)
        elif balFact <= -2:  # altezza figlio destro di node e' piu' grande di 2 rispetto al figlio sinistro
            if self.balanceFactor(node.rightSon) <= 0:  # sbilanciamento DD
                self.leftRotation(node)
            else:  # sbilanciamento DS
                self.rightRotation(node.rightSon)
                self.leftRotation(node)

                # INSERTION: quite the same as for dictBinaryTree. We have only to add the ability to manage nodes' height.

    def balInsert(self, newNode):
        curr = newNode.father
        while curr != None:
            if abs(self.balanceFactor(curr)) >= 2:
                break  # stop the height update at the first unbalanced predecessor.
            else:
                self.updateHeight(curr)
                curr = curr.father
        if curr != None:
            self.rotate(curr)

    def insert(self, key, value):
        newt = BinaryTree(BinaryNode([key, value, 0]))  # Primo cambiamento e' tripletta al posto della coppia key value

        if self.tree.root == None:
            self.tree.root = newt.root
        else:
            curr = self.tree.root
            pred = None
            while curr != None:
                pred = curr
                if key <= self.key(curr):
                    curr = curr.leftSon
                else:
                    curr = curr.rightSon

            if key <= self.key(pred):
                self.tree.insertAsLeftSubTree(pred, newt)
            else:
                self.tree.insertAsRightSubTree(pred, newt)
            self.balInsert(newt.root)  # secondo cambiamento e' la chiamata del metodo per bilanciare l'albero

            # DELETION: quite the same as for dictBinaryTree. We have only to add the ability to manage nodes' height.

    def balDelete(self, removedNode):
        curr = removedNode.father
        while curr != None:  # more than one may need to be rebalanced
            if abs(self.balanceFactor(curr)) == 2:
                self.rotate(curr)
            else:
                self.updateHeight(curr)
            curr = curr.father

    def cutOneSonNode(self, node):  # contrai un nodo con un singolo figlio
        son = None
        if node.leftSon != None:
            son = node.leftSon
        elif node.rightSon != None:
            son = node.rightSon  # ho cercato l'unico figlio e l'ho solvato in son

        if son == None:
            self.tree.cut(node)  # is a leaf
        else:
            node.info, son.info = son.info, node.info  # swap info

            nt = self.tree.cut(son)  # ora in son ci sono le info del nodo da tagliare

            self.tree.insertAsLeftSubTree(node, nt.cut(son.leftSon))
            self.tree.insertAsRightSubTree(node, nt.cut(son.rightSon))

        self.balDelete(node)  # This is the only change

    def delete(self, key):
        toRemove = self.searchNode(key)
        if toRemove != None:
            if toRemove.leftSon == None or toRemove.rightSon == None:
                self.cutOneSonNode(toRemove)
            else:
                maxLeft = self.maxKeySon(toRemove.leftSon)
                toRemove.info, maxLeft.info = maxLeft.info, toRemove.info
                # Avendo effettuato lo swap di tutto il campo info, si sono scambiate
                # anche le altezze dei nodi che invece dovevano rimanere uguali a prima
                # per tale motivo con queste tre righe di codice si ripristinano le
                # corrette altezze
                th = self.height(toRemove)
                self.setHeight(toRemove, self.height(maxLeft))
                self.setHeight(maxLeft, th)

                self.cutOneSonNode(maxLeft)

    # --------------------------------------------------------------------------------
    # estensione:


    def balConcatenation(self):
        """permette di bilanciare l'albero ottenuto da una concatenazione"""
        # bilancio il sottoAlbero sinistro della radice:
        curr = self.minKeySon(self.tree.root)
        self.balTreeInsert(curr)

        # bilancio quello destro:
        curr = self.maxKeySon(self.tree.root)
        self.balTreeInsert(curr)

    def balTreeInsert(self, node):
        """bilancia un ramo di un albero a partire da un certo nodo e risalendo verso la radice"""
        self.rotate(node)  # la prima cosa da fare è ruotare il nodo se sbilanciato

        curr = node.father
        rotazioni = True
        # il while più interno si blocca al primo nodo(dal basso) che è sbilanciato.
        # Ma se inserisco un albero, il risultato potrebbe essere sbilanciato in più nodi,
        # perciò controllo anche quelli più in alto col while più esterno
        while rotazioni:
            while curr != None:
                if abs(self.balanceFactor(curr)) >= 2:
                    break  # stop the height update at the first unbalanced predecessor.
                else:
                    self.updateHeight(curr)
                    curr = curr.father
            if curr != None:
                self.rotate(curr)
                curr = node
            else:
                break

    def concatenate(self, otherTree):
        """concatena due alberi AVL. il risultato è ancora un AVL."""

        radice1 = self.tree.root
        if radice1.info[2] == 0:  # è un albero composto solo dalla radice
            otherTree.insert(radice1.info[0], radice1.info[1])
            return otherTree

        radice2 = otherTree.tree.root
        if radice2.info[2] == 0:
            self.insert(radice2.info[0], radice2.info[1])
            return self

        if radice1.info[0] < radice2.info[0]:  # self è l'albero con tutte le chiavi minori

            maxNode = self.maxKeySon(radice1)

            newt = DictAVL()  # creo un nuovo AVL.....
            newt.insert(maxNode.info[0], maxNode.info[1])  # .....con radice il nodo staccato in precedenza..
            self.cutOneSonNode(maxNode)  # stacco la chiave con valore massimo dell'albero più piccolo

            # ora inserisco i sottoalberi:
            # NOTA: insertAsRightSubTree e insertAsLeftSubTree non eseguono rotazioni dopo l'inserimento.
            newt.tree.insertAsRightSubTree(newt.tree.root,
                                           otherTree.tree)  # come sottoalbero destro metto quello con chiavi più grandi
            newt.tree.insertAsLeftSubTree(newt.tree.root,
                                          self.tree)  # come sottoalb sinistro metto quello con chiavi più piccole
            newt.updateHeight(newt.tree.root)

            # newt adesso è un albero binario composto dalla concatenazione di self e otherTree ma probabilmente non è bilanciato
            if abs(newt.balanceFactor(newt.tree.root)) < 2:
                return newt  # è bilanciato: fine

            newt.rotate(
                newt.tree.root)  # scegliere di bilanciare la radice prima di tutto impedisce che la funzione successiva risalga tutto l'albero una volta in più.
            newt.balConcatenation()

            return newt

        else:  # otherTree è il mio albero minore, caso opposto

            maxNode = otherTree.maxKeySon(radice2)

            newt = DictAVL()
            newt.insert(maxNode.info[0], maxNode.info[1])
            otherTree.cutOneSonNode(maxNode)

            newt.tree.insertAsRightSubTree(newt.tree.root, self.tree)
            newt.tree.insertAsLeftSubTree(newt.tree.root, otherTree.tree)
            newt.updateHeight(newt.tree.root)

            if abs(newt.balanceFactor(newt.tree.root)) < 2:
                return newt
            newt.rotate(newt.tree.root)
            newt.balConcatenation()
            return newt
