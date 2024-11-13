# Prima prova Ingegneria degli Algoritmi: Concatenazione di due AVL

La funzione che implementa la concatenazione � definita all'interno del modulo
`dictionaryAVL`, nella classe `DictAVL`.

L'algoritmo presentato si basa sulla seguente osservazione: chiamiamo `A`
l'albero con tutte le chiavi minori di ogni chiave dell'altro e `B` quello con
chiavi tutte maggiori di ogni chiave dell'altro. Sappiamo per ipotesi che la
chiave massima di `A` (che chiameremo `keyMax`) � certamente minore della chiave
minima di `B`. Si pu� allora pensare di utilizzare `keyMax` come radice di un
nuovo albero avente come sotto albero sinistro l'albero `A` (senza il nodo
`keyMax`), e come sotto albero destro l'albero `B`. In questo modo la propriet�
di ricerca � sicuramente rispettata; si tratta quindi solo di bilanciare il
nuovo albero.

Per realizzare quest'idea, ho pensato di usare queste operazioni: si invidua il
nodo `keyMax` in `A` e si inseriscono le sue informazioni in un nuovo albero
vuoto (in modo che esse saranno le informazioni della radice). Si stacca
`keyMax` dall'albero `A` (si noti che `keyMax` pu� avere al massimo un figlio
sinistro) e l'AVL viene automaticamente ribilanciato. In seguito si procede
impostando l'albero `A` come sottoalbero sinistro, e l'albero `B` come
sottoalbero destro della radice `keyMax`.

Per questo motivo, se la concatenazione avviene in questo modo, l'unico nodo che
potrebbe essere sbilanciato � la radice: sappiamo infatti che l'albero `A`
ritorna AVL subito dopo l'eliminazione del nodo `keyMax`, `B` invece � sempre
stato bilanciato; allora ogni nodo di `A` e ogni nodo di `B` � bilanciato.

Effettuata l'unione, bisogna quindi bilanciare, se necessario, la radice del
nuovo albero. La rotazione alla radice potrebbe per� sbilanciare altri nodi,
quindi interviene una nuova funzione che rimedia a questo: `balConcatenation`
(nota:bilanciare subito la radice significa evitare che la funzione
`balTreeInsert`, richiamata in `balConcatenation`, risalga l'albero una volta in
pi�).

L'idea alla base di questa funzione � di bilanciare uno per volta i due
sottoalberi della radice del nuovo albero partendo dal nodo minimo e dal nodo
massimo. Al termine di questa operazione il nuovo albero sar� un albero di
ricerca bilanciato.

NB: affinch� la funzione `rotate` funzioni bene anche per questo problema, ho
dovuto modificarla:

- riga 75:

```python
# before change
if balFact == 2:
```

```python
# after change
if balFact >= 2:
```

- riga 81:

```python
# before change
if balFact == -2:
```

```python
# before change
if balFact <= -2:
```

infatti in questo problema � possibile avere fattori di bilanciamento `a` tali
che $|a| > 2$.

