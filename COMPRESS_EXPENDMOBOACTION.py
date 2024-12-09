import numpy as np


def compress_monomial_action(Q, k, n, q):
    """
    Compresse une matrice monomiale Q en deux listes : permutation et coefficients.

    :param Q: Matrice monomiale de taille n x n.
    :param k: Nombre de lignes de la matrice utilisée pour la compression.
    :param n: Taille de la matrice Q.
    :param q: Taille du champ fini Fq.
    :return: Deux listes : π (indices de permutation) et u (coefficients multiplicatifs).
    """
    π = []  # Liste des indices de permutation
    u = []  # Liste des coefficients multiplicatifs

    # Parcourir les k premières lignes de Q pour extraire les informations
    for i in range(k):
        for j in range(n):
            if Q[i, j] != 0:  # Trouver l'entrée non nulle
                π.append(j)  # Indice de la colonne (permutation)
                u.append(Q[i, j])  # Coefficient multiplicatif
                break

    return π, u
def expand_to_monomial_action(π, u, n, q):
    """
    Reconstruit une matrice monomiale Q à partir de listes compressées.

    :param π: Liste des indices de permutation.
    :param u: Liste des coefficients multiplicatifs.
    :param n: Taille de la matrice Q.
    :param q: Taille du champ fini Fq.
    :return: Matrice monomiale Q reconstruite.
    """
    Q = np.zeros((n, n), dtype=int)  # Initialiser une matrice nulle

    # Remplir Q en utilisant π et u
    for i in range(len(π)):
        Q[i, π[i]] = u[i]

    return Q

Q = np.array([
    [6,0,0,0],
    [0,4,0,0],
    [0,0,2,0],
    [0,0,0,5]
])

k,n,q = 4,4,7 #dimension et taille du champ fini

#compression de l'action monomiale
pi , u = compress_monomial_action(Q, k,n,q)

print("indices des permutations (pi) :", pi)
print("coefficients multiplicatifs (u) :", u)

#expension reconstruction de la matrice monomiale
Q_reconstructed = expand_to_monomial_action(pi, u , n,q)
print("la matrice monomiale reconstruite est :\n", Q_reconstructed)