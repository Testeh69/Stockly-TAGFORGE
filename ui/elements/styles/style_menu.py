from core.utils import detect_dark_mode



class StyleMenu:

    @staticmethod
    def apply_style_menu():
        """
        Apply a style to a menu based on the theme mode.

        Returns:
            str: The stylesheet for the menu.
        """
        is_dark_mode = detect_dark_mode()
        if is_dark_mode:
            style_menu = """
                QMenu {
                    background-color: qlineargradient(
                                x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #add8e6,  /* Bleu clair */
                                stop: 1 #1e90ff   /* Bleu plus foncé */
                    );                    
                    color: white;
                    border: 1px solid #3E3E42;
                }
                QMenu::item:selected {
                    background-color: #0078D7;
                }
            """
        else:
            style_menu = """
                QMenu {
                    background-color: #FFFFFF;
                    color: black;
                    border: 1px solid #C8C8C8;
                }
                QMenu::item:selected {
                    background-color: #E5E5E5;
                }
            """
        return style_menu            