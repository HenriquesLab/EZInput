

from .ezinput_jupyter import EZInputJupyter
"""
EZInput Package

This package provides a set of tools for simplifying user input handling in Python applications. 
It includes modules for managing input in different environments, such as Jupyter notebooks 
and command-line prompts, as well as a general-purpose input handler.

Modules:
- ezinput_jupyter: Handles user input specifically in Jupyter notebook environments.
- ezinput_prompt: Provides utilities for managing command-line input prompts.
- ezinput: A general-purpose input handler for various use cases.

The EZInput package is designed to streamline the process of gathering and managing user input, 
making it easier to integrate into Python projects.
"""
from .ezinput_prompt import EZInputPrompt
from .ezinput import EZInput
