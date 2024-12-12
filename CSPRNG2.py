import numpy as np

def csprng_fixed_weight_challenge(seed, t, ω, s):
    """
    Génère un défi à poids fixe en utilisant un CSPRNG.

    :param seed: La graine initiale pour générer le défi.
    :param t: Longueur totale du défi (nombre de bits).
    :param ω: Nombre de bits non nuls dans le défi.
    :param s: Taille de l'ensemble des défis possibles (valeurs dans [1, s-1]).
    :return: Tableau contenant un défi de longueur t et de poids fixe ω.
    """
    # Initialisation avec la graine
    np.random.seed(seed)

    # Étape 1 : Créer un tableau initialisé à zéro
    challenge = np.zeros(t, dtype=int)

    # Étape 2 : Générer les ω indices pour les bits non nuls
    non_zero_positions = np.random.choice(t, size=ω, replace=False)
    
    # Étape 3 : Attribuer des valeurs non nulles (dans [1, s-1]) aux positions sélectionnées
    for pos in non_zero_positions:
        challenge[pos] = np.random.randint(1, s)

    return challenge


# Exemple d'utilisation :
seed = 42  # Une graine pour garantir la reproductibilité
t = 8      # Longueur totale du défi
ω = 3      # Nombre de bits non nuls
s = 4      # Valeurs non nulles dans l'intervalle [1, s-1]

challenge = csprng_fixed_weight_challenge(seed, t, ω, s)

print("Défi généré :")
print(challenge)