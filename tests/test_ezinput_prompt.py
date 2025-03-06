from ezinput import EZInput
from ezinput import EZInputPrompt


def test_header():
    gui = EZInputPrompt("Test")
    gui.add_header("Test Header")


def test_header_eg():
    eg = EZInput(title="Test", mode="prompt")
    eg.add_header("Test Header")

def test_bounded_float_text():
    gui = EZInput(title="Test", mode="jupyter")
    gui.add_bounded_float_text(
        tag="test",
        value=0.5,
        min=0.01,
        max=1
    )