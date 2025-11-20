# Main application page
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor
from .gui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("SLYEST")
    app.setOrganizationName("Group 8")
    app.setApplicationVersion("0.1.0")
    
    window = MainWindow()
    window.show()

    # Start the event loop (keeps the app running until you close it)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()