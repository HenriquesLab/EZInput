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
    def __init__(self, value):
        self.value = value


class EZInputPrompt:
    """
    A class to create terminal-based GUIs using `prompt_toolkit`.

    Parameters
    ----------
    title : str
        Title of the GUI, used to store settings.
    """

    def __init__(self, title: str):
        """
        Initialize the GUI.

        Parameters
        ----------
        title : str
            Title of the GUI.
        """
        pass

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

    def add_label(self, value: str = ""):
        """
        @unified
        Add a header to the GUI.

        Parameters
        ----------
        tag : str
            Tag to identify the widget.
        label : str
            The label text to display.
        """
        self._nLabels += 1
        self.cfg[f"label_{self._nLabels}"] = value
        self.elements[f"label_{self._nLabels}"] = Element(
            self.cfg[f"label_{self._nLabels}"]
        )
        print("-" * len(value))
        print(value)
        print("-" * len(value))

    def add_text(
        self,
        tag: str,
        description: str,
        placeholder: str = "",
        *args,
        remember_value=False,
        **kwargs,
    ) -> str:
        """
        @unified
        Add a text prompt to the GUI.

        Parameters
        ----------
        tag : str
            Tag to identify the widget.
        description : str
            The message to display.
        placeholder : str, optional
            Placeholder text for the input field. Defaults to "".
        remember_value : bool, optional
            Whether to remember the last entered value. Defaults to False.
        *args : tuple
            Additional positional arguments for the `prompt` function.
        **kwargs : dict
            Additional keyword arguments for the `prompt` function.

        Returns
        -------
        str
            The text entered by the user.
        """
        if placeholder:
            kwargs["default"] = placeholder
        if self.params is not None:
            if tag in self.params:
                kwargs["default"] = self.params[tag]
        elif remember_value and tag in self.cfg:
            kwargs["default"] = self.cfg[tag]
        value = prompt(message=description + ": ", *args, **kwargs)  # type: ignore[misc]
        self.cfg[tag] = value
        self.elements[tag] = Element(self.cfg[tag])
        return self.elements[tag]

    def add_callback(
        self, tag, func, values: dict, description="Run", *args, **kwargs
    ):
        """
        @unified
        Add a button widget to the container.

        Parameters
        ----------
        tag : str
            Tag to identify the widget.
        func : callable
            The function to call when the button is clicked.
        values : dict
            Dictionary of widget values to pass to the callback function.
        description : str, optional
            The label for the button. Defaults to "Run".
        *args : tuple
            Additional positional arguments for the button.
        **kwargs : dict
            Additional keyword arguments for the button.
        """
        self.save_settings()
        func(values)

    def add_text_area(
        self,
        tag: str,
        description: str,
        placeholder: str = "",
        *args,
        remember_value=False,
        **kwargs,
    ) -> str:
        """
        @unified
        Add a text area prompt to the GUI.

        Parameters
        ----------
        tag : str
            Tag to identify the widget.
        description : str
            The message to display.
        placeholder : str, optional
            Placeholder text for the input field. Defaults to "".
        remember_value : bool, optional
            Whether to remember the last entered value. Defaults to False.
        *args : tuple
            Additional positional arguments for the `prompt` function.
        **kwargs : dict
            Additional keyword arguments for the `prompt` function.

        Returns
        -------
        str
            The text entered by the user.
        """
        if placeholder:
            kwargs["default"] = placeholder
        if self.params is not None:
            if tag in self.params:
                kwargs["default"] = str(self.params[tag])
        elif remember_value and tag in self.cfg:
            kwargs["default"] = self.cfg[tag]
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
        remember_value=False,
        **kwargs,
    ) -> float:
        """
        @unified
        Add a float range prompt to the GUI.

        Parameters
        ----------
        tag : str
            Tag to identify the widget.
        description : str
            The message to display.
        vmin : float
            Minimum value of the range.
        vmax : float
            Maximum value of the range.
        remember_value : bool, optional
            Whether to remember the last entered value. Defaults to False.
        *args : tuple
            Additional positional arguments for the `prompt` function.
        **kwargs : dict
            Additional keyword arguments for the `prompt` function.

        Returns
        -------
        float
            The float value entered by the user.
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
        remember_value=False,
        **kwargs,
    ) -> int:
        """
        @unified
        Add an integer range prompt to the GUI.

        Parameters
        ----------
        tag : str
            Tag to identify the widget.
        description : str
            The message to display.
        vmin : int
            Minimum value of the range.
        vmax : int
            Maximum value of the range.
        remember_value : bool, optional
            Whether to remember the last entered value. Defaults to False.
        *args : tuple
            Additional positional arguments for the `prompt` function.
        **kwargs : dict
            Additional keyword arguments for the `prompt` function.

        Returns
        -------
        int
            The integer value entered by the user.
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
        remember_value=False,
        **kwargs,
    ) -> bool:
        """
        @unified
        Add a yes/no prompt to the GUI.

        Parameters
        ----------
        tag : str
            Tag to identify the widget.
        description : str
            The message to display.
        remember_value : bool, optional
            Whether to remember the last entered value. Defaults to False.
        *args : tuple
            Additional positional arguments for the `prompt` function.
        **kwargs : dict
            Additional keyword arguments for the `prompt` function.

        Returns
        -------
        bool
            True if "yes" is selected, False otherwise.
        """
        if "default" in kwargs and isinstance(kwargs["default"], bool):
            kwargs["default"] = "yes" if kwargs["default"] else "no"

        if self.params is not None:
            if tag in self.params:
                if self.params[tag]:
                    kwargs["default"] = "yes"
                else:
                    kwargs["default"] = "no"
        elif remember_value and tag in self.cfg:
            if self.cfg[tag]:
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
        remember_value=False,
        **kwargs,
    ) -> int:
        """
        @unified
        Add an integer prompt to the GUI.

        Parameters
        ----------
        tag : str
            Tag to identify the widget.
        description : str
            The message to display.
        remember_value : bool, optional
            Whether to remember the last entered value. Defaults to False.
        *args : tuple
            Additional positional arguments for the `prompt` function.
        **kwargs : dict
            Additional keyword arguments for the `prompt` function.

        Returns
        -------
        int
            The integer value entered by the user.
        """
        print("ahhhhhhhhh")
        if "default" in kwargs and isinstance(kwargs["default"], int):
            kwargs["default"] = str(kwargs["default"])

        if self.params is not None:
            if tag in self.params:
                kwargs["default"] = str(self.params[tag])
        elif remember_value and tag in self.cfg:
            kwargs["default"] = str(self.cfg[tag])
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
        print("ahhhhhhhhh")
        return self.elements[tag]

    def add_bounded_int_text(
        self,
        tag: str,
        description: str,
        vmin: int,
        vmax: int,
        *args,
        remember_value=False,
        **kwargs,
    ) -> int:
        """
        @unified
        Add an integer range prompt to the GUI.

        Parameters
        ----------
        tag : str
            Tag to identify the widget.
        description : str
            The message to display.
        vmin : int
            Minimum value of the range.
        vmax : int
            Maximum value of the range.
        remember_value : bool, optional
            Whether to remember the last entered value. Defaults to False.
        *args : tuple
            Additional positional arguments for the `prompt` function.
        **kwargs : dict
            Additional keyword arguments for the `prompt` function.

        Returns
        -------
        int
            The integer value entered by the user.
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

    def add_float_text(
        self,
        tag: str,
        description: str = "",
        *args,
        remember_value=False,
        **kwargs,
    ) -> float:
        """
        @unified
        Add an integer prompt to the GUI.

        Parameters
        ----------
        tag : str
            Tag to identify the widget.
        description : str
            The message to display.
        remember_value : bool, optional
            Whether to remember the last entered value. Defaults to False.
        *args : tuple
            Additional positional arguments for the `prompt` function.
        **kwargs : dict
            Additional keyword arguments for the `prompt` function.

        Returns
        -------
        float
            The float value entered by the user.
        """
        if "default" in kwargs and isinstance(kwargs["default"], float):
            kwargs["default"] = str(kwargs["default"])

        if self.params is not None:
            if tag in self.params:
                kwargs["default"] = str(self.params[tag])
        elif remember_value and tag in self.cfg:
            kwargs["default"] = str(self.cfg[tag])
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
        remember_value=False,
        **kwargs,
    ) -> float:
        """
        @unified
        Add an integer range prompt to the GUI.

        Parameters
        ----------
        tag : str
            Tag to identify the widget.
        description : str
            The message to display.
        vmin : float
            Minimum value of the range.
        vmax : float
            Maximum value of the range.
        remember_value : bool, optional
            Whether to remember the last entered value. Defaults to False.
        *args : tuple
            Additional positional arguments for the `prompt` function.
        **kwargs : dict
            Additional keyword arguments for the `prompt` function.

        Returns
        -------
        float
            The float value entered by the user.
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

    def add_dropdown(
        self,
        tag: str,
        options: list,
        description: str = "",
        *args,
        remember_value=False,
        **kwargs,
    ) -> str:
        """
        @unified
        Add a dropdown prompt to the GUI.

        Parameters
        ----------
        tag : str
            Tag to identify the widget.
        description : str
            The message to display.
        options : list
            List of choices for the dropdown.
        remember_value : bool, optional
            Whether to remember the last selected value. Defaults to False.
        *args : tuple
            Additional positional arguments for the `prompt` function.
        **kwargs : dict
            Additional keyword arguments for the `prompt` function.

        Returns
        -------
        str
            The selected choice.
        """
        if self.params is not None:
            if tag in self.params:
                kwargs["default"] = self.params[tag]
        elif remember_value and tag in self.cfg:
            kwargs["default"] = self.cfg[tag]

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
        self, tag: str, description: str, *args, remember_value=False, **kwargs
    ) -> Path:
        """
        @prompt
        Add a path completer to the GUI.

        Parameters
        ----------
        tag : str
            Tag to identify the widget.
        description : str
            The message to display.
        remember_value : bool, optional
            Whether to remember the last entered path. Defaults to False.
        *args : tuple
            Additional positional arguments for the `prompt` function.
        **kwargs : dict
            Additional keyword arguments for the `prompt` function.

        Returns
        -------
        Path
            The path entered by the user.
        """
        if self.params is not None:
            if tag in self.params:
                kwargs["default"] = str(self.params[tag])
        elif remember_value and tag in self.cfg:
            kwargs["default"] = str(self.cfg[tag])

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
        self.elements[tag] = Element(self.cfg[tag])
        return self.elements[tag]

    def clear_elements(self):
        """
        @unified
        Clear all elements from the GUI.
        """
        self.elements = {}

    def save_parameters(self, path: str):
        """
        @unified
        Save the widget values to a file.

        Parameters
        ----------
        path : str
            The path to save the file.
        """
        if not path.endswith(".yml"):
            path += f"{self.title}_parameters.yml"
        out = {}
        for tag in self.elements:
            if tag.startswith("label_"):
                pass
            elif hasattr(self.elements[tag], "value"):
                out[tag] = self.elements[tag].value
        with open(path, "w") as f:
            yaml.dump(out, f)

    def save_settings(self):
        """
        @unified
        Save the widget values to the configuration file.
        """
        for tag in self.elements:
            if tag.startswith("label_"):
                pass
            elif hasattr(self.elements[tag], "value"):
                self.cfg[tag] = self.elements[tag].value
        config_file = CONFIG_PATH / f"{self.title}.yml"
        config_file.parent.mkdir(exist_ok=True)

        base_config = self._get_config(self.title)  # loads the config file
        for key, value in self.cfg.items():
            base_config[key] = value

        with open(config_file, "w") as f:
            yaml.dump(base_config, f)

    def show(self):
        """
        @unified
        Display the GUI. (No-op for terminal-based GUIs.)
        """
        pass

    def _get_config(self, title: Optional[str]) -> dict:
        """
        Get the configuration dictionary without needing to initialize the GUI.

        Parameters
        ----------
        title : str, optional
            The title of the GUI. If None, returns the entire configuration.

        Returns
        -------
        dict
            The configuration dictionary.
        """

        config_file = CONFIG_PATH / f"{title}.yml"

        if not config_file.exists():
            return {}

        with open(config_file, "r") as f:
            return yaml.load(f, Loader=yaml.SafeLoader)
