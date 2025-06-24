import sys
from PyQt6.QtWidgets import QDialog, QTableWidget, QTableWidgetItem, QMessageBox, QLabel, QPushButton
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QBrush, QColor
from view.components.rotated_label import RotatedLabel  # Import the custom widget

import os
from config import BASE_DIR

# Add the directory containing rotated_label.py to the Python module search path
sys.path.append(os.path.dirname(__file__))

class FlushingMatrixScreen(QDialog):
    def __init__(self, filaments, flushing_volumes, save_callback):
        super().__init__()
        loadUi(os.path.join(BASE_DIR, "assets", "flushing_matrix.ui"), self, {'RotatedLabel': RotatedLabel})
        self.setWindowTitle("Flushing Volume Matrix")
        self.save_callback = save_callback

        # setup required window properties
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.close_button.clicked.connect(lambda: self.close())
        self.minimize_button.clicked.connect(lambda: self.showMinimized())
        self.TitleBar.mouseMoveEvent = self.mouseMoveEvent

        # Set up the table
        self.tableWidget.setRowCount(len(filaments))
        self.tableWidget.setColumnCount(len(filaments))
        self.tableWidget.horizontalHeader().setVisible(False)  # Hide horizontal headers
        self.tableWidget.verticalHeader().setVisible(False)  # Hide vertical headers
        self.tableWidget.setProperty("class", "flushing_table")

        label_1 = self.findChild(QLabel, "label")
        label_1.setProperty("class", "heading")
        label_2 = self.findChild(QLabel, "label_2")
        label_2.setProperty("class", "heading")

        # Populate the labels for rows and columns
        for index, filament in enumerate(filaments):
            horizontal_label = self.findChild(QLabel, f"horizontalLabel_{index}")
            if horizontal_label:
                horizontal_label.setText(f"{filament['brand']} ({filament['material']})")
                horizontal_label.setProperty("class", "table_header")

            vertical_label = self.findChild(QLabel, f"verticalLabel_{index}")
            if vertical_label:
                vertical_label.setText(f"{filament['brand']} ({filament['material']})")
                vertical_label.setProperty("class", "table_header")

            # Set horizontal color labels (h_color_X)
            h_color_label = self.findChild(QLabel, f"h_color_{index}")
            if h_color_label and 'RGB_color' in filament and filament['RGB_color']:
                # print(f"Setting horizontal color label for index {index}, Filament RGB color: {filament['RGB_color']}")
                hex_color = filament['RGB_color']  # Example: "#FF5733"
                r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))  # Convert hex to RGB
                h_color_label.setStyleSheet(
                    '''background-color: rgb({0}, {1}, {2});
                    border: 1px solid rgb(0,0,0);
                    border-radius: 4px
                    '''.format(r, g, b))
            
            # Set vertical color labels (v_color_X)
            v_color_label = self.findChild(QLabel, f"v_color_{index}")
            if v_color_label and 'RGB_color' in filament and filament['RGB_color']:
                # print(f"Setting vertical color label for index {index}, Filament RGB color: {filament['RGB_color']}")
                hex_color = filament['RGB_color']  # Example: "#FF5733"
                r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))  # Convert hex to RGB
                v_color_label.setStyleSheet(
                    '''background-color: rgb({0}, {1}, {2});
                    border: 1px solid rgb(0,0,0);
                    border-radius: 4px
                    '''.format(r, g, b))

        # Populate the table with flushing volumes
        filament_ids = [f['id'] for f in filaments]
        for i, from_filament_id in enumerate(filament_ids):
            for j, to_filament_id in enumerate(filament_ids):
                volume = flushing_volumes.get((from_filament_id, to_filament_id), "")
                volume = int(float(volume)) if volume else ""
                item = QTableWidgetItem(str(volume))
                if not str(volume).isdigit():
                    item.setBackground(QBrush(QColor(0, 0, 0, 0)))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tableWidget.setItem(i, j, item)

        # Adjust table cell sizes
        for i in range(self.tableWidget.columnCount()):
            self.tableWidget.setColumnWidth(i, 40)  # Fixed width for each cell
        for i in range(self.tableWidget.rowCount()):
            self.tableWidget.setRowHeight(i, 40)  # Fixed height for each cell

        # Connect the save button
        self.findChild(QPushButton, "save_button").clicked.connect(self.save_changes)

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

    def save_changes(self):
        """Save changes to the flushing volumes."""
        changes = {}
        for i in range(self.tableWidget.rowCount()):
            for j in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(i, j)
                if item:
                    try:
                        volume = float(item.text())
                        changes[(i, j)] = volume
                    except ValueError:
                        continue

        # Confirm with the user
        confirm = QMessageBox.question(
            self,
            "Confirm Save",
            "Are you sure you want to save these changes? This action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            self.save_callback(changes)
