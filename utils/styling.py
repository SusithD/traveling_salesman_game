"""
Centralized styling for the Traveling Salesman Problem game
"""

class AppStyles:
    """Class to provide consistent styling across the application"""
    
    @staticmethod
    def get_dark_theme_stylesheet():
        """Returns the main dark theme stylesheet for the application"""
        return """
            QMainWindow, QWidget {
                background-color: black;
                color: white;
            }
            QMenuBar {
                background-color: black;
                color: white;
                border-bottom: 1px solid #444444;
            }
            QMenuBar::item {
                background-color: black;
                color: white;
                padding: 5px 10px;
            }
            QMenuBar::item:selected {
                background-color: #444444;
            }
            QMenu {
                background-color: black;
                color: white;
                border: 1px solid #444444;
            }
            QMenu::item {
                padding: 5px 30px 5px 20px;
                margin: 2px;
            }
            QMenu::item:selected {
                background-color: #444444;
            }
            QMessageBox {
                background-color: black;
                color: white;
            }
            QMessageBox QLabel {
                color: white;
            }
            QMessageBox QPushButton {
                background-color: #222222;
                color: white;
                border: 1px solid #444444;
                border-radius: 4px;
                padding: 6px 12px;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #444444;
            }
            QMessageBox QPushButton:pressed {
                background-color: #666666;
            }
            QLabel {
                color: white;
            }
            QTabWidget::pane {
                border: 1px solid #444444;
            }
            QTabBar::tab {
                background-color: #222222;
                color: white;
                padding: 8px 12px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: black;
                border-bottom: 2px solid white;
            }
            QLineEdit {
                background-color: #222222;
                color: white;
                border: 1px solid #444444;
                border-radius: 4px;
                padding: 5px;
            }
            QDialog {
                background-color: black;
                color: white;
            }
            QPushButton {
                background-color: #222222;
                color: white;
                border: 1px solid #444444;
                border-radius: 4px;
                padding: 8px 16px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #444444;
            }
            QPushButton:pressed {
                background-color: #666666;
            }
            QScrollArea {
                background-color: black;
                border: none;
            }
            QTextBrowser {
                background-color: black;
                color: white;
                border: 1px solid #444;
            }
            QGroupBox {
                border: 1px solid #444444;
                border-radius: 5px;
                margin-top: 1.5ex;
                padding: 10px;
                color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
                color: white;
                font-weight: bold;
            }
            QCheckBox {
                color: white;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 14px;
                height: 14px;
                border: 1px solid #666666;
            }
            QCheckBox::indicator:checked {
                background-color: #3498db;
                border: 1px solid #2980b9;
            }
        """
    
    @staticmethod
    def get_styled_frame_stylesheet():
        """Returns the stylesheet for styled frames"""
        return """
            background-color: black;
            color: white;
            border: 1px solid #444444;
            border-radius: 8px;
            padding: 10px;
            margin: 5px;
        """
    
    @staticmethod
    def get_input_field_stylesheet():
        """Returns the stylesheet for input fields"""
        return """
            background-color: #222222;
            color: white;
            border: 1px solid #444444;
            border-radius: 4px;
            padding: 5px;
        """
    
    @staticmethod
    def get_dialog_stylesheet():
        """Returns the stylesheet for dialogs"""
        return """
            QDialog {
                background-color: black;
                color: white;
            }
            QLabel {
                color: white;
            }
            QPushButton {
                background-color: #222222;
                color: white;
                border: 1px solid #444444;
                border-radius: 4px;
                padding: 6px 12px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #444444;
            }
        """
    
    @staticmethod
    def get_button_stylesheet():
        """Returns the stylesheet for buttons"""
        return """
            QPushButton {
                background-color: #222222;
                color: white;
                border: 1px solid #444444;
                border-radius: 4px;
                padding: 10px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #444444;
            }
            QPushButton:pressed {
                background-color: #666666;
            }
        """