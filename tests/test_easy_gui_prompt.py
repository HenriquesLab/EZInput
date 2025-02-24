from ezgui4jupyter import EZGUI
from ezgui4jupyter import EZGUIPrompt


def test_header():
    gui = EZGUIPrompt("Test")
    gui.add_header("Test Header")


def test_header_eg():
    eg = EZGUI(title="Test", mode="prompt")
    eg.add_header("Test Header")
