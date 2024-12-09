import hashlib
import numpy as np

def less_sign(private_key, message, salt, n, q, t):
    """
    Génère une signature pour un message donné en utilisant la clé privée et un défi.

    :param private_key: La clé privée (matrice privée).
    :param message: Le message à signer.
    :param salt: Un sel cryptographique pour garantir l'unicité.
    :param n: Nombre de colonnes de la matrice.
    :param q: Taille du champ fini Fq.
    :param t: Poids fixe du défi (nombre de bits non nuls).
    :return: Signature (salt, challenge, response, digest).
    """
    # Générer un défi aléatoire de taille n
    challenge = np.random.randint(0, q, size=n)

    # Calculer la réponse à ce défi en fonction de la clé privée
    response = np.dot(private_key, challenge) % q  # Réponse en foncti…
# Paramètres de l'exemple
message = "Message à signer"
salt = "randomsalt"  # Sel cryptographique pour garantir l'unicité
t = 3  # Poids du défi
n = 6  # Nombre de colonnes dans la matrice
q = 7  # Taille du champ fini

# Générer la signature
signature = less_sign(private_key, message, salt, n, q, t)

print("Signature générée :")
print(signature)