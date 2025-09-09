from core.utils import detect_dark_mode


class StyleGenericBtn:


    @staticmethod
    def apply_style_btn():
        """
        Apply a style to a button based on the theme mode.

        Args:
            btn (QPushButton): The button to style.
            is_dark_mode (bool): True for dark mode, False for light mode.
        """
        is_dark_mode = detect_dark_mode()
        if is_dark_mode:
            style_btn = """
                QPushButton {
                    background-color: #64E9EE;
                    color: black;
                    border: none;
                    border-radius: 5px;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #45C4C9;
                }
                QPushButton:pressed {
                    background-color: #2A9EA8;
                }
            """
        else:
            style_btn = """
                QPushButton {
                    background-color: #0078D7;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #005A9E;
                }
                QPushButton:pressed {
                    background-color: #004578;
                }
            """
            return style_btn