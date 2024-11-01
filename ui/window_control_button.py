from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import QPropertyAnimation, pyqtProperty, QEvent, Qt
from PyQt6.QtGui import QPainter, QColor, QBrush
from theme import THEME_COLORS

class WindowControlButton(QPushButton):
    def __init__(self, text, color, hover_color, parent=None):
        super().__init__(text, parent)
        self._opacity = 1.0
        self.base_color = QColor(color)
        self.hover_color = QColor(hover_color)
        self.current_color = self.base_color
        self.animation = QPropertyAnimation(self, b"opacity")
        self.animation.setDuration(150)
        self.setFixedSize(24, 24)

    def opacity(self):
        return self._opacity

    def setOpacity(self, opacity):
        self._opacity = opacity
        self.current_color = (
            self.hover_color if opacity < 1.0 else self.base_color
        )
        self.update()

    opacity = pyqtProperty(float, opacity, setOpacity)

    def enterEvent(self, event):
        self.animation.setStartValue(self._opacity)
        self.animation.setEndValue(0.7)
        self.animation.start()

    def leaveEvent(self, event):
        self.animation.setStartValue(self._opacity)
        self.animation.setEndValue(1.0)
        self.animation.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        color = self.current_color
        color.setAlphaF(self._opacity)
        painter.setBrush(QBrush(color))
        painter.drawEllipse(self.rect())
        text_color = (
            "white" if self.text() == "×" else THEME_COLORS['dark']
        )
        painter.setPen(QColor(text_color))
        painter.setFont(self.font())
        painter.drawText(
            self.rect(), Qt.AlignmentFlag.AlignCenter, self.text()
        )
