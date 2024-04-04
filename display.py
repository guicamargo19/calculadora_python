import math

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import (QGridLayout, QLabel, QLineEdit, QMainWindow,
                               QMessageBox, QPushButton, QVBoxLayout, QWidget)
from styles import (BIG_FONT_SIZE, MEDIUM_FONT_SIZE, MINIMUM_WIDTH,
                    SMALL_FONT_SIZE, TEXT_MARGIN, convertToNumber, isEmpty,
                    isNumOrDot, isValidNumber)

# DISPLAY INPUT


class Display(QLineEdit):
    eqPressed = Signal()
    delPressed = Signal()
    clearPressed = Signal()
    inputPressed = Signal(str)
    operatorPressed = Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        self.setStyleSheet(f'font-size: {BIG_FONT_SIZE}px;')
        self.setMinimumHeight(BIG_FONT_SIZE * 2)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setTextMargins(*[TEXT_MARGIN for _ in range(4)])
        self.setMinimumWidth(MINIMUM_WIDTH)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        text = event.text().strip()
        key = event.key()
        KEYS = Qt.Key

        isEnter = key in [KEYS.Key_Enter, KEYS.Key_Return, KEYS.Key_Equal]
        isDelele = key in [KEYS.Key_Backspace, KEYS.Key_Delete, KEYS.Key_D]
        isEscape = key in [KEYS.Key_Escape, KEYS.Key_C]
        isOperator = key in [KEYS.Key_P, KEYS.Key_Minus,
                             KEYS.Key_Plus, KEYS.Key_Asterisk, KEYS.Key_Slash]

        if isEnter:
            self.eqPressed.emit()
            return event.ignore()

        if isDelele:
            self.delPressed.emit()
            return event.ignore()

        if isEscape:
            self.clearPressed.emit()
            return event.ignore()

        if isOperator:
            if text.lower() == 'p':
                text = '^'
            self.operatorPressed.emit(text)
            return event.ignore()


# NÃO PASSAR DAQUI SEM TEXTO

        if isEmpty(text):
            return event.ignore()

        if isNumOrDot(text):
            self.inputPressed.emit(text)
            return event.ignore()


# INFO LABEL


class Info(QLabel):
    def __init__(self, text: str, parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.configStyle()

    def configStyle(self):
        self.setStyleSheet(f'font-size: {SMALL_FONT_SIZE}px;')
        self.setAlignment(Qt.AlignmentFlag.AlignRight)

# MAIN_WINDOW


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        # Título da janela
        self.setWindowTitle('Calculadora')

        # Configurações do Layout básico
        self.cWidget = QWidget()
        self.vLayout = QVBoxLayout()
        self.cWidget.setLayout(self.vLayout)
        self.setCentralWidget(self.cWidget)

    def adjustFixedSize(self):
        # Última coisa a ser feita
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    def addWidgetToVLayout(self, widget: QWidget):
        self.vLayout.addWidget(widget)

    def addLayoutToVLayout(self, layout: QGridLayout):
        self.vLayout.addLayout(layout)

    def makeMsgBox(self):
        return QMessageBox(self)

# BOTÕES


class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        # self.setStyleSheet(f"font-size: {MEDIUM_FONT_SIZE}px;")
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75, 75)


