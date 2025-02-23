import re

def analyze_password_strength(password):
    """Analyse la force d'un mot de passe et retourne un score de 0 à 4"""
    length_score = min(len(password) / 4, 2)

    if len(password) < 12:
        length_score = 0

    upper_score = 1 if re.search(r'[A-Z]', password) else 0
    lower_score = 1 if re.search(r'[a-z]', password) else 0
    digit_score = 1 if re.search(r'\d', password) else 0
    special_score = 1 if re.search(r'[!@#$%^&*(),.?":{}|<>]', password) else 0

    if len(password) > 6:
        unique_chars = len(set(password))
        repetition_score = max(0, (len(password) - unique_chars) / len(password))
        repetition_score = min(repetition_score * 3, 2)
    else:
        repetition_score = 0

    common_patterns = ["123456", "qwerty", "password", "abcdef", "letmein", "admin", "A1!", "abc123", "!@#$%^"]
    for pattern in common_patterns:
        if pattern in password.lower():
            repetition_score += 1

    total_score = length_score + upper_score + lower_score + digit_score + special_score - repetition_score - 1
    total_score = max(0, min(total_score, 4))

    levels = ["Très faible", "Faible", "Moyen", "Fort", "Très fort"]
    return levels[int(total_score)]

def suggest_improvements(password):
    """Analyse les faiblesses du mot de passe et propose des améliorations"""
    suggestions = []

    if len(password) < 12:
        suggestions.append("Ajoutez plus de caractères (minimum 12 recommandés).")

    uppercase_count = len(re.findall(r'[A-Z]', password))
    lowercase_count = len(re.findall(r'[a-z]', password))
    digit_count = len(re.findall(r'\d', password))
    special_count = len(re.findall(r'[!@#$%^&*(),.?":{}|<>]', password))

    if uppercase_count == 0:
        suggestions.append("Ajoutez au moins 2 majuscules.")
    elif uppercase_count == 1:
        suggestions.append("Ajoutez encore 1 majuscule.")

    if lowercase_count == 0:
        suggestions.append("Ajoutez au moins 2 minuscules.")
    elif lowercase_count == 1:
        suggestions.append("Ajoutez encore 1 minuscule.")

    if digit_count == 0:
        suggestions.append("Ajoutez au moins 2 chiffres.")
    elif digit_count == 1:
        suggestions.append("Ajoutez encore 1 chiffre.")

    if special_count == 0:
        suggestions.append("Ajoutez au moins 2 caractères spéciaux (!@#$%^&*...).")
    elif special_count == 1:
        suggestions.append("Ajoutez encore 1 caractère spécial.")

    common_patterns = ["123456", "qwerty", "password", "abcdef", "letmein", "admin", "A1!", "abc123", "!@#$%^"]
    for pattern in common_patterns:
        if pattern in password.lower():
            suggestions.append("Évitez les séquences trop courantes (ex: 123456, qwerty).")

    unique_chars = len(set(password))
    if len(password) > 6 and (len(password) - unique_chars) > 3:
        suggestions.append("Évitez trop de répétitions de caractères.")

    return " ".join(suggestions)
