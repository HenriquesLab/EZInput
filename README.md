# Easy GUI

Easy GUI is a Python library that simplifies the creation of graphical user interfaces (GUIs) both in the terminal and in Jupyter notebooks. It provides a convenient way to add various types of widgets, making it easier to interact with your code and visualize results.

## Installation

To install Easy GUI, you can use pip:

```bash
pip install easy_gui
```

## Usage

Easy GUI provides a single class `EasyGUI` that can be used to create GUIs in either the terminal or Jupyter notebooks. The mode is specified using the `mode` argument.

### Terminal Mode

To create a GUI in the terminal using prompt-toolkit:

```python
from easy_gui import EasyGUI

gui = EasyGUI(title="My Terminal GUI", mode="prompt")

# Add GUI elements
gui.add_yes_no("confirm", "Do you want to proceed?", remember_value=True)
gui.add_text("name", "Enter your name:", remember_value=True)
gui.add_int_range("age", "Enter your age:", 18, 100, remember_value=True)

# Save settings
gui.save_settings()

# Restore default settings
gui.restore_default_settings()
```

### Jupyter Notebook Mode

To create a GUI in Jupyter notebooks using ipywidgets:

```python
from easy_gui import EasyGUI

gui = EasyGUI(title="My Jupyter GUI", mode="jupyter")

# Add GUI elements
gui.add_text("text", value="Hello, world!")
gui.add_int_slider("int_slider", min=0, max=10, value=5)
gui.add_checkbox("checkbox", value=True)
gui.add_dropdown("dropdown", options=["Option 1", "Option 2", "Option 3"], value="Option 1")

# Display the GUI
gui.show()

# Save settings
gui.save_settings()
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.txt) file for details.
