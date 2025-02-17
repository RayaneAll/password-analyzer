import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtGui import QColor, QPalette
from complexity_checker import analyze_password_strength

class PasswordAnalyzer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Analyseur de mots de passe")
        self.setGeometry(100, 100, 400, 200)

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

        self.result_label = QLabel("")
        self.layout.addWidget(self.result_label)

        self.setLayout(self.layout)

    def analyze_password(self):
        password = self.password_input.text()
        strength = analyze_password_strength(password)
        self.result_label.setText(f"Force du mot de passe : {strength}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordAnalyzer()
    window.show()
    sys.exit(app.exec())
