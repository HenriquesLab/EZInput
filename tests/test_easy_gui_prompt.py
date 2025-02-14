from easy_gui import EasyGUI


def test_header():
    gui = EasyGUI("Test_GUI", mode="prompt")
    gui.add_header("Test Header")