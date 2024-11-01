from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSlider
)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter, QColor, QBrush
from ui.play_pause_button import PlayPauseButton
from ui.window_control_button import WindowControlButton
from theme import THEME_COLORS
from audio.player import AudioPlayer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rain Sound")
        self.setFixedSize(320, 420)
        self.setWindowFlags(
            Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.oldPos = None

        # Audio player
        self.audio_player = AudioPlayer()

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(24)

        # Window control buttons
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(12)
        self.close_button = WindowControlButton(
            "×", THEME_COLORS['red'], THEME_COLORS['pink']
        )
        self.close_button.clicked.connect(self.close)
        self.close_button.setFont(self.font())
        self.close_button.setStyleSheet(
            "font-weight: bold; font-size: 16px;"
        )
        self.minimize_button = WindowControlButton(
            "−", THEME_COLORS['yellow'], THEME_COLORS['orange']
        )
        self.minimize_button.clicked.connect(self.showMinimized)
        self.minimize_button.setFont(self.font())
        self.minimize_button.setStyleSheet(
            "font-weight: bold; font-size: 16px;"
        )
        controls_layout.addWidget(self.close_button)
        controls_layout.addWidget(self.minimize_button)
        controls_layout.addStretch()
        main_layout.addLayout(controls_layout)

        # Play/Pause button
        self.toggle_button = PlayPauseButton()
        self.toggle_button.clicked.connect(self.toggle_play_pause)

        # Volume slider
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setFixedHeight(40)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(100)
        self.volume_slider.valueChanged.connect(self.change_volume)
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

        # Assemble main layout
        main_layout.addStretch()
        main_layout.addWidget(
            self.toggle_button, 0, Qt.AlignmentFlag.AlignCenter
        )
        main_layout.addWidget(self.volume_slider)
        main_layout.addStretch()

    def toggle_play_pause(self):
        self.toggle_button.is_playing = not self.toggle_button.is_playing
        self.toggle_button.updateIcon()
        if self.toggle_button.is_playing:
            self.audio_player.resume()
        else:
            self.audio_player.pause()

    def change_volume(self, value):
        volume = value / 100.0
        self.audio_player.set_volume(volume)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        background_color = QColor(THEME_COLORS['background'])
        background_color.setAlpha(252)
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
