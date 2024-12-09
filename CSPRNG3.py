import numpy as np

def csprng_expand_to_rref(seed, k, n, q):
    """
    Génère une matrice génératrice sous forme réduite (RREF) à partir d'une graine.

    :param seed: La graine utilisée pour générer la matrice.
    :param k: Nombre de lignes de la matrice (dimension du code).
    :param n: Nombre de colonnes de la matrice (longueur du code).
    :param q: Taille du champ fini Fq.
    :return: Une matrice génératrice G en RREF.
    """
    # Initialiser le générateur pseudo-aléatoire avec la graine
    np.random.seed(seed)

    # Étape 1 : Initialiser les k premières colonnes en tant qu'identité
    G = np.zeros((k, n), dtype=int)
    G[:, :k] = np.eye(k, dtype=int)

    # Étape 2 : Remplir les colonnes restantes avec des coefficients aléatoires
    for i in range(k):  # Parcourir chaque ligne
        for j in range(k, n):  # Remplir les colonnes non identitaires
            G[i, j] = np.random.randint(0, q)  # Valeurs dans [0, q-1]

    return G


# Exemple d'utilisation :
seed = 42  # Une graine fixe pour garantir la reproductibilité
k = 3  # Nombre de lignes
n = 5  # Nombre de colonnes
q = 7  # Taille du champ fini

G = csprng_expand_to_rref(seed, k, n, q)

print("Matrice génératrice G en RREF :")
print(G)