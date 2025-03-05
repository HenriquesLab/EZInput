from ezinput import EZInput
from ezinput import EZInputPrompt


def test_header():
    gui = EZInputPrompt("Test")
    gui.add_header("Test Header")


def test_header_eg():
    eg = EZInput(title="Test", mode="prompt")
    eg.add_header("Test Header")
