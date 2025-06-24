from PyQt6.QtWidgets import QLabel, QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QFontMetrics, QPen

class RotatedLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.rotate(-90)
        painter.translate(-self.height(), self.width())
        metrics = QFontMetrics(self.font())
        text_rect = metrics.boundingRect(self.text())
        x = 2
        y = (self.width() - text_rect.height() + (metrics.ascent() / 2)) / -2   # Adjusted for vertical centering
        painter.drawText(int(x), int(y), self.text())

        painter.end()

    def sizeHint(self):
        base = super().sizeHint()
        return base.transposed()  # Swap width and height
