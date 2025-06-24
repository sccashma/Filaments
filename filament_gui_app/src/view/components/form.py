from PyQt6.QtWidgets import QDialog, QPushButton, QLineEdit, QColorDialog, QMessageBox
from PyQt6 import uic

import os
from config import BASE_DIR

class FilamentForm(QDialog):
    def __init__(self, submit_callback=None, cancel_callback=None):
        super(FilamentForm, self).__init__()
        self.submit_callback = submit_callback
        self.cancel_callback = cancel_callback
        self.RGB_color = None
        
        uic.loadUi(os.path.join(BASE_DIR, "assets", "form.ui"), self)
        self.setWindowTitle("Add Filament")

        self.brand_entry = self.findChild(QLineEdit, "input_brand")
        self.material_entry = self.findChild(QLineEdit, "input_material")
        self.color_entry = self.findChild(QLineEdit, "input_color")
        self.weight_entry = self.findChild(QLineEdit, "input_weight")
        self.purchase_link_entry = self.findChild(QLineEdit, "input_purchase_link")
        self.cost_entry = self.findChild(QLineEdit, "input_cost")
        self.k_factor_entry = self.findChild(QLineEdit, "input_k_factor")
        self.flow_rate_entry = self.findChild(QLineEdit, "input_flow_rate")

        self.color_picker_button = self.findChild(QPushButton, "color_picker")

        self.color_picker_button.clicked.connect(self.pick_color)
        self.submit_button.clicked.connect(self.submit)
        self.cancel_button.clicked.connect(self.cancel)

        self.setProperty("class", "window")

    def pick_color(self):
        """Open a color picker dialog and set the button's background color."""
        color = QColorDialog.getColor()  # Open the color picker dialog
        if color.isValid():  # Check if the user selected a valid color
            self.RGB_color = color.name()  # Store the selected color as a hex string
            self.color_picker_button.setStyleSheet(f"background-color: {self.RGB_color};")  # Update button color
        
    def validate_inputs(self):
        """Validate all input fields."""
        if not self.brand_entry.text().strip():
            self.show_error("Brand cannot be empty.")
            return False
        if not self.color_entry.text().strip():
            self.show_error("Color cannot be empty.")
            return False
        if not self.material_entry.text().strip():
            self.show_error("Material cannot be empty.")
            return False
        if not self.purchase_link_entry.text().strip():
            self.show_error("Purchase Link cannot be empty.")
            return False
        if not str(self.RGB_color).strip() or str(self.RGB_color) == 'None':
            self.show_error("RGB Color cannot be empty.")
            return False

        # Validate numeric fields
        try:
            float(self.weight_entry.text())
        except ValueError:
            self.show_error("Weight must be a valid number.")
            return False

        try:
            float(self.cost_entry.text())
        except ValueError:
            self.show_error("Cost must be a valid number.")
            return False
        
        try:
            float(self.k_factor_entry.text())
        except ValueError:
            self.k_factor_entry.setText("0.0") # default value

        try:
            float(self.flow_rate_entry.text())
        except ValueError:
            self.show_error("Flow Rate must be a valid number.")
            self.flow_rate_entry.setText("0.0") # default value
            return False

        return True

    def show_error(self, message):
        """Display an error message in a popup."""
        QMessageBox.critical(self, "Error", message)

    def submit(self):
        """Handle form submission."""
        if not self.validate_inputs():
            return

        if self.submit_callback:
            data = {
                'brand': self.brand_entry.text(),
                'color': self.color_entry.text(),
                'material': self.material_entry.text(),
                'weight': self.weight_entry.text(),
                'purchase_link': self.purchase_link_entry.text(),
                'cost': self.cost_entry.text(),
                'RGB_color': self.RGB_color,
                'k_factor': self.k_factor_entry.text(),
                'flow_rate': self.flow_rate_entry.text()  # New field
            }
            self.submit_callback(data)
        self.accept()

    def cancel(self):
        """Handle form cancellation."""
        if self.cancel_callback:
            self.cancel_callback()
        self.reject()