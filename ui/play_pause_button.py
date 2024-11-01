from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import (
    QPropertyAnimation, pyqtProperty, QPoint, QEvent, Qt
)
from PyQt6.QtGui import QPainter, QColor
from theme import THEME_COLORS

class PlayPauseButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_playing = True
        self.setFixedSize(64, 64)
        self.play_icon = "⯈"   # Triangle symbol
        self.pause_icon = "⏸"
        self.updateIcon()
        self._opacity = 1.0
        self.animation = QPropertyAnimation(self, b"opacity")
        self.animation.setDuration(150)

    def opacity(self):
        return self._opacity

    def setOpacity(self, opacity):
        self._opacity = opacity
        self.update()

    opacity = pyqtProperty(float, opacity, setOpacity)

    def updateIcon(self):
        icon = self.pause_icon if self.is_playing else self.play_icon
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                color: {THEME_COLORS['blue']};
                font-size: 32px;
                padding: 0px;
                text-align: center;
                line-height: 64px;
                margin: 0px;
                font-family: 'Arial Unicode MS', 'Segoe UI Symbol';
                min-width: 64px;
            }}
            QPushButton:hover {{
                color: {THEME_COLORS['light_blue']};
            }}
            QPushButton:pressed {{
                color: {THEME_COLORS['purple']};
            }}
        """)
        self.setText(icon)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        fm = painter.fontMetrics()
        text = self.text()
        text_width = fm.horizontalAdvance(text)
        text_height = fm.height()
        x = (self.width() - text_width) / 2
        y = (self.height() + text_height) / 2 - fm.descent()
        if not self.is_playing:
            x += 2  # Adjust for play icon
        color = QColor(THEME_COLORS['blue'])
        color.setAlphaF(self._opacity)
        painter.setPen(color)
        painter.setFont(self.font())
        painter.drawText(QPoint(int(x), int(y)), text)

    def enterEvent(self, event):
        self.animation.setStartValue(self._opacity)
        self.animation.setEndValue(0.7)
        self.animation.start()

    def leaveEvent(self, event):
        self.animation.setStartValue(self._opacity)
        self.animation.setEndValue(1.0)
        self.animation.start()
