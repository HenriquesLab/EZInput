# EZInput

[![PyPI](https://img.shields.io/pypi/v/ezinput.svg?color=green)](https://pypi.org/project/ezinput)
[![Python Version](https://img.shields.io/pypi/pyversions/ezinput.svg?color=green)](https://python.org)
[![Downloads](https://img.shields.io/pypi/dm/ezinput)](https://pypi.org/project/ezinput)
[![Docs](https://img.shields.io/badge/documentation-link-blueviolet)](https://henriqueslab.github.io/EZInput/)
[![License](https://img.shields.io/github/license/HenriquesLab/EZInput?color=Green)](https://github.com/HenriquesLab/EZInput/blob/main/LICENSE.txt)
[![Tests](https://github.com/HenriquesLab/EZInput/actions/workflows/oncall_test.yml/badge.svg)](https://github.com/HenriquesLab/EZInput/actions/workflows/oncall_test.yml.yml)
[![Coverage](https://img.shields.io/codecov/c/github/HenriquesLab/EZInput.svg?branch=main)](https://img.shields.io/codecov/c/github/HenriquesLab/EZInput?branch=main)
[![Contributors](https://img.shields.io/github/contributors-anon/HenriquesLab/EZInput)](https://github.com/HenriquesLab/EZInput/graphs/contributors)
[![GitHub stars](https://img.shields.io/github/stars/HenriquesLab/EZInput?style=social)](https://github.com/HenriquesLab/EZInput/)
[![GitHub forks](https://img.shields.io/github/forks/HenriquesLab/EZInput?style=social)](https://github.com/HenriquesLab/EZInput/)
[![DOI](https://img.shields.io/badge/Publication-Soon-purple)]()

<p align="center">
  <img src="docs/logo_white_bg.png" alt="EZInput Logo" width="400"/>
</p>

**Write once, run everywhere** - Create interactive GUIs that work seamlessly in both Jupyter notebooks and terminal environments with the exact same code.

EZInput is a Python library that simplifies creating user interfaces for data science, image analysis, and computational research. Whether you're prototyping in a notebook or deploying a command-line tool, your UI code remains identical.

## ✨ Key Features

- 🔄 **Unified API**: Same code works in Jupyter notebooks (.ipynb) and terminal scripts (.py)
- 📋 **Copy-Pastable**: Move code between notebooks and scripts without modification
- 💾 **Auto-Persistence**: Widget values are automatically saved and restored between sessions
- 🎯 **Type-Safe**: Validated inputs with type checking (int, float, text, paths, etc.)
- 🎨 **Rich Widgets**: Sliders, dropdowns, text inputs, file pickers, and more
- ⚡ **Zero Boilerplate**: No environment detection code needed - it just works

> **Note**: This project is currently in alpha stage and may undergo API changes.

## 🎯 Perfect For

- Image analysis pipelines requiring user parameters
- Data science workflows with interactive configuration
- Research tools that need both notebook and CLI interfaces
- Teaching and tutorials with reproducible parameter sets

## 📦 Installation

Install EZInput using pip:

```bash
pip install ezinput
```

For development with all optional dependencies:

```bash
pip install ezinput[all]
```

### Requirements

- Python >= 3.9
- Dependencies are automatically installed:
  - `ipywidgets` and `ipyfilechooser` for Jupyter notebooks
  - `prompt-toolkit` for terminal interfaces
  - `pyyaml` for configuration persistence

## 🚀 Quick Start

### The Simplest Example

```python
from ezinput import EZInput

# Create a GUI (works in both Jupyter and terminal!)
gui = EZInput("my_app")

# Add widgets - order of adding determines display order
name = gui.add_text("name", "Enter your name:")
age = gui.add_int_range("age", "Select age:", 18, 100)
confirm = gui.add_check("confirm", "Proceed with analysis?")

# In Jupyter: display the widgets
gui.show()

# Access values
print(f"Hello {name.value}, you are {age.value} years old")
if confirm.value:
    print("Starting analysis...")
```

### Running Jupyter Notebooks from Terminal

Execute notebooks as scripts using the `ezinput` command:

```bash
# Run a notebook from terminal
ezinput my_notebook.ipynb

# The notebook will execute with terminal-style prompts
# for all EZInput widgets
```

This is perfect for:
- Running analysis pipelines in batch mode
- Deploying notebook-based tools as CLI applications
- CI/CD integration

**💡 Copy-Paste Friendly**: This exact code works in both:
- Jupyter notebooks (.ipynb files) - displays interactive widgets
- Terminal scripts (.py files) - shows interactive prompts

Run in terminal with:
```bash
python my_script.py
```

### Real-World Example: Image Analysis

Here's a complete example for an image analysis pipeline:

```python
from ezinput import EZInput
import numpy as np

# One EZInput instance per analysis task recommended
gui = EZInput("image_analysis_v1")

# Configuration section
gui.add_label(value="=== Image Processing Parameters ===")
input_file = gui.add_text("input", "Input image path:", 
                          placeholder="/path/to/image.tif")
threshold = gui.add_float_range("threshold", "Detection threshold:", 
                                0.0, 1.0)
min_size = gui.add_int_range("min_size", "Minimum object size (pixels):", 
                             10, 1000)

gui.add_label(value="=== Output Options ===")
save_results = gui.add_check("save", "Save results to disk?")
output_format = gui.add_dropdown("format", ["PNG", "TIFF", "JPEG"], 
                                 "Output format:")

# Display GUI (in Jupyter) or collect inputs (in terminal)
gui.show()

# Your analysis code using the values
def run_analysis(values):
    """Process image with user-provided parameters."""
    print(f"Processing {values['input'].value}")
    print(f"Using threshold: {values['threshold'].value}")
    print(f"Minimum size: {values['min_size'].value}")
    
    # Your image processing code here
    # ...
    
    if values['save'].value:
        print(f"Saving as {values['format'].value}")

# Add a callback button (in Jupyter: creates button, in terminal: executes after show())
gui.add_callback("process", run_analysis, gui.get_values(), 
                 description="Run Analysis")
```

**Key Points:**
- Widget tags (like `"input"`, `"threshold"`) must be unique within each GUI instance
- Create one `EZInput` instance per analysis task or computational pipeline
- The order you add widgets is the order they appear on screen
- Use `remember_value=True` parameter on widgets to persist values between runs

### Terminal vs Jupyter: Same Code, Different Experience

**In Jupyter Notebook:**
- Widgets appear as interactive UI elements
- Sliders, dropdowns, and buttons are fully visual
- Call `gui.show()` to display the interface

**In Terminal:**
- Interactive prompts appear sequentially  
- Type-validated input with autocomplete
- Press Enter to submit each value
- Run with: `python your_script.py`

## 📚 Core Concepts

### 1. Automatic Environment Detection

EZInput automatically detects whether it's running in Jupyter or terminal:

```python
from ezinput import EZInput

# No environment detection code needed!
gui = EZInput("my_app")

# Or import specific versions if needed:
from ezinput import EZInputJupyter  # Jupyter-specific
from ezinput import EZInputPrompt   # Terminal-specific
```

### 2. Value Persistence & Priority

Values are automatically saved to `~/.ezinput/{title}.yml`. Priority order:

1. **Loaded parameters** (from `load_parameters()`)
2. **Remembered values** (from previous runs, if `remember_value=True` parameter)
3. **Explicit defaults** (passed via `default=` parameter)
4. **Widget defaults** (empty string, 0, False, etc.)

```python
# Values automatically persist when remember_value=True (default for most widgets)
gui = EZInput("my_app")
age = gui.add_int_range("age", "Age:", 0, 120, remember_value=True)
# Next time: shows the previously entered value!

# Load from specific configuration file
gui = EZInput("my_app")
gui.load_parameters("experiment_config.yml")

# Or save current values to share
gui.save_parameters("my_optimal_params.yml")
```

### 3. Configuration Files

Create shareable configuration files:

```python
gui = EZInput("my_analysis")

# ... add widgets and collect values ...

# Save current values
gui.save_parameters("my_config.yml")  # Explicit filename
# or
gui.save_parameters("")  # Auto-named: my_analysis_parameters.yml

# Share this file with colleagues!
# They can load it:
gui2 = EZInput("my_analysis", params_file="my_config.yml")
```

**Config file location:**
- Explicit saves: wherever you specify
- Auto-saved settings: `~/.ezinput/{title}.yml`

**Resetting to defaults:**
```python
# Clear all remembered values - returns widgets to original defaults
gui.restore_defaults()

# ⚠️ Important: Re-run your cell (Jupyter) or script (terminal) to see the reset take effect
# The method removes the memory file but doesn't immediately change displayed widgets
```

## 🎨 Available Widgets

All widgets work identically in Jupyter and terminal. Here's the complete reference:

### Text Input Widgets

| Widget | Description | Example |
|--------|-------------|---------|
| `add_text()` | Single-line text input | `gui.add_text("name", "Your name:")` |
| `add_text_area()` | Multi-line text input | `gui.add_text_area("notes", "Comments:")` |

```python
# Text input with placeholder
email = gui.add_text("email", "Email address:", 
                     placeholder="user@example.com")

# Multi-line text area
notes = gui.add_text_area("description", "Project description:",
                          placeholder="Enter detailed description...")
```

### Numeric Input Widgets

| Widget | Description | Example |
|--------|-------------|---------|
| `add_int_range()` | Integer slider/input with bounds | `gui.add_int_range("count", "Count:", 1, 100)` |
| `add_float_range()` | Float slider/input with bounds | `gui.add_float_range("alpha", "Alpha:", 0.0, 1.0)` |
| `add_int_text()` | Integer input (no bounds) | `gui.add_int_text("age", "Age:")` |
| `add_float_text()` | Float input (no bounds) | `gui.add_float_text("weight", "Weight:")` |
| `add_bounded_int_text()` | Integer input with validation | `gui.add_bounded_int_text("percent", "%:", 0, 100)` |
| `add_bounded_float_text()` | Float input with validation | `gui.add_bounded_float_text("ratio", "Ratio:", 0.0, 1.0)` |

```python
# Slider-style (Jupyter) or validated prompt (terminal)
iterations = gui.add_int_range("iter", "Iterations:", 10, 1000)

# Free-form number input
temperature = gui.add_float_text("temp", "Temperature (°C):")

# Bounded input with automatic clamping
percentage = gui.add_bounded_int_text("coverage", "Coverage %:", 0, 100)
```

### Selection Widgets

| Widget | Description | Example |
|--------|-------------|---------|
| `add_check()` | Boolean yes/no or checkbox | `gui.add_check("verbose", "Enable verbose output?")` |
| `add_dropdown()` | Single selection from list | `gui.add_dropdown("method", ["A", "B", "C"], "Method:")` |

```python
# Boolean checkbox (Jupyter) or yes/no prompt (terminal)
debug = gui.add_check("debug", "Enable debug mode?")

# Dropdown with autocomplete in terminal
algorithm = gui.add_dropdown("algo", 
                             ["linear", "rbf", "polynomial"],
                             "Interpolation method:")
```

### File & Path Widgets

| Widget | Environment | Description |
|--------|-------------|-------------|
| `add_path_completer()` | Terminal only | Path input with autocomplete |
| `add_file_upload()` | Jupyter only | Visual file picker |

```python
# Terminal: autocomplete-enabled path input
input_file = gui.add_path_completer("input", "Select input file:")

# Jupyter: visual file browser
input_file = gui.add_file_upload("input", accept="*.tif")
```

### Display Widgets

| Widget | Description | Example |
|--------|-------------|---------|
| `add_label()` | Static text/header | `gui.add_label(value="=== Settings ===")` |
| `add_output()` | Output display area (Jupyter) | `gui.add_output("results")` |
| `add_HTML()` | Rich HTML content (Jupyter only) | `gui.add_HTML("info", "<b>Note:</b> ...")` |

```python
# Section headers
gui.add_label(value="=== Input Parameters ===")

# Output area for results (Jupyter)
gui.add_output("results")
with gui["results"]:
    print("Analysis complete!")

# Rich formatting (Jupyter only)
gui.add_HTML("warning", '<p style="color:red">⚠️ Experimental feature</p>')
```

### Callback & Actions

```python
# add_callback ensures naming consistency between Jupyter and terminal
def process_data(values):
    """Process data with current parameter values."""
    threshold = values["threshold"].value
    method = values["method"].value
    print(f"Processing with {method} at threshold {threshold}")
    # Your processing code here...

# In Jupyter: creates a button
# In terminal: executes immediately
gui.add_callback("run", process_data, gui.get_values(), 
                 description="Start Processing")
```

**Why `add_callback`?** 
The name maintains API consistency between Jupyter (button-based) and terminal (immediate execution) interfaces.

## 💡 Best Practices

### 1. Unique Widget Tags

```python
# ✅ Good: unique tags
gui.add_text("input_file", "File:")
gui.add_text("output_file", "Output:")

# ❌ Bad: duplicate tags
gui.add_text("file", "File:")
gui.add_text("file", "Output:")  # Overwrites the first one!
```

### 2. One GUI Per Task

```python
# ✅ Good: separate GUIs for different analyses
preprocessing_gui = EZInput("preprocessing_v1")
analysis_gui = EZInput("main_analysis_v2")

# ❌ Avoid: reusing the same GUI instance for different purposes
gui = EZInput("multi_purpose")  # Config files may conflict
```

### 3. Meaningful Titles

```python
# ✅ Good: descriptive, versioned titles
gui = EZInput("cell_segmentation_v2")
gui = EZInput("image_denoising_2024")

# ✅ Also good: user/project specific
gui = EZInput("john_experiment_setup")

# ❌ Avoid: generic titles that may conflict
gui = EZInput("test")
gui = EZInput("gui")
```

### 4. Display Order Matters

```python
# Widgets appear in the order you add them
gui = EZInput("my_app")

# This order...
gui.add_label(value="=== Step 1 ===")
gui.add_text("name", "Name:")
gui.add_int_range("age", "Age:", 0, 120)
gui.add_label(value="=== Step 2 ===")  
gui.add_check("confirm", "Confirm?")

# ...is the order users see them in
gui.show()
```

## 📖 Documentation

- **[Full Documentation](https://henriqueslab.github.io/EZInput/)**: Comprehensive guides and API reference
- **[Widget Gallery](https://henriqueslab.github.io/EZInput/widgets.html)**: Interactive examples of all widgets
- **[Tutorials](https://henriqueslab.github.io/EZInput/tutorials.html)**: Step-by-step guides
- **[API Reference](https://henriqueslab.github.io/EZInput/api.html)**: Detailed method documentation

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.


---

**Made with ❤️ for the scientific Python community**