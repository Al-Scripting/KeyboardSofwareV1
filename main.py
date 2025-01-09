from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QStackedWidget,
    QTabWidget, QColorDialog
)
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt


class KeyboardConfigurator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DIY Keyboard Configurator")
        self.setGeometry(100, 100, 1650, 850)  # Adjusted size for better spacing

        # Apply a dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2B2B2B;
            }
            QPushButton {
                background-color: #3C3F41;
                color: white;
                border: 1px solid #555;
                border-radius: 5px;
                font-size: 14px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #505357;
            }
            QLabel {
                color: white;
                font-size: 16px;
            }
            QTabWidget::pane {
                border: 1px solid #555;
            }
        """)

        # Main layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # Sidebar (Navigation)
        sidebar = QVBoxLayout()
        sidebar.setSpacing(10)

        sidebar_buttons = ["Keymap", "Lighting", "Macro", "Firmware Update", "Key Test", "Bug Report"]
        self.sidebar_btns = {}

        for btn_text in sidebar_buttons:
            btn = QPushButton(btn_text)
            btn.setFixedHeight(50)
            btn.setStyleSheet("font-size: 14px; width: 150px;")
            sidebar.addWidget(btn)
            self.sidebar_btns[btn_text] = btn

        # Stack for different views
        self.stack = QStackedWidget()
        self.keymap_view = QWidget()
        self.lighting_view = QWidget()

        self.stack.addWidget(self.keymap_view)
        self.stack.addWidget(self.lighting_view)

        # Connect sidebar buttons to views
        self.sidebar_btns["Keymap"].clicked.connect(lambda: self.show_view(self.keymap_view))
        self.sidebar_btns["Lighting"].clicked.connect(lambda: self.show_view(self.lighting_view))

        # Keyboard Layout View
        self.create_keymap_view()
        self.create_lighting_view()

        main_layout.addLayout(sidebar, 1)
        main_layout.addWidget(self.stack, 4)

        # Set default selected view
        self.show_view(self.keymap_view)

    def show_view(self, view):
        """ Switch to the selected tab. """
        self.stack.setCurrentWidget(view)

    def create_keymap_view(self):
        """ Creates the keymap customization UI. """
        layout = QVBoxLayout(self.keymap_view)
        label = QLabel("Key Mapping")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(label)

        # Profile selection
        self.profile_tabs = QTabWidget()
        profiles = ["Profile 1", "Profile 2"]
        self.keyboards = {}

        for profile in profiles:
            tab = QWidget()
            self.profile_tabs.addTab(tab, profile)
            self.keyboards[profile] = self.create_keyboard_grid(tab)

        layout.addWidget(self.profile_tabs)

        # Reset button
        reset_btn = QPushButton("Reset Layout")
        reset_btn.setStyleSheet("background-color: #D32F2F; font-weight: bold; font-size: 16px; height: 50px;")
        reset_btn.clicked.connect(self.reset_layout)
        layout.addWidget(reset_btn)

    def create_lighting_view(self):
        """ Creates the lighting customization UI. """
        layout = QVBoxLayout(self.lighting_view)
        label = QLabel("Lighting Configuration")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(label)

        # Same profile structure for lighting
        self.lighting_profiles = QTabWidget()
        for profile in ["Profile 1", "Profile 2"]:
            tab = QWidget()
            self.lighting_profiles.addTab(tab, profile)
            self.create_keyboard_grid(tab, mode="lighting")

        layout.addWidget(self.lighting_profiles)

    def create_keyboard_grid(self, parent_widget, mode="keymap"):
        """ Creates a full keyboard layout with proper spacing and alignment. """
        keyboard_layout = [
            ["Esc", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "PrtSc", "ScrLk", "Pause"],
            ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "Backspace"],
            ["Tab", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "[", "]", "\\"],
            ["Caps", "A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "'", "Enter"],
            ["LShift", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", "RShift"],
            ["LCtrl", "LWin", "LAlt", "Space", "RAlt", "RWin", "RCtrl"],
            ["Ins", "Home", "PgUp", "Del", "End", "PgDn"],
            ["Up", "Left", "Down", "Right"],
            ["NumLock", "/", "*", "-", "N7", "N8", "N9", "+"],
            ["N4", "N5", "N6"],
            ["N1", "N2", "N3", "Enter"],
            ["N0", ".", ""]
        ]

        grid = QGridLayout(parent_widget)
        keys = {}

        # Custom key sizes
        key_sizes = {
            "Backspace": (120, 50), "Tab": (100, 50), "Caps": (110, 50), "Enter": (110, 50),
            "LShift": (130, 50), "RShift": (130, 50), "Space": (400, 50),
        }

        for row_idx, row in enumerate(keyboard_layout):
            col_offset = 0
            for col_idx, char in enumerate(row):
                if not char:
                    col_offset += 1
                    continue
                btn = QPushButton(char)

                width, height = key_sizes.get(char, (65, 55))
                btn.setFixedSize(width, height)
                btn.setFont(QFont("Arial", 12))

                if mode == "lighting":
                    btn.clicked.connect(lambda checked, b=btn: self.change_key_color(b))

                grid.addWidget(btn, row_idx, col_idx + col_offset)
                keys[char] = btn

        return keys

    def change_key_color(self, button):
        """ Show color picker and update button color. """
        color = QColorDialog.getColor()
        if color.isValid():
            button.setStyleSheet(f"background-color: {color.name()};")

    def reset_layout(self):
        """ Reset keys to default layout. """
        for btn in self.keyboards[self.profile_tabs.tabText(self.profile_tabs.currentIndex())].values():
            btn.setText(btn.text())

if __name__ == "__main__":
    app = QApplication([])
    window = KeyboardConfigurator()
    window.show()
    app.exec_()
