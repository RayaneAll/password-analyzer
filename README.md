# 🔐 Password Analyzer

**Password Analyzer** est une application Python avec interface graphique (GUI) développée avec **PyQt6**. Elle permet d’analyser en temps réel la force d’un mot de passe et fournit des suggestions de renforcement. Le tout dans une interface moderne, responsive et en dark mode.

---

## 🧠 Fonctionnalités

- Analyse complète de la force d’un mot de passe selon plusieurs critères.
- Affichage dynamique du niveau de sécurité (Très faible → Très fort).
- Suggestions en temps réel pour améliorer le mot de passe.
- Interface graphique épurée en **dark mode**.
- Composants interactifs :
  - Bouton pour afficher/masquer le mot de passe (œil).
  - Barre de progression animée.
  - Icône dynamique selon la force du mot de passe.
  - Copie rapide dans le presse-papiers.

---

## 🗂 Arborescence

```
password-analyzer/
├── complexity_checker.py     # Logique d’analyse de mot de passe
├── gui.py                    # Interface graphique avec PyQt6
├── main.py                   # Point d’entrée de l’application
```

---

## ⚙️ Critères d’analyse

Le score du mot de passe est calculé selon :
- ✅ Longueur du mot de passe
- ✅ Présence de majuscules / minuscules
- ✅ Présence de chiffres
- ✅ Présence de caractères spéciaux
- ❌ Répétitions trop fréquentes
- ❌ Séquences communes connues (`123456`, `qwerty`, etc.)

Le score final est compris entre 0 (Très faible) et 4 (Très fort).

---

## 💡 Suggestions de renforcement

Lorsque le mot de passe est jugé faible, l'application propose des conseils comme :
- Ajouter des majuscules, chiffres ou caractères spéciaux
- Éviter les séquences ou mots courants
- Augmenter la longueur du mot de passe
- Utiliser des caractères uniques

---

## 🖥 Pré-requis

- Python 3.8+
- PyQt6

> ✅ Optionnel mais recommandé : créer un environnement virtuel (`venv`)

---

## 🚀 Installation

```bash
# 1. Cloner le dépôt ou décompresser l'archive
cd password-analyzer

# 2. Créer un environnement virtuel
python3 -m venv .venv
source .venv/bin/activate  # (Windows: .venv\Scripts\activate)

# 3. Installer PyQt6
pip install PyQt6
```

---

## ▶️ Lancer l’application

```bash
python3 main.py
```

---

## 📁 Détail des fichiers

### `main.py`
Point d’entrée de l’application. Initialise la fenêtre principale `PasswordAnalyzer`.

### `gui.py`
Composants graphiques de l’application :
- Design en dark mode
- Champs de saisie, boutons et labels
- Interaction utilisateur (afficher/cacher, copier, analyser...)

### `complexity_checker.py`
Contient la logique d’évaluation de la complexité d’un mot de passe :
- Calcul du score
- Détection de séquences faibles
- Génération de recommandations

---

## 🔧 À venir / Améliorations possibles

- Générateur de mot de passe sécurisé intégré
- Sauvegarde locale (hashée) des mots de passe forts
- Mode "expert" avec visualisation du score numérique
- Intégration web avec Flask ou Electron

---

## 👨‍💻 Auteur

Projet développé par **Rayane**  
Étudiant en informatique passionné par la sécurité, l’UX et les interfaces modernes.

---

## 📜 Licence

Ce projet est open-source et libre d’utilisation.  
Licence : MIT