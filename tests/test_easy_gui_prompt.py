from easy_gui import EasyGUI
from easy_gui.easy_gui_prompt import EasyGUIPrompt


def test_header():
    gui = EasyGUIPrompt("Test")
    gui.add_header("Test Header")


def test_header_eg():
    eg = EasyGUI(title="Test", mode="prompt")
    eg.add_header("Test Header")
