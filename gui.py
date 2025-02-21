import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QProgressBar
from PyQt6.QtGui import QColor, QPalette
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
        self.layout.addWidget(self.progress_bar)

        self.setLayout(self.layout)

    def analyze_password(self):
        password = self.password_input.text()
        strength = analyze_password_strength(password)

        # Calcul du score pour la progress bar
        score = self.get_password_score(strength)
        self.progress_bar.setValue(score)

        # Mise à jour du texte et de la couleur
        self.result_label.setText(f"Force du mot de passe : {strength}")
        self.update_text_color(score)

    def get_password_score(self, strength):
        levels = ["Très faible", "Faible", "Moyen", "Fort", "Très fort"]
        return levels.index(strength) * 25  # Convertir le score en pourcentage (0 à 100)

    def update_text_color(self, score):
        palette = self.result_label.palette()
        if score <= 25:
            palette.setColor(QPalette.ColorRole.WindowText, QColor("red"))
        elif score <= 50:
            palette.setColor(QPalette.ColorRole.WindowText, QColor("orange"))
        elif score <= 75:
            palette.setColor(QPalette.ColorRole.WindowText, QColor("yellow"))
        else:
            palette.setColor(QPalette.ColorRole.WindowText, QColor("green"))
        self.result_label.setPalette(palette)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordAnalyzer()
    window.show()
    sys.exit(app.exec())
