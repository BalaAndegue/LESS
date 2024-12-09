import numpy as np

def lex_min(vector, field_size):
    """
    Calcule le minimum lexicographique d'un vecteur modulo un champ fini.

    :param vector: Vecteur d'entrée.
    :param field_size: Taille du champ fini.
    :return: Vecteur sous forme lexicographique minimale.
    """
    # Calculer toutes les versions possibles avec les multiplicateurs du champ fini
    lex_versions = [np.mod(vector * coef, field_size) for coef in range(1, field_size)]
    # Retourner la version ayant le minimum lexicographique
    return min(lex_versions, key=lambda x: tuple(x))


def lex_sort_columns(matrix):
    """
    Trie les colonnes d'une matrice selon leur ordre lexicographique.

    :param matrix: Matrice d'entrée.
    :return: Matrice avec colonnes triées.
    """
    columns = [tuple(matrix[:, j]) for j in range(matrix.shape[1])]
    sorted_columns = sorted(columns)
    return np.array(sorted_columns).T


def rref_p(matrix, field_size):
    """
    Réduit une matrice à sa forme échelonnée réduite (RREF) et identifie les pivots.

    :param matrix: Matrice d'entrée.
    :param field_size: Taille du champ fini.
    :return: Matrice RREF et liste des colonnes pivot.
    """
    rref_matrix = matrix.copy()
    nrows, ncols = rref_matrix.shape
    is_pivot = [False] * ncols
    row = 0

    for col in range(ncols):
        if row >= nrows:
            break
        # Trouver une ligne avec un pivot non nul dans cette colonne
        pivot_row = row
        while pivot_row < nrows and rref_matrix[pivot_row, col] == 0:
            pivot_row += 1
        if pivot_row == nrows:
            continue
        
        # Échanger les lignes pour placer le pivot en haut
        rref_matrix[[row, pivot_row]] = rref_matrix[[pivot_row, row]]
        
        # Normaliser le pivot
        pivot = int(rref_matrix[row, col])  # Conversion explicite
        inverse_pivot = pow(pivot, -1, field_size)  # Inverse modulaire
        rref_matrix[row] = (rref_matrix[row] * inverse_pivot) % field_size
        
        # Éliminer les autres valeurs dans cette colonne
        for r in range(nrows):
            if r != row and rref_matrix[r, col] != 0:
                factor = int(rref_matrix[r, col])  # Conversion explicite
                rref_matrix[r] = (rref_matrix[r] - factor * rref_matrix[row]) % field_size
        
        is_pivot[col] = True
        row += 1

    return rref_matrix, is_pivot


def prepare_digest_input(G, Q, field_size):
    """
    Prépare les entrées pour le digest cryptographique.

    :param G: Matrice génératrice.
    :param Q: Matrice monomiale.
    :param field_size: Taille du champ fini.
    :return: V, matrice des colonnes non pivotées triées lexicographiquement, et Q mis à jour.
    """
    # Multiplier la matrice G par la matrice monomiale Q
    GQ = np.mod(np.dot(G, Q), field_size)
    # Réduire à la forme RREF et obtenir les informations sur les pivots
    G_rref, is_pivot = rref_p(GQ, field_size)
    
    # Initialiser la matrice V et la matrice monomiale mise à jour
    V = []
    Q_updated = np.zeros_like(Q)
    pivot_index = 0
    non_pivot_index = G.shape[0]
    
    for col in range(GQ.shape[1]):
        column = G_rref[:, col]
        if not is_pivot[col]:
            # Ajouter les colonnes non pivotées après transformation lexicographique
            V.append(lex_min(column, field_size))
            Q_updated[:, non_pivot_index] = Q[:, col]
            non_pivot_index += 1
        else:
            Q_updated[:, pivot_index] = Q[:, col]
            pivot_index += 1
    
    # Trier les colonnes de V lexicographiquement
    V = np.array(V).T
    V = lex_sort_columns(V)
    
    return V, Q_updated


# Exemple d'utilisation :
field_size = 7  # Taille du champ fini
G = np.array([[1, 2, 3, 0], [0, 1, 4, 5], [1, 0, 2, 3]])  # Matrice génératrice
Q = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])  # Matrice monomiale

V, Q_updated = prepare_digest_input(G, Q, field_size)

print("Matrice V :")
print(V)
print("\nMatrice Q mise à jour :")
print(Q_updated)