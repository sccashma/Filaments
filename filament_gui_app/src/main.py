import sys
import os
from PyQt6.QtWidgets import QApplication
from view.main_screen import MainScreen
from presenter.main_presenter import MainPresenter
from model.database import Database  # Import the model
from tools.migration import migrate_database
from config import BASE_DIR

def main():
    db_file_path = os.path.join(BASE_DIR, "filament_data.db")
    migrate_database(db_file_path)  # Run migration script
    app = QApplication([])
    with open(os.path.join(BASE_DIR, "css", "application.css"), "r") as f:
        app.setStyleSheet(f.read())
    main_screen = MainScreen()
    model = Database(db_file_path)
    presenter = MainPresenter(main_screen, model)
    main_screen.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
