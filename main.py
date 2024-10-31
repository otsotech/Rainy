import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                           QSlider, QVBoxLayout, QWidget, QHBoxLayout)
from PyQt6.QtCore import (Qt, QPropertyAnimation, QEasingCurve, QPoint, 
                         QRect, pyqtProperty)
from PyQt6.QtGui import QPalette, QColor, QPainter, QBrush

# Theme Colors
THEME_COLORS = {
    'red': '#FF3B30',
    'pink': '#FF2D55',
    'purple': '#5856D6',
    'blue': '#007AFF',
    'light_blue': '#5AC8FA',
    'green': '#4CD964',
    'orange': '#FF9500',
    'yellow': '#FFCC00',
    'dark': '#1F1F21',
    'gray': '#8E8E93',
    'light_gray': '#C7C7CC',
    'background': '#F7F7F7'
}

class PlayPauseButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_playing = True
        self.setFixedSize(64, 64)
        
        # Custom symbols for play and pause icons
        self.play_icon = "⯈"  # Changed to a triangle symbol
        self.pause_icon = "⏸"
        
        # Initial state
        self.updateIcon()
        
        # Hover animation
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
        
        # Center text precisely
        fm = painter.fontMetrics()
        text = self.text()
        text_width = fm.horizontalAdvance(text)
        text_height = fm.height()
        
        x = (self.width() - text_width) / 2
        y = (self.height() + text_height) / 2 - fm.descent()
        
        if not self.is_playing:
            x += 2  # Center play icon more precisely
        
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
        self.current_color = QColor(self.hover_color if opacity < 1.0 else self.base_color)
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
        
        # Draw circular button background
        painter.setPen(Qt.PenStyle.NoPen)
        color = self.current_color
        color.setAlphaF(self._opacity)
        painter.setBrush(QBrush(color))
        painter.drawEllipse(self.rect())
        
        # Draw symbol
        painter.setPen(QColor(self.text() == "×" and "white" or THEME_COLORS['dark']))
        painter.setFont(self.font())
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text())

class RoundedWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Audio Controls")
        self.setFixedSize(320, 420)
        
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.oldPos = None
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(24)

        # Window controls
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(12)
        
        # Close button
        self.close_button = WindowControlButton("×", THEME_COLORS['red'], THEME_COLORS['pink'])
        self.close_button.clicked.connect(self.close)
        self.close_button.setFont(self.font())
        self.close_button.setStyleSheet("font-weight: bold; font-size: 16px;")
        
        # Minimize button
        self.minimize_button = WindowControlButton("−", THEME_COLORS['yellow'], THEME_COLORS['orange'])
        self.minimize_button.clicked.connect(self.showMinimized)
        self.minimize_button.setFont(self.font())
        self.minimize_button.setStyleSheet("font-weight: bold; font-size: 16px;")
        
        controls_layout.addWidget(self.close_button)
        controls_layout.addWidget(self.minimize_button)
        controls_layout.addStretch()
        main_layout.addLayout(controls_layout)

        # Toggle button
        self.toggle_button = PlayPauseButton()
        self.toggle_button.clicked.connect(self.toggle_play_pause)
        
        # Volume slider
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setFixedHeight(40)
        self.volume_slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                border: none;
                height: 4px;
                background: {THEME_COLORS['light_gray']};
                border-radius: 2px;
            }}
            QSlider::handle:horizontal {{
                background: {THEME_COLORS['blue']};
                border: none;
                width: 20px;
                height: 20px;
                margin: -8px 0;
                border-radius: 10px;
            }}
            QSlider::handle:horizontal:hover {{
                background: {THEME_COLORS['light_blue']};
            }}
            QSlider::sub-page:horizontal {{
                background: {THEME_COLORS['blue']};
                border-radius: 2px;
            }}
        """)
        
        main_layout.addStretch()
        main_layout.addWidget(self.toggle_button, 0, Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.volume_slider)
        main_layout.addStretch()

    def toggle_play_pause(self):
        self.toggle_button.is_playing = not self.toggle_button.is_playing
        self.toggle_button.updateIcon()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Background with subtle transparency
        background_color = QColor(THEME_COLORS['background'])
        background_color.setAlpha(252)  # Slightly transparent
        brush = QBrush(background_color)
        painter.setBrush(brush)
        painter.setPen(Qt.PenStyle.NoPen)
        
        rect = self.rect()
        painter.drawRoundedRect(rect, 24, 24)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.oldPos:
            delta = QPoint(event.globalPosition().toPoint() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPosition().toPoint()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = RoundedWindow()
    window.show()
    sys.exit(app.exec())
