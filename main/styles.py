# QSS - Estilos do QT for Python
# https://doc.qt.io/qtforpython/tutorials/basictutorial/widgetstyling.html
# Dark Theme
# https://pyqtdarktheme.readthedocs.io/en/latest/how_to_use.html

import re
from pathlib import Path

import qdarktheme  # type: ignore

# CAMINHOS

ROOT_DIR = Path(__file__).parent
ICON_DIR = ROOT_DIR / 'files'
ICON = ICON_DIR / 'calc_icon.png'

# COLORS

PRIMARY_COLOR = '#1e81b0'
DARKER_PRIMARY_COLOR = '#16658a'
DARKEST_PRIMARY_COLOR = '#115270'

# SIZING

BIG_FONT_SIZE = 40
MEDIUM_FONT_SIZE = 24
SMALL_FONT_SIZE = 18
TEXT_MARGIN = 15
MINIMUM_WIDTH = 500

# NUMBERS CHECKING

NUM_OR_DOT_REGEX = re.compile(r'^[0-9.]$')


def isNumOrDot(string: str):
    return bool(NUM_OR_DOT_REGEX.search(string))


def convertToNumber(string: str):
    number = float(string)

    if number.is_integer():
        number = int(number)
    return number


def isValidNumber(string: str):
    valid = False
    try:
        float(string)
        valid = True
    except ValueError:
        ...
    return valid


def isEmpty(string: str):
    return len(string) == 0


# QSS - application THEME


qss = f"""
    QPushButton[cssClass="specialButton"] {{
        color: #fff;
        background: {PRIMARY_COLOR};
    }}
    QPushButton[cssClass="specialButton"]:hover {{
        color: #fff;
        background: {DARKER_PRIMARY_COLOR};
    }}
    QPushButton[cssClass="specialButton"]:pressed {{
        color: #fff;
        background: {DARKEST_PRIMARY_COLOR};
    }}
"""


def setupTheme():
    qdarktheme.setup_theme(
        theme='dark',
        corner_shape='rounded',
        custom_colors={
            "[dark]": {"primary": f"{PRIMARY_COLOR}", },
            "[light]": {"primary": f"{PRIMARY_COLOR}", },
        },
        additional_qss=qss,
    )
