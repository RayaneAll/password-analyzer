import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QProgressBar
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import QTimer
from complexity_checker import analyze_password_strength

class PasswordAnalyzer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Analyseur de mots de passe")
        self.setGeometry(100, 100, 400, 250)

        # Activer le dark mode
        self.setStyleSheet("background-color: #121212; color: #ffffff;")

        self.layout = QVBoxLayout()

        self.label = QLabel("Entrez un mot de passe :")
        self.layout.addWidget(self.label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("background-color: #1e1e1e; color: #ffffff; border: 1px solid #555; padding: 5px;")
        self.layout.addWidget(self.password_input)

        self.analyze_button = QPushButton("Analyser")
        self.analyze_button.setStyleSheet("background-color: #6200EE; color: white; padding: 5px; border-radius: 5px;")
        self.analyze_button.clicked.connect(self.analyze_password)
        self.layout.addWidget(self.analyze_button)

        # Label du résultat
        self.result_label = QLabel("")
        self.layout.addWidget(self.result_label)

        # Ajout de la barre de progression
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)  # 0% à 100%
        self.progress_bar.setValue(0)  # Valeur initiale

        # Style moderne pour la progress bar
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #555;
                border-radius: 5px;
                background-color: #1e1e1e;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #ff0000;
                border-radius: 5px;
            }
        """)

        self.layout.addWidget(self.progress_bar)
        self.setLayout(self.layout)

    def analyze_password(self):
        password = self.password_input.text()
        strength = analyze_password_strength(password)

        # Calcul du score pour la progress bar
        score = self.get_password_score(strength)

        # Animation fluide de la barre de progression
        self.animate_progress(score)

        # Mise à jour du texte et de la couleur de la progress bar
        self.result_label.setText(f"Force du mot de passe : {strength}")
        self.update_progress_color(score)

    def get_password_score(self, strength):
        levels = ["Très faible", "Faible", "Moyen", "Fort", "Très fort"]
        return levels.index(strength) * 25  # Convertir le score en pourcentage (0 à 100)

    def update_progress_color(self, score):
        """Change dynamiquement la couleur de la progress bar"""
        if score <= 25:
            color = "#FF3B30"  # Rouge
        elif score <= 50:
            color = "#FF9500"  # Orange
        elif score <= 75:
            color = "#FFD60A"  # Jaune
        else:
            color = "#30D158"  # Vert

        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid #555;
                border-radius: 5px;
                background-color: #1e1e1e;
                text-align: center;
                color: white;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 5px;
            }}
        """)

    def animate_progress(self, target_value):
        """Anime la progress bar en augmentant progressivement la valeur"""
        current_value = self.progress_bar.value()
        step = 1 if target_value > current_value else -1

        def update():
            nonlocal current_value
            if current_value != target_value:
                current_value += step
                self.progress_bar.setValue(current_value)
                QTimer.singleShot(10, update)  # Rafraîchir toutes les 10ms

        update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordAnalyzer()
    window.show()
    sys.exit(app.exec())
