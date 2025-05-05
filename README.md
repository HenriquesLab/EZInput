# EZInput

[![PyPI](https://img.shields.io/pypi/v/ezinput.svg?color=green)](https://pypi.org/project/ezinput)
[![Python Version](https://img.shields.io/pypi/pyversions/ezinput.svg?color=green)](https://python.org)
[![Downloads](https://img.shields.io/pypi/dm/ezinput)](https://pypi.org/project/ezinput)
[![Docs](https://img.shields.io/badge/documentation-link-blueviolet)](https://henriqueslab.github.io/EZInput/ezinput.html)
[![License](https://img.shields.io/github/license/HenriquesLab/EZInput?color=Green)](https://github.com/HenriquesLab/EZInput/blob/main/LICENSE.txt)
[![Tests](https://github.com/HenriquesLab/EZInput/actions/workflows/oncall_test.yml/badge.svg)](https://github.com/HenriquesLab/EZInput/actions/workflows/oncall_test.yml.yml)
[![Coverage](https://img.shields.io/codecov/c/github/HenriquesLab/EZInput.svg?branch=main)](https://img.shields.io/codecov/c/github/HenriquesLab/EZInput?branch=main)
[![Contributors](https://img.shields.io/github/contributors-anon/HenriquesLab/EZInput)](https://github.com/HenriquesLab/EZInput/graphs/contributors)
[![GitHub stars](https://img.shields.io/github/stars/HenriquesLab/EZInput?style=social)](https://github.com/HenriquesLab/EZInput/)
[![GitHub forks](https://img.shields.io/github/forks/HenriquesLab/EZInput?style=social)](https://github.com/HenriquesLab/EZInput/)
[![DOI](https://img.shields.io/badge/Publication-Soon-purple)]()

EZInput is a Python library that simplifies the creation of user interfaces both in the terminal and in Jupyter notebooks. It provides a convenient way to add various types of widgets, making it easier to interact with your code and visualize results.  
  
DISCLAIMER: the project is currently in alpha stage and will likely suffer changes in the API and functionality.

## Installation

To install EZInput, you can use pip:

```bash
pip install ezinput
```

## Usage

EZInput provides a unified interface for creating UIs in either the terminal or Jupyter notebooks. The mode is automatically determined based on the environment.

### Terminal Mode

To create a GUI in the terminal using `prompt_toolkit`:

```python
from ezinput import EZInput

gui = EZInput(title="My Terminal GUI")

# Add GUI elements
gui.add_check("confirm", "Do you want to proceed?", remember_value=True)
gui.add_text("name", "Enter your name:", placeholder="John Doe", remember_value=True)
gui.add_int_range("age", "Enter your age:", 18, 100, remember_value=True)
gui.add_float_range("height", "Enter your height (in meters):", 1.0, 2.5, remember_value=True)
gui.add_dropdown("color", "Choose your favorite color:", ["Red", "Blue", "Green"], remember_value=True)
gui.add_path_completer("file_path", "Enter a file path:", remember_value=True)

# Save settings
gui.save_settings()

# Restore default settings
gui.restore_default_settings()
```

### Jupyter Notebook Mode

To create a GUI in Jupyter notebooks using `ipywidgets`:

```python
from ezinput import EZInput

gui = EZInput(title="My Jupyter GUI")

# Add GUI elements
gui.add_text("text", description="Enter some text:", placeholder="Hello, world!", remember_value=True)
gui.add_int_range("int_slider", description="Choose a number:", vmin=0, vmax=10, remember_value=True)
gui.add_float_range("float_slider", description="Choose a decimal:", vmin=0.0, vmax=1.0, remember_value=True)
gui.add_check("checkbox", description="Check this box:", remember_value=True)
gui.add_dropdown("dropdown", options=["Option 1", "Option 2", "Option 3"], description="Choose an option:", remember_value=True)
gui.add_file_upload("file_upload", accept=".txt", multiple=False)

# Display the GUI
gui.show()

# Save settings
gui.save_settings()
```

### Unified API

EZInput provides a unified API for both terminal and Jupyter notebook modes. The following methods are available:

- **`add_label(tag, label)`**: Add a label to the GUI.
- **`add_text(tag, description, placeholder="", remember_value=False)`**: Add a text input field.
- **`add_text_area(tag, description, placeholder="", remember_value=False)`**: Add a multi-line text area.
- **`add_int_range(tag, description, vmin, vmax, remember_value=False)`**: Add an integer slider or range input.
- **`add_float_range(tag, description, vmin, vmax, remember_value=False)`**: Add a float slider or range input.
- **`add_check(tag, description, remember_value=False)`**: Add a yes/no or checkbox input.
- **`add_dropdown(tag, options, description="", remember_value=False)`**: Add a dropdown menu.
- **`add_callback(tag, func, values, description="Run")`**: Add a function to be ran (if in jupyter, after the press of the generated button) that triggers a callback function.

### Saving and Restoring Settings

EZInput allows you to save and restore widget values using configuration files:

```python
# Save current settings
gui.save_settings()

# Restore default settings
gui.restore_default_settings()
```

### Examples

#### Terminal Example

```python
from ezinput import EZInput

gui = EZInput(title="Terminal Example")
gui.add_text("username", "Enter your username:", remember_value=True)
gui.add_int_range("age", "Enter your age:", 18, 100, remember_value=True)
gui.save_settings()
```

#### Jupyter Notebook Example

```python
from ezinput import EZInput

gui = EZInput(title="Jupyter Example")
gui.add_text("username", description="Enter your username:", remember_value=True)
gui.add_int_range("age", description="Enter your age:", vmin=18, vmax=100, remember_value=True)
gui.show()
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.txt) file for details.
