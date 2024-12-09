import numpy as np
def compress_rref(G, k, n, q):
    """
    Compresse une matrice génératrice en RREF en réduisant les données nécessaires.

    :param G: Matrice en RREF (k x n).
    :param k: Nombre de lignes de la matrice.
    :param n: Nombre de colonnes de la matrice.
    :param q: Taille du champ fini Fq.
    :return: Une représentation compressée de la matrice.
    """
    # Identifier les colonnes pivot
    pivots = []
    for j in range(n):
        if any(G[i, j] == 1 and all(G[x, j] == 0 for x in range(k) if x != i) for i in range(k)):
            pivots.append(1)  # 1 si la colonne est un pivot
        else:
            pivots.append(0)  # 0 sinon

    # Extraire les coefficients des colonnes non pivot
    non_pivot_values = []
    for j in range(n):
        if pivots[j] == 0:  # Si la colonne n'est pas un pivot
            for i in range(k):
                non_pivot_values.append(G[i, j])  # Ajouter les coefficients

    return pivots, non_pivot_values

#exemple de matrice en RREF

G = np.array([
    [1,0,0,6,3],
    [0,1,0,4,2],
    [0,0,1,5,6]
])

k,n,q = 3,5,7 #dimension et taille du champ fini

#compression de la matrice
pivots , non_pivots = compress_rref(G,k,n,q)

print("colonne pivot :", pivots)
print("valeurs non pivotes :", non_pivots)

def expand_rref(pivots, non_pivot_values, k, n, q):
    """
    Reconstruit une matrice génératrice en RREF à partir de données compressées.

    :param pivots: Liste indiquant les colonnes pivot.
    :param non_pivot_values: Coefficients des colonnes non pivotées.
    :param k: Nombre de lignes de la matrice.
    :param n: Nombre de colonnes de la matrice.
    :param q: Taille du champ fini Fq.
    :return: Matrice reconstruite (k x n).
    """
    G = np.zeros((k, n), dtype=int)
    non_pivot_index = 0

    for j in range(n):
        if pivots[j] == 1:  # Si la colonne est un pivot
            # Remplir avec une colonne de la matrice identité
            for i in range(k):
                G[i, j] = 1 if i == pivots[:j].count(1) else 0
        else:
            # Remplir avec les valeurs compressées
            for i in range(k):
                G[i, j] = non_pivot_values[non_pivot_index]
                non_pivot_index += 1

    return G
G_reconstructed = expand_rref(pivots, non_pivots,k,n,q)

print("la matrice reconstruite est :\n",G_reconstructed)