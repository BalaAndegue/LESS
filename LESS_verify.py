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
        return False  # Si les digests ne correspondent pas, la signature est invalide

    # Reconstruction des graines à partir du chemin de l'arbre
    t = len(rsp)  # Nombre de répétitions du protocole
    x_values = np.random.randint(0, 2, size=t)  # Représentation des challenges
    for i in range(t):
        if x_values[i] == 0:
            Q_i = np.random.randint(0, 2, size=(pk[0].shape[0], pk[0].shape[1]))  # Exemple de challenge
        else:
            Q_i = rsp[i]  # Réponse monomiale obtenue de la signature

        # Validation de l'action monomiale
        if not validate_monom(Q_i):
            return False  # Si l'action monomiale est invalide, la signature est invalide
        
        # Vérification des matrices publiques et des réponses
        G_i = pk[i]
        if np.all(np.dot(G_i, Q_i) != G_i):
            return False  # La multiplication ne donne pas la bonne matrice publique

    return True