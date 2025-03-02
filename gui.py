import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QProgressBar, QHBoxLayout
from PyQt6.QtGui import QPixmap, QIcon, QClipboard
from PyQt6.QtCore import QTimer, Qt
from complexity_checker import analyze_password_strength, suggest_improvements

class PasswordAnalyzer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Analyseur de mots de passe")
        self.setGeometry(100, 100, 400, 300)

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
        self.password_input.textChanged.connect(self.analyze_password)  # Mode analyse en temps réel
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

        # Label pour afficher les suggestions d'amélioration
        self.suggestion_label = QLabel("")
        self.suggestion_label.setStyleSheet("color: #FFD700; font-size: 12px;")
        self.suggestion_label.setWordWrap(True)
        self.layout.addWidget(self.suggestion_label)

        # Barre de progression
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.layout.addWidget(self.progress_bar)

        self.setLayout(self.layout)

    def analyze_password(self):
        password = self.password_input.text()
        strength = analyze_password_strength(password)
        suggestions = suggest_improvements(password)

        score = self.get_password_score(strength)

        self.progress_bar.setValue(score)
        self.suggestion_label.setText(f"💡 Suggestions : {suggestions}" if suggestions else "✅ Aucun renforcement nécessaire")

    def toggle_password_visibility(self):
        """Affiche ou masque le mot de passe."""
        self.password_input.setEchoMode(QLineEdit.EchoMode.Normal if self.password_input.echoMode() == QLineEdit.EchoMode.Password else QLineEdit.EchoMode.Password)

        # Changer l'icône
        new_icon = "icons/eye_open.png" if self.password_input.echoMode() == QLineEdit.EchoMode.Normal else "icons/eye_closed.png"
        self.toggle_visibility_button.setIcon(QIcon(new_icon))

    def copy_password(self):
        """Copie le mot de passe dans le presse-papiers."""
        clipboard = QApplication.clipboard()
        clipboard.setText(self.password_input.text())

        self.copy_button.setIcon(QIcon("icons/copied.png"))
        QTimer.singleShot(1000, lambda: self.copy_button.setIcon(QIcon("icons/copy.png")))

    def get_password_score(self, strength):
        levels = ["Très faible", "Faible", "Moyen", "Fort", "Très fort"]
        return levels.index(strength) * 25

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordAnalyzer()
    window.show()
    sys.exit(app.exec())
