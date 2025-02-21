import re

def analyze_password_strength(password):
    """Analyse la force d'un mot de passe et retourne un score de 0 à 4"""
    # Vérification de la longueur
    length_score = min(len(password) / 4, 2)  # Limiter la longueur à 2 points maximum

    # Pénalité pour les mots de passe trop courts
    if len(password) < 12:
        length_score = 0  # Forcer un score faible pour les mots de passe trop courts
    
    # Vérification de la diversité des caractères (majuscule, minuscule, chiffre, spécial)
    upper_score = 1 if re.search(r'[A-Z]', password) else 0
    lower_score = 1 if re.search(r'[a-z]', password) else 0
    digit_score = 1 if re.search(r'\d', password) else 0
    special_score = 1 if re.search(r'[!@#$%^&*(),.?":{}|<>]', password) else 0

    # Vérification des répétitions de caractères
    if len(password) > 6:
        unique_chars = len(set(password))  # Nombre de caractères uniques
        repetition_score = max(0, (len(password) - unique_chars) / len(password))  # Proportion de répétitions
        repetition_score = min(repetition_score * 3, 2)  # Pénalité maximum de 2 points pour répétition
    else:
        repetition_score = 0  # Pas de pénalité pour les mots de passe courts

    # Pénaliser les mots de passe basés sur des séquences simples (qwerty, 123456, etc.)
    common_patterns = ["123456", "qwerty", "password", "abcdef", "letmein", "admin", "A1!", "abc123", "!@#$%^"]
    for pattern in common_patterns:
        if pattern in password.lower():  # Comparer de manière insensible à la casse
            repetition_score += 1  # Appliquer une pénalité pour les mots de passe avec des motifs simples

    # Calcul du score total
    total_score = length_score + upper_score + lower_score + digit_score + special_score - repetition_score - 1
    total_score = max(0, min(total_score, 4))  # Limiter à un score entre 0 et 4

    levels = ["Très faible", "Faible", "Moyen", "Fort", "Très fort"]
    return levels[int(total_score)]
