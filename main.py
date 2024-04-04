# CALCULADORA MAIN PAGE

import sys

from display import Display, Info, MainWindow, buttonsGrid
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from styles import ICON, setupTheme

if __name__ == '__main__':
    # Cria a aplicação
    app = QApplication(sys.argv)
    setupTheme()
    window = MainWindow()

    # Definindo ícone da aplicação
    icon = QIcon(str(ICON))
    app.setWindowIcon(icon)
    window.setWindowIcon(icon)

    # Info
    info = Info('VE / operador / VD / igual / resultado')
    window.addWidgetToVLayout(info)

    # Display
    display = Display()
    window.addWidgetToVLayout(display)

    # Grid
    buttons_grid = buttonsGrid(display, info, window)
    window.addLayoutToVLayout(buttons_grid)

    # Executa a aplicação
    window.adjustFixedSize()
    window.show()
    app.exec()
