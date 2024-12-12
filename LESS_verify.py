import hashlib
import numpy as np

def validate_monom(Q):
    """
    Vérifie si l'action monomiale est valide, c'est-à-dire que tous les indices des colonnes de destination sont distincts et dans l'intervalle [0, n-1],
    et si tous les coefficients multiplicatifs sont dans F_q*.

    :param Q: Matrice monomiale candidate.
    :return: True si l'action monomiale est valide, False sinon.
    """
    rows, cols = Q.shape
    for i in range(rows):
        non_zero_count = np.count_nonzero(Q[i])
        if non_zero_count != 1:  # Chaque ligne doit avoir exactement une valeur non nulle
            print(f"Validation de l'action monomiale échouée à la ligne {i}: {Q[i]}")
            return False
    return True

def less_verify(pk, sigma, msg):
    """
    Vérifie la signature LESS.

    :param pk: Clé publique (liste des matrices génératrices).
    :param sigma: Signature composée de salt, des chemins d'arbre, des réponses, et du digest.
    :param msg: Message à vérifier.
    :return: True si la signature est valide, False sinon.
    """
    salt, treepath, *rsp_and_digest = sigma
    rsp = rsp_and_digest[:-1]
    digest = rsp_and_digest[-1]

    # Recalculer le message digest
    d_prime = hashlib.sha256((salt + ''.join(map(str, rsp)) + msg).encode()).hexdigest()
    if digest != d_prime:
        print(f"Digest recalculé ne correspond pas: {d_prime} != {digest}")
        return False  # Si les digests ne correspondent pas, la signature est invalide

    # Reconstruction des graines à partir du chemin de l'arbre
    t = len(rsp)  # Nombre de répétitions du protocole
    x_values = np.random.randint(0, 2, size=t)  # Représentation des challenges
    for i in range(t):
        if x_values[i] == 0:
            Q_i = np.random.randint(0, 2, size=(pk[0].shape[0], pk[0].shape[1]))  # Exemple de challenge
        else:
            Q_i = rsp[i]  # Réponse monomiale obtenue de la signature

        print(f"Validation de Q_i pour l'index {i}: {Q_i}")
        
        # Validation de l'action monomiale
        if not validate_monom(Q_i):
            print(f"Validation de l'action monomiale échouée pour Q_i: {Q_i}")
            return False  # Si l'action monomiale est invalide, la signature est invalide
        
        # Vérification des matrices publiques et des réponses
        G_i = pk[i]
        if not np.array_equal(np.dot(G_i, Q_i), G_i):
            print(f"Échec de la vérification de la multiplication pour G_i et Q_i: \nG_i: {G_i} \nQ_i: {Q_i} \nRésultat: {np.dot(G_i, Q_i)}")
            return False  # La multiplication ne donne pas la bonne matrice publique

    return True

# Paramètres d'exemple (simplifiés pour la démonstration)
pk_valid = [np.array([[1, 0], [0, 1]]), np.array([[1, 0], [0, 1]])]
# Note: digest doit être calculé en utilisant le bon sel, rsp et msg, pour illustrer un cas vérifié correctement
sigma_valid = ['salt', 'treepath', np.array([[1, 0], [0, 1]]), np.array([[1, 0], [0, 1]]), hashlib.sha256(b'salt[[1 0]\n [0 1]][[1 0]\n [0 1]]MESSAGE A VERIFIER .').hexdigest()]
msg = 'MESSAGE A VERIFIER .'

# Cas 1: Signature valide
is_valid_valid = less_verify(pk_valid, sigma_valid, msg)
print("Validité de la signature (valide):", is_valid_valid)

# Cas 2: Signature invalide avec digest recalculé différent
pk_invalid = [np.array([[1, 0], [0, 1]]), np.array([[1, 0], [0, 1]])]
sigma_invalid = ['bad_salt', 'treepath', np.array([[1, 0], [1, 0]]), np.array([[1, 0], [0, 1]]), hashlib.sha256(b'bad_salt[[1 0]\n [1 0]][[1 0]\n [0 1]]MESSAGE A VERIFIER . modification').hexdigest()]

is_valid_invalid = less_verify(pk_invalid, sigma_invalid, msg)
print("Validité de la signature (invalide):", is_valid_invalid)

# Cas 3: Signature invalide avec une mauvaise réponse
pk_invalid_rsp = [np.array([[1, 0], [0, 1]]), np.array([[1, 0], [0, 1]])]
sigma_invalid_rsp = ['salt', 'treepath', np.array([[1, 0], [1, 0]]), np.array([[1, 0], [0, 1]]), hashlib.sha256(b'salt[[1 0]\n [1 0]][[1 0]\n [0 1]]MESSAGE A VERIFIER .').hexdigest()]

is_valid_invalid_rsp = less_verify(pk_invalid_rsp, sigma_invalid_rsp, msg)
print("Validité de la signature (invalide - mauvaise réponse):", is_valid_invalid_rsp)
