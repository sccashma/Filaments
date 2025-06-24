from PyQt6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QMessageBox, QAbstractScrollArea, QPushButton
from PyQt6.QtGui import QAction, QColor
from PyQt6.QtCore import Qt
from PyQt6 import uic

from view.components.form import FilamentForm
from view.components.flushing_volumes import FlushingMatrixScreen

import os
from config import BASE_DIR

class MainScreen(QMainWindow):
    def __init__(self):
        super(MainScreen, self).__init__()

        uic.loadUi(os.path.join(BASE_DIR, "assets", "main.ui"), self)

        # setup required window properties
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.close_button.clicked.connect(lambda: self.close())
        self.minimize_button.clicked.connect(lambda: self.showMinimized())
        self.TitleBar.mouseMoveEvent = self.mouseMoveEvent


        # define main ui elements
        self.add_button = self.findChild(QPushButton, "action_add")
        self.add_button.clicked.connect(self.add_filament)

        self.delete_button = self.findChild(QPushButton, "action_delete")
        self.delete_button.clicked.connect(self.delete_filament)

        self.edit_button = self.findChild(QPushButton, "action_edit")
        self.edit_button.clicked.connect(self.edit_filament)

        self.properties_button = self.findChild(QPushButton, "action_properties")
        self.properties_button.clicked.connect(self.view_properties)
        
        self.flushing_matrix_button = self.findChild(QPushButton, "action_flushing_matrix")
        self.flushing_matrix_button.clicked.connect(self.flushing_matrix)

        self.filaments_table = self.findChild(QTableWidget, "filaments_table")
        self.filaments_table.setColumnWidth(0, 50)
        self.filaments_table.setColumnWidth(1, 200)
        self.filaments_table.setColumnWidth(2, 200)
        self.filaments_table.setColumnWidth(3, 20)
        self.filaments_table.setColumnWidth(4, 200)

        # Set selection mode and behavior
        self.filaments_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.filaments_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.filaments_table.verticalHeader().setVisible(False)  # Hide vertical headers
        self.filaments_table.horizontalHeader().setVisible(False)  # Hide horizontal headers
        self.filaments_table.setShowGrid(False)
        self.filaments_table.setProperty("class", "table")

# TODO: THIS WORKS HERE, BUT NOT IN THE CSS FILE... DEBUG!!!!
        self.filaments_table.setStyleSheet("""
            background-color: #C8C8C8;
                                           """)

        self.setProperty("class", "window")
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.initial_pos = event.position().toPoint()
        super().mousePressEvent(event)
        event.accept()
    
    def mouseMoveEvent(self, event):
        if self.initial_pos is not None:
            delta = event.position().toPoint() - self.initial_pos
            self.window().move(
                self.window().x() + delta.x(),
                self.window().y() + delta.y(),
            )
        super().mouseMoveEvent(event)
        event.accept()
    
    def mouseReleaseEvent(self, event):
        self.initial_pos = None
        super().mouseReleaseEvent(event)
        event.accept()

    def add_filament(self):
        """Handle the Add Filament button click."""
        if self.presenter:
            self.presenter.show_add_filament_screen()

    def view_properties(self):
        """Handle the Properties button click."""
        filament_id = self.get_selected_filament_id()
        if self.presenter:
            self.presenter.show_filament_properties(filament_id)
        
    def flushing_matrix(self):
        """Handle the Flushing Matrix button click."""
        if self.presenter:
            self.presenter.show_flushing_matrix()

    def update_filament_list(self, filaments):
        """Update the table with the current filaments."""
        self.filaments_table.setRowCount(0)  # Clear existing rows

        for filament in filaments:
            row_position = self.filaments_table.rowCount()
            self.filaments_table.insertRow(row_position)
            self.filaments_table.setItem(row_position, 0, QTableWidgetItem(str(filament[0])))  # ID
            self.filaments_table.setItem(row_position, 1, QTableWidgetItem(filament[1]))  # Brand
            self.filaments_table.setItem(row_position, 2, QTableWidgetItem(filament[3]))  # Material
            self.filaments_table.setItem(row_position, 4, QTableWidgetItem(filament[2]))  # Color

            # Style the RGB_color cell
            rgb_color = filament[7]  # Assuming RGB_color is in the 8th column
            if rgb_color:
                color_item = QTableWidgetItem()  # Create an empty table item
                color_item.setBackground(QColor(rgb_color))  # Set the background color
                color_item.setFlags(color_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Make the cell non-editable
                self.filaments_table.setItem(row_position, 3, color_item)  # Set the item in the RGB_color column

    def get_selected_filament_id(self):
        selected_row = self.filaments_table.currentRow()
        if selected_row == -1:
            QMessageBox.critical(self, "Selection Error", "Please select a filament to edit.")
            return

        # Get the filament ID from the first column
        filament_id_item = self.filaments_table.item(selected_row, 0)
        if not filament_id_item:
            QMessageBox.critical(self, "Error", "Could not retrieve the filament ID.")
            return

        return int(filament_id_item.text())
    
    def edit_filament(self, s):
        """Handle the Edit Filament button click."""
        filament_id = self.get_selected_filament_id()

        # Pass the filament ID to the presenter
        if self.presenter:
            self.presenter.show_edit_filament_screen(filament_id)

    def delete_filament(self, s):
        """Handle the Delete Filament button click."""
        filament_id = self.get_selected_filament_id()

        # Confirm deletion
        confirm = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete the selected filament (ID: {filament_id})?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            if self.presenter:
                self.presenter.delete_filament(filament_id)

    def set_presenter(self, presenter):
        self.presenter = presenter

    def show_error(self, message):
        """Display an error message in a popup."""
        QMessageBox.critical(self, "Error", message)

    def show_properties_popup(self, properties):
        """Display the properties of a filament in a popup."""
        message = "\n".join([f"{key}: {value}" for key, value in properties.items()])
        QMessageBox.information(self, "Filament Properties", message)

    def show_form(self, filament=None, submit_callback=None):
        """Display a form for adding or editing a filament."""
        form = FilamentForm(submit_callback=submit_callback)

        # Dynamically populate the form if filament data is provided
        if filament:
            for key, value in filament.items():
                # Check if the form has a corresponding field for the key
                if hasattr(form, f"{key}_entry"):
                    field = getattr(form, f"{key}_entry")
                    field.setText(str(value))  # Set the value as text

                # Handle the RGB_color field specifically
                if key == "RGB_color" and value:
                    form.color_picker_button.setStyleSheet(f"background-color: {value};")
                    form.RGB_color = value

        # Show the form as a modal dialog
        form.exec()
    
    def show_flushing_matrix(self, filaments, flushing_volumes, save_callback):
        """Display the flushing volume matrix."""
        matrix_screen = FlushingMatrixScreen(filaments, flushing_volumes, save_callback)
        matrix_screen.exec()
