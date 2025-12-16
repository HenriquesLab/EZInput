import os
import yaml
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter, PathCompleter
from prompt_toolkit.validation import Validator, ValidationError
from pathlib import Path

from typing import Optional

"""
A module to help simplify the create of GUIs in terminals using python prompt-toolkit.
"""


CONFIG_PATH = Path.home() / ".ezinput"

if not os.path.exists(CONFIG_PATH):
    os.makedirs(CONFIG_PATH)


class Element:
    """A simple wrapper class for widget values.

    Parameters
    ----------
    value : Any
        The value to store in the element.
    """

    def __init__(self, value):
        self.value = value


class EZInputPrompt:
    """A class to create terminal-based GUIs using `prompt_toolkit`.

    This class provides a simple interface for creating interactive terminal
    GUIs with various input widgets. Settings are automatically saved and
    restored between sessions.

    Parameters
    ----------
    title : str
        Title of the GUI, used to store settings and identify the
        configuration file.

    Examples
    --------
    >>> gui = EZInputPrompt("my_app")
    >>> name = gui.add_text("name", "Enter your name")
    >>> age = gui.add_int_text("age", "Enter your age")
    >>> gui.show()
    """

    def __init__(self, title: str):
        """Initialize the terminal-based GUI.

        Creates a new GUI instance and loads any previously saved settings
        from the configuration file.

        Parameters
        ----------
        title : str
            Title of the GUI, used to identify the configuration file.
        """
        self.title = title
        self.elements = {}
        self.cfg = self._get_config(title)
        self.params = None
        self._nLabels = 0

    def __getvalue__(self, tag: str):
        """
        @unified
        Get the value of a widget.

        Parameters
        ----------
        tag : str
            Tag to identify the widget.

        Returns
        -------
        Any
            The value of the widget.
        """
        return self.elements[tag].value

    def add_label(self, tag: Optional[str] = None, value: str = ""):
        """**@unified** - Add a label/header to the GUI.

        Prints a formatted label with horizontal separators in the terminal.
        This is useful for organizing sections in your terminal GUI.

        Parameters
        ----------
        tag : str, optional
            Tag to identify the widget. If None, auto-generates a tag.
        value : str, optional
            The label text to display. Defaults to "".

        Examples
        --------
        >>> gui.add_label(value="Configuration")
        ----------------
        Configuration
        ----------------
        """
        self._nLabels += 1
        if tag is None:
            tag = f"label_{self._nLabels}"
        self.cfg[tag] = value
        self.elements[tag] = Element(self.cfg[tag])
        print("-" * len(value))
        print(value)
        print("-" * len(value))

    def add_text(
        self,
        tag: str,
        description: str,
        placeholder: str = "",
        *args,
        remember_value=True,
        **kwargs,
    ) -> str:
        """**@unified** - Add a text input prompt to the GUI.

        Creates a single-line text input that prompts the user for text entry.
        The value is automatically remembered between sessions if enabled.

        Parameters
        ----------
        tag : str
            Unique identifier for this widget.
        description : str
            The prompt message displayed to the user.
        placeholder : str, optional
            Placeholder text shown when the input is empty. Default is "".
        remember_value : bool, optional
            If True, remembers and restores the last entered value.
            Default is True.
        value : str, optional
            Initial value for the text field (passed via kwargs).
        *args : tuple
            Additional positional arguments for `prompt_toolkit.prompt`.
        **kwargs : dict
            Additional keyword arguments for `prompt_toolkit.prompt`.

        Returns
        -------
        Element
            An Element object containing the entered text as `.value`.

        Examples
        --------
        >>> gui = EZInputPrompt("app")
        >>> name = gui.add_text("username", "Enter username")
        >>> print(name.value)  # After user input
        """
        if "value" in kwargs:
            kwargs["default"] = kwargs.pop("value")
        if placeholder:
            kwargs["default"] = placeholder
        if remember_value and tag in self.cfg:
            kwargs["default"] = self.cfg[tag]
        if self.params is not None and tag in self.params:
            kwargs["default"] = self.params[tag]
        value = prompt(message=description + ": ", *args, **kwargs)  # type: ignore[misc]
        self.cfg[tag] = value
        self.elements[tag] = Element(self.cfg[tag])
        return self.elements[tag]

    def add_callback(
        self, tag, func, values: dict, description="Run", *args, **kwargs
    ):
        """**@unified** - Execute a callback function.

        In the terminal version, this immediately executes the provided function
        with the current widget values, then saves settings.

        Parameters
        ----------
        tag : str
            Tag to identify this callback.
        func : callable
            The function to execute. Should accept one argument (values dict).
        values : dict
            Dictionary of widget values to pass to the callback function.
        description : str, optional
            Description of the callback (not displayed in terminal). Default is "Run".
        *args : tuple
            Additional positional arguments (unused in terminal version).
        **kwargs : dict
            Additional keyword arguments (unused in terminal version).

        Examples
        --------
        >>> def process(values):
        ...     print(f"Processing {values}")
        >>> gui.add_callback("run", process, gui.get_values())
        """
        self._save_settings()
        func(values)

    def add_text_area(
        self,
        tag: str,
        description: str,
        placeholder: str = "",
        *args,
        remember_value=True,
        **kwargs,
    ) -> str:
        """**@unified** - Add a multi-line text area prompt to the GUI.

        Creates a text input prompt for multi-line text entry. In the terminal
        version, this behaves similarly to `add_text` but is intended for
        longer text inputs.

        Parameters
        ----------
        tag : str
            Unique identifier for this widget.
        description : str
            The prompt message displayed to the user.
        placeholder : str, optional
            Placeholder text shown when the input is empty. Default is "".
        remember_value : bool, optional
            If True, remembers and restores the last entered value.
            Default is True.
        value : str, optional
            Initial value for the text area (passed via kwargs).
        *args : tuple
            Additional positional arguments for `prompt_toolkit.prompt`.
        **kwargs : dict
            Additional keyword arguments for `prompt_toolkit.prompt`.

        Returns
        -------
        Element
            An Element object containing the entered text as `.value`.

        Notes
        -----
        In the terminal interface, this is functionally equivalent to `add_text`.
        The distinction is more meaningful in the Jupyter interface.
        """
        if "value" in kwargs:
            kwargs["default"] = str(kwargs.pop("value"))
        if placeholder:
            kwargs["default"] = placeholder
        if remember_value and tag in self.cfg:
            kwargs["default"] = self.cfg[tag]
        if self.params is not None and tag in self.params:
            kwargs["default"] = str(self.params[tag])
        value = prompt(message=description + ": ", *args, **kwargs)  # type: ignore[misc]
        self.cfg[tag] = value
        self.elements[tag] = Element(self.cfg[tag])
        return self.elements[tag]

    def add_float_range(
        self,
        tag: str,
        description: str,
        vmin: float,
        vmax: float,
        *args,
        remember_value=True,
        **kwargs,
    ) -> float:
        """**@unified** - Add a validated float input prompt with range constraints.

        Prompts the user for a floating-point number within a specified range.
        Input is validated to ensure it's a valid number within [vmin, vmax].

        Parameters
        ----------
        tag : str
            Unique identifier for this widget.
        description : str
            The prompt message displayed to the user.
        vmin : float
            Minimum allowed value (inclusive).
        vmax : float
            Maximum allowed value (inclusive).
        remember_value : bool, optional
            If True, remembers and restores the last entered value.
            Default is True.
        default : float, optional
            Default value to show (passed via kwargs).
        *args : tuple
            Additional positional arguments for `prompt_toolkit.prompt`.
        **kwargs : dict
            Additional keyword arguments for `prompt_toolkit.prompt`.

        Returns
        -------
        Element
            An Element object containing the float value as `.value`.

        Examples
        --------
        >>> alpha = gui.add_float_range("alpha", "Learning rate", 0.0, 1.0)
        >>> print(alpha.value)  # e.g., 0.01

        See Also
        --------
        add_int_range : Integer range input
        add_bounded_float_text : Alternative float range input
        """
        if "default" in kwargs and isinstance(kwargs["default"], int):
            kwargs["default"] = str(kwargs["default"])

        if self.params is not None:
            if tag in self.params:
                kwargs["default"] = str(self.params[tag])
        elif remember_value and tag in self.cfg:
            kwargs["default"] = str(self.cfg[tag])

        value = prompt(  # type: ignore[misc]
            *args,
            message=description + f" ({vmin}-{vmax}): ",
            validator=Validator.from_callable(
                lambda x: x.strip() != ""
                and x.replace(".", "", 1).isdigit()
                and vmin <= float(x) <= vmax,
                error_message=f"Please enter a valid number ({vmin}-{vmax}).",
                move_cursor_to_end=True,
            ),
            **kwargs,
        )
        self.cfg[tag] = float(value)
        self.elements[tag] = Element(self.cfg[tag])
        return self.elements[tag]

    def add_int_range(
        self,
        tag: str,
        description: str,
        vmin: int,
        vmax: int,
        *args,
        remember_value=True,
        **kwargs,
    ) -> int:
        """**@unified** - Add a validated integer input prompt with range constraints.

        Prompts the user for an integer within a specified range. Input is
        validated to ensure it's a valid integer within [vmin, vmax].

        Parameters
        ----------
        tag : str
            Unique identifier for this widget.
        description : str
            The prompt message displayed to the user.
        vmin : int
            Minimum allowed value (inclusive).
        vmax : int
            Maximum allowed value (inclusive).
        remember_value : bool, optional
            If True, remembers and restores the last entered value.
            Default is True.
        default : int, optional
            Default value to show (passed via kwargs).
        *args : tuple
            Additional positional arguments for `prompt_toolkit.prompt`.
        **kwargs : dict
            Additional keyword arguments for `prompt_toolkit.prompt`.

        Returns
        -------
        Element
            An Element object containing the integer value as `.value`.

        Examples
        --------
        >>> count = gui.add_int_range("count", "Number of items", 1, 100)
        >>> print(count.value)  # e.g., 42

        See Also
        --------
        add_float_range : Float range input
        add_bounded_int_text : Alternative integer range input
        """
        if "default" in kwargs and isinstance(kwargs["default"], int):
            kwargs["default"] = str(kwargs["default"])

        if self.params is not None:
            if tag in self.params:
                kwargs["default"] = str(self.params[tag])
        elif remember_value and tag in self.cfg:
            kwargs["default"] = str(self.cfg[tag])

        value = prompt(  # type: ignore[misc]
            *args,
            message=description + f" ({vmin}-{vmax}): ",
            validator=Validator.from_callable(
                lambda x: x.strip() != ""
                and x.isdigit()
                and vmin <= int(x) <= vmax,
                error_message=f"Please enter a valid number ({vmin}-{vmax}).",
                move_cursor_to_end=True,
            ),
            **kwargs,
        )
        self.cfg[tag] = int(value)
        self.elements[tag] = Element(self.cfg[tag])
        return self.elements[tag]

    def add_check(
        self,
        tag: str,
        description: str,
        *args,
        remember_value=True,
        **kwargs,
    ) -> bool:
        """**@unified** - Add a yes/no prompt to the GUI.

        Prompts the user with a yes/no question. Input is validated to ensure
        only "yes" or "no" is accepted, with autocomplete support.

        Parameters
        ----------
        tag : str
            Unique identifier for this widget.
        description : str
            The question or prompt message displayed to the user.
        remember_value : bool, optional
            If True, remembers and restores the last entered value.
            Default is True.
        value : bool, optional
            Initial value for the checkbox (passed via kwargs).
        default : bool, optional
            Alternative way to set initial value (passed via kwargs).
        *args : tuple
            Additional positional arguments for `prompt_toolkit.prompt`.
        **kwargs : dict
            Additional keyword arguments for `prompt_toolkit.prompt`.

        Returns
        -------
        Element
            An Element object containing True or False as `.value`.

        Examples
        --------
        >>> confirm = gui.add_check("confirm", "Proceed with operation")
        >>> if confirm.value:
        ...     print("Confirmed!")
        """
        if "value" in kwargs:
            val = kwargs.pop("value")
            kwargs["default"] = "yes" if val else "no"
        if "default" in kwargs and isinstance(kwargs["default"], bool):
            kwargs["default"] = "yes" if kwargs["default"] else "no"

        if remember_value and tag in self.cfg:
            if self.cfg[tag]:
                kwargs["default"] = "yes"
            else:
                kwargs["default"] = "no"
        if self.params is not None and tag in self.params:
            if self.params[tag]:
                kwargs["default"] = "yes"
            else:
                kwargs["default"] = "no"

        value = prompt(  # type: ignore[misc]
            *args,
            message=description + " (yes/no): ",
            completer=WordCompleter(["yes", "no"]),
            validator=Validator.from_callable(
                lambda x: x in ["yes", "no"],
                error_message="Please enter 'yes' or 'no'.",
                move_cursor_to_end=True,
            ),
            **kwargs,
        )
        self.cfg[tag] = value.lower() == "yes"
        self.elements[tag] = Element(self.cfg[tag])
        return self.elements[tag]

    def add_int_text(
        self,
        tag: str,
        description: str = "",
        *args,
        remember_value=True,
        **kwargs,
    ) -> int:
        """**@unified** - Add an integer input prompt to the GUI.

        Prompts the user for an integer value. Input is validated to ensure
        it's a valid integer (no range constraints).

        Parameters
        ----------
        tag : str
            Unique identifier for this widget.
        description : str, optional
            The prompt message displayed to the user. Default is "".
        remember_value : bool, optional
            If True, remembers and restores the last entered value.
            Default is True.
        value : int, optional
            Initial value (passed via kwargs).
        default : int, optional
            Alternative way to set initial value (passed via kwargs).
        *args : tuple
            Additional positional arguments for `prompt_toolkit.prompt`.
        **kwargs : dict
            Additional keyword arguments for `prompt_toolkit.prompt`.

        Returns
        -------
        Element
            An Element object containing the integer value as `.value`.

        Examples
        --------
        >>> age = gui.add_int_text("age", "Enter age")
        >>> print(age.value)  # e.g., 25

        See Also
        --------
        add_int_range : Integer input with range constraints
        add_bounded_int_text : Integer input with bounds
        """
        if "value" in kwargs:
            kwargs["default"] = str(kwargs.pop("value"))
        if "default" in kwargs and isinstance(kwargs["default"], int):
            kwargs["default"] = str(kwargs["default"])

        if remember_value and tag in self.cfg:
            kwargs["default"] = str(self.cfg[tag])
        if self.params is not None and tag in self.params:
            kwargs["default"] = str(self.params[tag])
        value = prompt(  # type: ignore[misc]
            *args,
            message=description + ": ",
            validator=Validator.from_callable(
                lambda x: x.isdigit(),
                error_message="Please enter a valid number.",
                move_cursor_to_end=True,
            ),
            **kwargs,
        )
        self.cfg[tag] = int(value)
        self.elements[tag] = Element(self.cfg[tag])
        return self.elements[tag]

    def add_bounded_int_text(
        self,
        tag: str,
        description: str,
        vmin: int,
        vmax: int,
        *args,
        remember_value=True,
        **kwargs,
    ) -> int:
        """**@unified** - Add a bounded integer input prompt to the GUI.

        Prompts the user for an integer within specified bounds. Functionally
        identical to `add_int_range` in the terminal interface.

        Parameters
        ----------
        tag : str
            Unique identifier for this widget.
        description : str
            The prompt message displayed to the user.
        vmin : int
            Minimum allowed value (inclusive).
        vmax : int
            Maximum allowed value (inclusive).
        remember_value : bool, optional
            If True, remembers and restores the last entered value.
            Default is True.
        value : int, optional
            Initial value (passed via kwargs).
        default : int, optional
            Alternative way to set initial value (passed via kwargs).
        *args : tuple
            Additional positional arguments for `prompt_toolkit.prompt`.
        **kwargs : dict
            Additional keyword arguments for `prompt_toolkit.prompt`.

        Returns
        -------
        Element
            An Element object containing the integer value as `.value`.

        See Also
        --------
        add_int_range : Identical functionality
        add_int_text : Unbounded integer input
        """
        if "value" in kwargs:
            kwargs["default"] = str(kwargs.pop("value"))
        if "default" in kwargs and isinstance(kwargs["default"], int):
            kwargs["default"] = str(kwargs["default"])

        if remember_value and tag in self.cfg:
            kwargs["default"] = str(self.cfg[tag])
        if self.params is not None and tag in self.params:
            kwargs["default"] = str(self.params[tag])

        value = prompt(  # type: ignore[misc]
            *args,
            message=description + f" ({vmin}-{vmax}): ",
            validator=Validator.from_callable(
                lambda x: x.strip() != ""
                and x.isdigit()
                and vmin <= int(x) <= vmax,
                error_message=f"Please enter a valid number ({vmin}-{vmax}).",
                move_cursor_to_end=True,
            ),
            **kwargs,
        )
        self.cfg[tag] = int(value)
        self.elements[tag] = Element(self.cfg[tag])
        return self.elements[tag]

    def add_float_text(
        self,
        tag: str,
        description: str = "",
        *args,
        remember_value=True,
        **kwargs,
    ) -> float:
        """**@unified** - Add a float input prompt to the GUI.

        Prompts the user for a floating-point value. Input is validated to
        ensure it's a valid number (no range constraints).

        Parameters
        ----------
        tag : str
            Unique identifier for this widget.
        description : str, optional
            The prompt message displayed to the user. Default is "".
        remember_value : bool, optional
            If True, remembers and restores the last entered value.
            Default is True.
        value : float, optional
            Initial value (passed via kwargs).
        default : float, optional
            Alternative way to set initial value (passed via kwargs).
        *args : tuple
            Additional positional arguments for `prompt_toolkit.prompt`.
        **kwargs : dict
            Additional keyword arguments for `prompt_toolkit.prompt`.

        Returns
        -------
        Element
            An Element object containing the float value as `.value`.

        Examples
        --------
        >>> weight = gui.add_float_text("weight", "Enter weight (kg)")
        >>> print(weight.value)  # e.g., 72.5

        See Also
        --------
        add_float_range : Float input with range constraints
        add_bounded_float_text : Float input with bounds
        """
        if "value" in kwargs:
            kwargs["default"] = str(kwargs.pop("value"))
        if "default" in kwargs and isinstance(kwargs["default"], float):
            kwargs["default"] = str(kwargs["default"])

        if remember_value and tag in self.cfg:
            kwargs["default"] = str(self.cfg[tag])
        if self.params is not None and tag in self.params:
            kwargs["default"] = str(self.params[tag])
        value = prompt(  # type: ignore[misc]
            *args,
            message=description + ": ",
            validator=Validator.from_callable(
                lambda x: x.replace(".", "", 1).isdigit(),
                error_message="Please enter a valid number.",
                move_cursor_to_end=True,
            ),
            **kwargs,
        )
        self.cfg[tag] = float(value)
        self.elements[tag] = Element(self.cfg[tag])
        return self.elements[tag]

    def add_bounded_float_text(
        self,
        tag: str,
        description: str,
        vmin: float,
        vmax: float,
        *args,
        remember_value=True,
        **kwargs,
    ) -> float:
        """**@unified** - Add a bounded float input prompt to the GUI.

        Prompts the user for a floating-point value within specified bounds.
        Functionally identical to `add_float_range` in the terminal interface.

        Parameters
        ----------
        tag : str
            Unique identifier for this widget.
        description : str
            The prompt message displayed to the user.
        vmin : float
            Minimum allowed value (inclusive).
        vmax : float
            Maximum allowed value (inclusive).
        remember_value : bool, optional
            If True, remembers and restores the last entered value.
            Default is True.
        value : float, optional
            Initial value (passed via kwargs).
        default : float or int, optional
            Alternative way to set initial value (passed via kwargs).
        *args : tuple
            Additional positional arguments for `prompt_toolkit.prompt`.
        **kwargs : dict
            Additional keyword arguments for `prompt_toolkit.prompt`.

        Returns
        -------
        Element
            An Element object containing the float value as `.value`.

        See Also
        --------
        add_float_range : Identical functionality
        add_float_text : Unbounded float input
        """
        if "value" in kwargs:
            kwargs["default"] = str(kwargs.pop("value"))
        if "default" in kwargs and isinstance(kwargs["default"], int):
            kwargs["default"] = str(kwargs["default"])

        if remember_value and tag in self.cfg:
            kwargs["default"] = str(self.cfg[tag])
        if self.params is not None and tag in self.params:
            kwargs["default"] = str(self.params[tag])

        value = prompt(  # type: ignore[misc]
            *args,
            message=description + f" ({vmin}-{vmax}): ",
            validator=Validator.from_callable(
                lambda x: x.strip() != ""
                and x.replace(".", "", 1).isdigit()
                and vmin <= float(x) <= vmax,
                error_message=f"Please enter a valid number ({vmin}-{vmax}).",
                move_cursor_to_end=True,
            ),
            **kwargs,
        )
        self.cfg[tag] = float(value)
        self.elements[tag] = Element(self.cfg[tag])
        return self.elements[tag]

    def add_dropdown(
        self,
        tag: str,
        options: list,
        description: str = "",
        *args,
        remember_value=True,
        **kwargs,
    ) -> str:
        """**@unified** - Add a dropdown selection prompt to the GUI.

        Prompts the user to select one option from a list. Features
        autocomplete and validates that the input matches one of the options.

        Parameters
        ----------
        tag : str
            Unique identifier for this widget.
        options : list
            List of valid choices for selection.
        description : str, optional
            The prompt message displayed to the user. Default is "".
        remember_value : bool, optional
            If True, remembers and restores the last selected value.
            Default is True.
        value : str, optional
            Initial selected value (passed via kwargs).
        *args : tuple
            Additional positional arguments for `prompt_toolkit.prompt`.
        **kwargs : dict
            Additional keyword arguments for `prompt_toolkit.prompt`.

        Returns
        -------
        Element
            An Element object containing the selected option as `.value`.

        Examples
        --------
        >>> method = gui.add_dropdown(
        ...     "method",
        ...     ["linear", "rbf", "poly"],
        ...     "Select interpolation method"
        ... )
        >>> print(method.value)  # e.g., "rbf"
        """
        if "value" in kwargs:
            kwargs["default"] = kwargs.pop("value")
        if remember_value and tag in self.cfg:
            kwargs["default"] = self.cfg[tag]
        if self.params is not None and tag in self.params:
            kwargs["default"] = self.params[tag]

        value = prompt(  # type: ignore[misc]
            *args,
            message=description + ": ",
            completer=WordCompleter(options),
            validator=Validator.from_callable(
                lambda x: x in options,
                error_message="Please select a valid choice from the dropdown.",
                move_cursor_to_end=True,
            ),
            **kwargs,
        )
        self.cfg[tag] = value
        self.elements[tag] = Element(self.cfg[tag])
        return self.elements[tag]

    def add_path_completer(
        self, tag: str, description: str, *args, remember_value=True, **kwargs
    ) -> Path:
        """**@prompt** - Add a file path input with autocomplete.

        Prompts the user for a file or directory path with autocomplete support.
        Validates that the entered path exists on the filesystem.

        Parameters
        ----------
        tag : str
            Unique identifier for this widget.
        description : str
            The prompt message displayed to the user.
        remember_value : bool, optional
            If True, remembers and restores the last entered path.
            Default is True.
        value : str or Path, optional
            Initial path value (passed via kwargs).
        *args : tuple
            Additional positional arguments for `prompt_toolkit.prompt`.
        **kwargs : dict
            Additional keyword arguments for `prompt_toolkit.prompt`.

        Returns
        -------
        Element
            An Element object containing the Path as `.value`.

        Notes
        -----
        This widget is specific to the terminal interface and provides
        filesystem path autocomplete. Not available in Jupyter.

        Examples
        --------
        >>> config = gui.add_path_completer("config", "Select config file")
        >>> print(config.value)  # e.g., Path('/home/user/config.yml')
        """
        if "value" in kwargs:
            kwargs["default"] = str(kwargs.pop("value"))
        if remember_value and tag in self.cfg:
            kwargs["default"] = str(self.cfg[tag])
        if self.params is not None and tag in self.params:
            kwargs["default"] = str(self.params[tag])

        value = prompt(  # type: ignore[misc]
            *args,
            message=description + ": ",
            completer=PathCompleter(),
            validator=Validator.from_callable(
                lambda x: Path(x).exists(),
                error_message="Please enter a valid path.",
                move_cursor_to_end=True,
            ),
            **kwargs,
        )
        self.cfg[tag] = Path(value)
        self.elements[tag] = Element(value)
        return self.elements[tag]

    def add_output(self, tag: str, *args, **kwargs):
        """**@unified** - Add an output widget (no-op in terminal).

        This method exists for API compatibility with the Jupyter interface
        but does nothing in the terminal version.

        Parameters
        ----------
        tag : str
            Tag to identify the widget (unused).
        *args : tuple
            Additional positional arguments (unused).
        **kwargs : dict
            Additional keyword arguments (unused).

        Notes
        -----
        In Jupyter, this creates an output widget for displaying results.
        In the terminal, output is printed directly to stdout.
        """
        pass

    def clear_elements(self):
        """**@unified** - Clear all widgets from the GUI.

        Removes all registered widgets, resetting the GUI to an empty state.
        This does not delete saved configuration files.
        """
        self.elements = {}

    def save_parameters(self, path: str):
        """**@unified** - Save current widget values to a YAML file.

        Exports all widget values to a YAML file that can be loaded later
        using `load_parameters`.

        Parameters
        ----------
        path : str
            The file path for saving parameters. If it doesn't end with '.yml',
            the filename will be auto-generated as '{title}_parameters.yml'.

        Examples
        --------
        >>> gui.save_parameters("my_params.yml")
        >>> gui.save_parameters("/path/to/")  # Saves to /path/to/{title}_parameters.yml

        See Also
        --------
        load_parameters : Load parameters from a file
        """
        if not path.endswith(".yml"):
            path += f"{self.title}_parameters.yml"
        out = {}
        for tag in self.elements:
            if hasattr(self.elements[tag], "value"):
                out[tag] = self.elements[tag].value
        with open(path, "w") as f:
            yaml.dump(out, f)

    def _save_settings(self):
        """**@unified** - Internal method to save settings automatically.

        Saves current widget values to the persistent configuration file.
        This method is called automatically and should not be called directly.

        Notes
        -----
        Configuration files are stored in `~/.ezinput/{title}.yml`.
        """
        for tag in self.elements:
            if hasattr(self.elements[tag], "value"):
                self.cfg[tag] = self.elements[tag].value
        config_file = CONFIG_PATH / f"{self.title}.yml"
        config_file.parent.mkdir(exist_ok=True)

        base_config = self._get_config(self.title)  # loads the config file
        for key, value in self.cfg.items():
            base_config[key] = value

        with open(config_file, "w") as f:
            yaml.dump(base_config, f)

    def load_parameters(self, path: str):
        """**@unified** - Load widget values from a YAML file.

        Loads parameters from a previously saved YAML file. These values
        will be used as defaults when creating widgets.

        Parameters
        ----------
        path : str
            The file path to load parameters from.

        Raises
        ------
        FileNotFoundError
            If the specified file does not exist.

        Examples
        --------
        >>> gui.load_parameters("my_params.yml")
        >>> # Widgets will now use values from the file

        See Also
        --------
        save_parameters : Save parameters to a file
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"The file {path} does not exist.")
        with open(path, "r") as f:
            params = yaml.load(f, Loader=yaml.SafeLoader)
        self.params = params

    def show(self):
        """**@unified** - Finalize and display the GUI.

        In the terminal interface, this method saves the current settings
        to the configuration file. Call this after adding all widgets and
        collecting user input.

        Notes
        -----
        Unlike the Jupyter version which displays widgets, the terminal
        version has already shown prompts as widgets were added. This
        method primarily handles cleanup and saving.
        """
        self._save_settings()

    def _get_config(self, title: Optional[str] = None) -> dict:
        """Internal method to retrieve saved configuration.

        Loads the configuration dictionary from the saved YAML file.

        Parameters
        ----------
        title : str, optional
            The GUI title to load configuration for. If None, uses self.title.

        Returns
        -------
        dict
            The configuration dictionary. Returns empty dict if no config exists.
        """

        if title is None:
            title = self.title

        config_file = CONFIG_PATH / f"{title}.yml"

        if not config_file.exists():
            return {}

        with open(config_file, "r") as f:
            return yaml.load(f, Loader=yaml.SafeLoader)

    def get_values(self) -> dict:
        """**@unified** - Get current values of all widgets.

        Returns a dictionary of all widget values, excluding label widgets.

        Returns
        -------
        dict
            Dictionary mapping widget tags to their current values.
            Label widgets (starting with 'label_') are excluded.

        Examples
        --------
        >>> values = gui.get_values()
        >>> print(values)
        {'name': 'Alice', 'age': 30, 'confirm': True}
        """
        out = {}
        for tag in self.elements:
            if tag.startswith("label_"):
                pass
            elif hasattr(self.elements[tag], "value"):
                out[tag] = self.elements[tag].value
        return out

    def restore_defaults(self):
        """**@unified** - Restore all widgets to their default values.

        Deletes the memory file, restoring the values to the defaults setup by the developer.
        Requires rerunning the GUI to take effect. Does not affect saved configuration files.

        Examples
        --------
        >>> gui.restore_defaults()
        """
        config_file = CONFIG_PATH / f"{self.title}.yml"
        if config_file.exists():
            try:
                os.remove(config_file)
            except OSError as e:
                print(f"Failed to remove {config_file}: {e}")
        self.cfg = {}
