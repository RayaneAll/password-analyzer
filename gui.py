import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QProgressBar, QHBoxLayout
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import QTimer, Qt
from complexity_checker import analyze_password_strength

class PasswordAnalyzer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Analyseur de mots de passe")
        self.setGeometry(100, 100, 400, 270)

        # Activer le dark mode
        self.setStyleSheet("background-color: #121212; color: #ffffff;")

        self.layout = QVBoxLayout()

        self.label = QLabel("Entrez un mot de passe :")
        self.layout.addWidget(self.label)

        # Layout pour le champ de mot de passe + bouton œil
        self.password_layout = QHBoxLayout()

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("background-color: #1e1e1e; color: #ffffff; border: 1px solid #555; padding: 5px;")
        self.password_layout.addWidget(self.password_input)

        # Bouton pour afficher/cacher le mot de passe
        self.toggle_password_button = QPushButton()
        self.toggle_password_button.setIcon(QIcon("icons/eye_closed.png"))
        self.toggle_password_button.setStyleSheet("background: transparent; border: none;")
        self.toggle_password_button.setFixedSize(24, 24)
        self.toggle_password_button.clicked.connect(self.toggle_password_visibility)
        self.password_layout.addWidget(self.toggle_password_button)

        self.layout.addLayout(self.password_layout)

        self.analyze_button = QPushButton("Analyser")
        self.analyze_button.setStyleSheet("background-color: #6200EE; color: white; padding: 5px; border-radius: 5px;")
        self.analyze_button.clicked.connect(self.analyze_password)
        self.layout.addWidget(self.analyze_button)

        # Layout horizontal pour le résultat + icône centrée
        self.result_layout = QHBoxLayout()
        self.result_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.result_label = QLabel("")
        self.result_layout.addWidget(self.result_label)

        # Ajout d'une icône dynamique centrée
        self.icon_label = QLabel()
        self.icon_label.setPixmap(QPixmap("icons/base.png"))
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_layout.addWidget(self.icon_label)

        self.layout.addLayout(self.result_layout)

        # Ajout de la barre de progression
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

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

        score = self.get_password_score(strength)

        self.animate_progress(score)

        self.result_label.setText(f"Force du mot de passe : {strength}")
        self.update_progress_color(score)
        self.update_icon(strength)

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

    def update_icon(self, strength):
        """Met à jour l'icône en fonction de la force du mot de passe"""
        icon_mapping = {
            "Très faible": "icons/very_weak.png",
            "Faible": "icons/weak.png",
            "Moyen": "icons/medium.png",
            "Fort": "icons/strong.png",
            "Très fort": "icons/very_strong.png"
        }
        self.icon_label.setPixmap(QPixmap(icon_mapping[strength]))
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Assurer le centrage après le changement d'icône

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

    def toggle_password_visibility(self):
        """Affiche ou masque le mot de passe"""
        if self.password_input.echoMode() == QLineEdit.EchoMode.Password:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_password_button.setIcon(QIcon("icons/eye_open.png"))
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_password_button.setIcon(QIcon("icons/eye_closed.png"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordAnalyzer()
    window.show()
    sys.exit(app.exec())