L'algoritmo distingue due casi, perfettamente simmetrici, dipendenti dal
confronto tra i due alberi iniziali (infatti la chiave `keyMax` si deve
ricercare nell'albero `A`, definito come l'albero con tutte le chiavi minori
della chiave minima dell'altro). Proprio a causa della simmetria, l'analisi dei
tempi di esecuzione � presentata per un solo caso.

# Analisi dei tempi di esecuzione

## Caso peggiore

Chiamiamo `n` il numero di nodi dell'albero `A`, e `m` il numero di nodi
dell'albero `B`. Si avr� quindi $hA = O(logn)$ e $ hB = O(logm)$.

La prima operazione � quella di ricercare `keyMax` in A, che avviene in tempo
`O(hA)`. La creazione di un AVL vuoto avviene in tempo costante `O(1)`, cos�
come l'inserimento di `keyMax` come radice: infatti viene sfruttata la funzione
`insert`, che ha tempo di esecuzione logaritmico nei nodi dell'albero, ma, nel
nostro caso, � un albero vuoto. Anche l'impostare i sottoalberi destri e
sinistri della radice avviene in tempo costante: si tratta di modificare i
puntatori della radice del nuovo albero e _dirigerli_ opportunamente verso le
radici di `A` e di `B`. Infine, per bilanciare la concatenazione si impiega un
tempo totale dato dal tempo impiegato per bilanciare il sottoalbero sinistro,
pi� quello necessario a bilanciare il sottoalbero destro della radice. Il nuovo
albero avr� un numero di nodi pari a $n + m$ e avr� altezza $k = O(log(n+m))$;
il sottoalbero sinistro `A` avr� `n - 1` nodi e altezza $hA = O(log(n))$, quello
destro, `B`, avr� `m` nodi e altezza $hB = O(log(m))$. Essendo `k` l'altezza del
nuovo albero, si avr�: $k = max{hA, hB} + 1$.

Assumiamo che il sottoalbero pi� alto sia il sottoalbero sinistro. Per
bilanciarlo allora si deve ricercare il minimo, impiegando quindi un `O(k)` e
chiamare la funzione `balTreeInsert` su questo nodo. La funzione risalir� il
sottoalbero dal minimo fino al primo nodo sbilanciato, eseguir� un'opportuna
rotazione (tempo costante) e ricomincerer� dal basso, arrivando alla radice solo
nell'ultimo passo. Il tempo di esecuzione di queste continue scalate dal minimo
alla radice si pu� quindi maggiorare con: $c \cdot k$ dove la costante `c`
identifica il numero di volte in cui si risale l'albero. In totale, bilanciare
un sottoalbero coster� al massimo `O(k)`. Si noti che non si pu� avere `O(k)`
per bilanciare anche l'altro sottoalbero perch�, se cos� fosse, la radice
sarebbe bilanciata, e quindi non sarebbe necessario eseguire questa operazione.

Per maggiorare l'analisi del tempo di esecuzione, consideriamo comunque che
l'algoritmo impieghi tempo di esecuzione pari a `O(k)` per bilanciare anche il
sottoalbero di altezza minore.

In totale, il tempo di esecuzione nel caso peggiore sar� quindi:

$$
T(hA,hB) \leq c1 \cdot hA + 2 \cdot c2 \cdot k \leq 3 \cdot c3 \cdot k \Rightarrow t(hA,hB) = O(k)
$$

dove $k = max{hA, hB}+1$.

Il tempo di esecuzione � quindi lineare nell'altezza, e cio� logaritmico nel
numero di nodi:

$$
T(n,m) \leq c1 \cdot log(n) + 2 \cdot c2 \cdot log(n+m) \leq 3 \cdot c3 \cdot log(n+m) \Rightarrow T(n,m)
\leq O(log(n+m))
$$

## Caso migliore

Il caso migliore si verifica quando uno dei due alberi ha un solo nodo: la
radice. Infatti in questo caso si tratta solo di inserire quell'elemento
nell'altro albero. Chiamiamo `A` l'albero con un solo nodo, l'altro invece sar�
`B` (di altezza `hB` ed `m` nodi); si avr� quindi:

## $$T(hA, hB) = O(hB); T(n, m) = O(log(m))$$

# Esecuzione demo, spiegazioni varie

## Funzione ausiliaria

La funzione `creaDicts` prende in input due interi e restituisce una tupla
contenente due AVL: il primo, che avr� `n` elementi, avr� la chiave massima
minore della chiave minima dell'altro, che invece avr� `m` nodi. Le chiavi sono
lettere maiuscole, ed hanno come valore la posizione che occupano nell'alfabeto
(da 1 a 26). `keyMax`, generato casualmente, � la posizione che la chiave
massima dell'albero con chiavi minori occupa nell'alfabero. Il range varia tra 0
e 24 e non tra 0 e 25, in modo da garantire l'esistenza di almeno un nodo anche
nel secondo sottoalbero. Si inseriscono infine `n` o `m` elementi nei relativi
alberi scegliendo gli elementi a caso tra quelli opportunamente selezionati.
Tempo di esecuzione:

$$T(n,m) = O(n \cdot log(n) + m \cdot log(m))$$

## Demo della concatenazione

Si creano due alberi di dimensioni variabili tra 1,20 (il valore massimo pu�
essere cambiato in base al numero di nodi che, al massimo, si vuole concedere a
ciascun albero). Si ricorda che `n` � il numero di nodi dell'albero che avr� la
chiave massima minore della chiave minima dell'altro, che invece avr� `m`
elementi. Dopo la stampa dei due alberi, si procede alla concatenazione e la si
stampa. Infine, l'`if` all'interno del ciclo permette di decidere se andare
avanti con un'altra concatenazione o interrompere se si vuole terminare. Inoltre
permetter� di verificare l'esattezza dei risultati ottenuti.

## Demo dei tempi di esecuzione

In questa demo si verificano i tempi di esecuzione di ogni caso dell'algoritmo.
Si distinguono 3 casi fondamentali:

    - quando uno dei due alberi passati in input ha solo un nodo;
    - quando dopo aver creato il nuovo AVL e impostato i sottoalberi
    destri e sinistri, la sua radice � gi� bilanciata;
    - quando si ha bisogno di ribilanciare l'albero.

Nell'analisi teorica dei tempi di esecuzione ho definito il primo caso come
quello migliore, mentre pu� capitare che in pratica esso impieghi un tempo
maggiore del secondo caso. Questo � giustificabile dal fatto che, con
particolari input, si pu� aver bisogno di maggiori rotazioni (tempo costante
nell'analisi teorica, e quindi trascurate) per bilanciare l'AVL ottenuto nel
primo caso rispetto al numero di rotazioni necessarie a bilanciare quello del
secondo caso.

Come mostrato dalla demo, il tempo di esecuzione medio di ogni concatenazione �
circa pari a 2 ms.
