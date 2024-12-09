import numpy as np
def seed_tree_leaves(root_seed, salt, t):
    """
    Génère les feuilles d'un arbre de graines.

    :param root_seed: Graine racine de l'arbre.
    :param salt: Sel cryptographique pour protéger contre les collisions.
    :param t: Nombre total de feuilles nécessaires.
    :return: Liste des graines générées pour chaque feuille.
    """
    # Initialiser un arbre de taille suffisante
    np.random.seed(int(root_seed, 16) + int(salt, 16))
    leaves = [np.random.randint(0, 2**32-1) for _ in range(t)]
    return [format(seed, '032x') for seed in leaves]

def seed_tree_paths(root_seed, revealed_indices, t):
    """
    Calcule les chemins à révéler pour reconstruire les graines nécessaires.

    :param root_seed: Graine racine de l'arbre.
    :param revealed_indices: Indices des feuilles à révéler.
    :param t: Nombre total de feuilles.
    :return: Liste des nœuds à révéler.
    """
    tree_depth = int(np.ceil(np.log2(t)))
    np.random.seed(int(root_seed, 16))
    
    # Simuler un arbre complet
    full_tree = [np.random.randint(0, 2*32) for _ in range(2*tree_depth - 1)]
    
    # Trouver les indices des nœuds nécessaires pour révéler les feuilles
    revealed_nodes = set()
    for idx in revealed_indices:
        node = idx + len(full_tree) // 2  # Aller à la couche feuille
        while node > 0:
            revealed_nodes.add(node)
            node = (node - 1) // 2  # Remonter à la racine
        revealed_nodes.add(0)  # Inclure la racine
    
    return [full_tree[node] for node in sorted(revealed_nodes)]

def rebuild_seed_tree_leaves(revealed_nodes, t, revealed_indices):
    """
    Reconstruit les feuilles à partir des nœuds révélés.

    :param revealed_nodes: Liste des nœuds révélés.
    :param t: Nombre total de feuilles.
    :param revealed_indices: Indices des feuilles à reconstruire.
    :return: Feuilles reconstruites.
    """
    tree_depth = int(np.ceil(np.log2(t)))
    reconstructed_tree = [None] * (2**tree_depth - 1)
    
    # Reconstruire les nœuds de l'arbre
    node_idx = 0
    for node in revealed_nodes:
        reconstructed_tree[node_idx] = node
        node_idx += 1
    
    # Extraire les feuilles reconstruites
    leaves = reconstructed_tree[-t:]
    return [leaves[idx] for idx in revealed_indices]

# Paramètres
root_seed = "12345678abcdef"  # Graine racine
salt = "feedfacecafebeef"     # Sel
t = 8                         # Nombre de feuilles
revealed_indices = [0, 3, 6]  # Feuilles à révéler

# Générer les feuilles
leaves = seed_tree_leaves(root_seed, salt, t)
print("Feuilles générées :", leaves)

# Calculer les chemins nécessaires
paths = seed_tree_paths(root_seed, revealed_indices, t)
print("\nNœuds à révéler :", paths)

# Reconstruire les feuilles
reconstructed_leaves = rebuild_seed_tree_leaves(paths, t, revealed_indices)
print("\nFeuilles reconstruites :", reconstructed_leaves)