class buttonsGrid(QGridLayout):
    def __init__(self, display: Display, info: Info, window: MainWindow,
                 *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._gridMask = [
            ['C', '+/-', '^', '/'],  # '◀' - BACKSPACE
            ['7', '8', '9', 'x'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0',  '', '.', '='],
        ]
        self.display = display
        self.info = info
        self.window = window
        self._equation = ''
        self._equationInitialValue = 'Sua Conta'
        self._right = None
        self._left = None
        self._op = None
        self.equation = self._equationInitialValue
        self._makeGrid()

    @property
    def equation(self):
        return self._equation

    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)

    def _makeGrid(self):
        self.display.eqPressed.connect(self._eq)
        self.display.delPressed.connect(self._backspace)
        self.display.clearPressed.connect(self._clear)
        self.display.inputPressed.connect(self._insertTextToDisplay)
        self.display.operatorPressed.connect(self._configLeftOp)

        for i, row in enumerate(self._gridMask):
            for j, buttonText in enumerate(row):

                if buttonText == '0':
                    button = Button(buttonText)
                    self.addWidget(button, i, j, 1, 2)
                elif buttonText == '':
                    continue
                else:
                    button = Button(buttonText)
                    self.addWidget(button, i, j)

                if not isNumOrDot(buttonText):
                    button.setProperty('cssClass', 'specialButton')
                    self._configSpecialButton(button)

                slot = self._makeButtonSlot(
                    self._insertTextToDisplay, buttonText)
                self._connectClicked(button, slot)

    def _connectClicked(self, button, slot):
        button.clicked.connect(slot)

    def _configSpecialButton(self, button):
        text = button.text()

        if text == 'C':
            self._connectClicked(button, self._clear)

        if text == '+/-':
            self._connectClicked(button, self._InvertNumber)

        if text in '+-/x^':
            self._connectClicked(button, self._makeButtonSlot(
                self._configLeftOp, text))

        if text == '=':
            self._connectClicked(button, self._eq)

    @Slot()
    def _makeButtonSlot(self, func, *args, **kwargs):
        @Slot()
        def realSlot():
            func(*args, **kwargs)
        return realSlot

    @Slot()
    def _insertTextToDisplay(self, text):
        newDisplayValue = self.display.text() + text

        if not isValidNumber(newDisplayValue):
            return

        self.display.insert(text)
        self.display.setPlaceholderText('')
        self.display.setFocus()

    @Slot()
    def _clear(self):
        self._right = None
        self._left = None
        self._op = None
        self.equation = self._equationInitialValue
        self.display.clear()
        self.display.setFocus()
        self.display.setPlaceholderText('')

    @Slot()
    def _configLeftOp(self, text):
        displayText = self.display.text()
        self.display.clear()
        self.display.setFocus()

        if isValidNumber(displayText):
            self._left = convertToNumber(displayText)

        if not isValidNumber(displayText) and self._left is None:
            self._showError('Nenhum número digitado.')
            return

        if self._left is None:
            self._left = convertToNumber(displayText)

        self._op = text
        self.equation = f'{self._left} {self._op} ??'

    @Slot()
    def _eq(self):
        displayText = self.display.text()

        if not isValidNumber(displayText) or self._left is None:
            return

        self._right = convertToNumber(displayText)
        self.equation = f'{self._left} {self._op} {self._right}'
        result = 'error'

        try:
            if '^' in self.equation and isinstance(self._left, int | float):
                result = math.pow(self._left, self._right)
                result = convertToNumber(str(result))
            elif 'x' in self.equation and isinstance(self._left, int | float):
                result = self._left * self._right
                result = convertToNumber(str(result))
            else:
                result = eval(self.equation)
                result = convertToNumber(str(result))
        except ZeroDivisionError:
            self._showError('Divisão inválida')
        except OverflowError:
            self._showError('Número muito grande')

        self.display.clear()
        self.info.setText(f'{self.equation} = {result}')

        self._left = result
        self._right = None

        if result == 'error':
            self._left = None

        self.display.setFocus()

    @Slot()
    def _backspace(self):
        self.display.backspace()
        self.display.setFocus()

    @Slot()
    def _InvertNumber(self):
        displayText = self.display.text()

        if not isValidNumber(displayText):
            return

        number = convertToNumber(displayText) * -1
        self.display.setText(str(number))

    def _showError(self, text):
        self.display.setPlaceholderText(text)
        """ msgBox = self.window.makeMsgBox()
        msgBox.setText(text) """
        """ msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.exec() """
