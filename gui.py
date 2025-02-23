import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QProgressBar, QHBoxLayout
from PyQt6.QtGui import QPixmap, QIcon, QClipboard
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

        # Layout horizontal pour le champ de saisie + boutons
        self.input_layout = QHBoxLayout()

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("background-color: #1e1e1e; color: #ffffff; border: 1px solid #555; padding: 5px;")
        self.input_layout.addWidget(self.password_input)

        # Bouton pour afficher/cacher le mot de passe
        self.toggle_visibility_button = QPushButton()
        self.toggle_visibility_button.setIcon(QIcon("icons/eye_closed.png"))
        self.toggle_visibility_button.setStyleSheet("background: none; border: none; padding: 2px;")
        self.toggle_visibility_button.setFixedSize(24, 24)
        self.toggle_visibility_button.clicked.connect(self.toggle_password_visibility)
        self.input_layout.addWidget(self.toggle_visibility_button)

        # Bouton de copie
        self.copy_button = QPushButton()
        self.copy_button.setIcon(QIcon("icons/copy.png"))
        self.copy_button.setStyleSheet("background: none; border: none; padding: 2px;")
        self.copy_button.setFixedSize(24, 24)
        self.copy_button.clicked.connect(self.copy_password)
        self.input_layout.addWidget(self.copy_button)

        self.layout.addLayout(self.input_layout)

        self.analyze_button = QPushButton("Analyser")
        self.analyze_button.setStyleSheet("background-color: #6200EE; color: white; padding: 5px; border-radius: 5px;")
        self.analyze_button.clicked.connect(self.analyze_password)
        self.layout.addWidget(self.analyze_button)

        # Layout horizontal pour le résultat + icône centrée
        self.result_layout = QHBoxLayout()
        self.result_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.result_label = QLabel("")
        self.result_layout.addWidget(self.result_label)

        # Icône dynamique
        self.icon_label = QLabel()
        self.icon_label.setPixmap(QPixmap("icons/base.png"))
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_layout.addWidget(self.icon_label)

        self.layout.addLayout(self.result_layout)

        # Barre de progression
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
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

        # État initial du champ de mot de passe (caché)
        self.password_visible = False

    def analyze_password(self):
        password = self.password_input.text()
        strength = analyze_password_strength(password)

        score = self.get_password_score(strength)

        self.animate_progress(score)

        self.result_label.setText(f"Force du mot de passe : {strength}")
        self.update_progress_color(score)
        self.update_icon(strength)

    def toggle_password_visibility(self):
        """Affiche ou masque le mot de passe."""
        self.password_visible = not self.password_visible
        self.password_input.setEchoMode(QLineEdit.EchoMode.Normal if self.password_visible else QLineEdit.EchoMode.Password)

        # Changer l'icône
        new_icon = "icons/eye_open.png" if self.password_visible else "icons/eye_closed.png"
        self.toggle_visibility_button.setIcon(QIcon(new_icon))

    def copy_password(self):
        """Copie le mot de passe dans le presse-papiers et change temporairement l’icône."""
        clipboard = QApplication.clipboard()
        clipboard.setText(self.password_input.text())

        # Changer temporairement l'icône
        self.copy_button.setIcon(QIcon("icons/copied.png"))

        # Rétablir l'icône après 1 seconde
        QTimer.singleShot(1000, lambda: self.copy_button.setIcon(QIcon("icons/copy.png")))

    def get_password_score(self, strength):
        levels = ["Très faible", "Faible", "Moyen", "Fort", "Très fort"]
        return levels.index(strength) * 25

    def update_progress_color(self, score):
        if score <= 25:
            color = "#FF3B30"
        elif score <= 50:
            color = "#FF9500"
        elif score <= 75:
            color = "#FFD60A"
        else:
            color = "#30D158"

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
        icon_mapping = {
            "Très faible": "icons/very_weak.png",
            "Faible": "icons/weak.png",
            "Moyen": "icons/medium.png",
            "Fort": "icons/strong.png",
            "Très fort": "icons/very_strong.png"
        }
        self.icon_label.setPixmap(QPixmap(icon_mapping[strength]))
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def animate_progress(self, target_value):
        current_value = self.progress_bar.value()
        step = 1 if target_value > current_value else -1

        def update():
            nonlocal current_value
            if current_value != target_value:
                current_value += step
                self.progress_bar.setValue(current_value)
                QTimer.singleShot(10, update)

        update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordAnalyzer()
    window.show()
    sys.exit(app.exec())
