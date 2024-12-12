import numpy as np

def seed_tree_leaves(root_seed, salt, t):
    """
    Génère les feuilles d'un arbre de graines.

    :param root_seed: Graine racine de l'arbre.
    :param salt: Sel cryptographique pour protéger contre les collisions.
    :param t: Nombre total de feuilles nécessaires.
    :return: Liste des graines générées pour chaque feuille.
    """
    # Calculer la graine en prenant le module 2**32
    seed = (int(root_seed, 16) + int(salt, 16)) % 2**32
    np.random.seed(seed)
    leaves = [np.random.randint(0, 2**31) for _ in range(t)]
    return [format(leaf, '08x') for leaf in leaves]

def seed_tree_paths(root_seed, revealed_indices, t):
    """
    Calcule les chemins à révéler pour reconstruire les graines nécessaires.

    :param root_seed: Graine racine de l'arbre.
    :param revealed_indices: Indices des feuilles à révéler.
    :param t: Nombre total de feuilles.
    :return: Liste des nœuds à révéler.
    """
    tree_depth = int(np.ceil(np.log2(t)))
    seed = int(root_seed, 16) % 2**32  # Assurer que la graine est valide
    np.random.seed(seed)
    
    # Simuler un arbre complet
    full_tree = [np.random.randint(0, 2**31) for _ in range(2**tree_depth - 1)]

    # Trouver les indices des nœuds nécessaires pour révéler les feuilles
    revealed_nodes = set()
    for idx in revealed_indices:
        node = idx + 2**(tree_depth - 1) - 1  # Calcul correct pour aller à la couche feuille
        while node > 0:
            revealed_nodes.add(node)
            node = (node - 1) // 2  # Remonter à la racine
        revealed_nodes.add(0)  # Inclure la racine
    
    return [full_tree[node] for node in sorted(revealed_nodes) if node < len(full_tree)]  # Correction pour éviter les indices hors limites

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
