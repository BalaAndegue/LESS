import numpy as np

def csprng_to_monomial_matrix(seed, n, q):
    """
    Génère une matrice monomiale Q (permutation + coefficients) à partir d'une graine.

    :param seed: Graine utilisée pour initialiser le générateur aléatoire.
    :param n: Dimension de la matrice Q (taille n x n).
    :param q: Taille du champ fini Fq.
    :return: Une matrice monomiale Q représentée par deux listes Q.π (permutation) et Q.u (coefficients).
    """
    # Initialisation du générateur aléatoire avec la graine donnée
    np.random.seed(seed)
    
    # Génération de la permutation (Q.π)
    permutation = np.random.permutation(n)
    
    # Génération des coefficients multiplicatifs (Q.u) dans [1, q-1]
    coefficients = np.random.randint(1, q, size=n)
    
    # Création de la matrice monomiale Q
    Q = np.zeros((n, n), dtype=int)
    for i in range(n):
        Q[i, permutation[i]] = coefficients[i]  # Placer le coefficient au bon endroit
    
    return Q


# Exemple d'utilisation :
seed = 42  # Une graine fixe pour la génération
n = 4  # Dimension de la matrice (4x4)
q = 7  # Taille du champ fini Fq
Q = csprng_to_monomial_matrix(seed, n, q)

print("Matrice monomiale Q :")
print(Q)