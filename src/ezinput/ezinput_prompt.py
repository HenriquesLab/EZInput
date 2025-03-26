import os
import yaml
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter, PathCompleter
from prompt_toolkit.validation import Validator
from pathlib import Path

from typing import Optional

"""
A module to help simplify the create of GUIs in terminals using python prompt-toolkit.
"""


CONFIG_PATH = Path.home() / ".config" / "ezinput"

if not os.path.exists(CONFIG_PATH):
    os.makedirs(CONFIG_PATH)


class Element:
    def __init__(self, value):
        self.value = value


class EZInputPrompt:
    def __init__(self, title: str):
        """
        Initialize the GUI.

        Args:
            title (str): Title of the GUI.
        """
        pass

    def __getvalue__(self, tag: str):
        """
        @unified
        Get the value of a widget.

        Args:
            tag (str): Tag to identify the widget.

        Returns:
            Any: The value of the widget.
        """
        return self.elements[tag].value

    def add_label(self, tag: str, label: str):
        """
        @unified
        Add a header to the GUI.

        Args:
            message (str): The message to display.
        """
        self.cfg[tag] = label
        self.elements[tag] = Element(self.cfg[tag])
        print("-" * len(label))
        print(label)
        print("-" * len(label))

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

        Args:
            tag (str): Tag to identify the widget.
            message (str): The message to display.
            remember_value (bool, optional): Remember the last value. Defaults to False.

        Returns:
            str: The text entered.
        """
        if placeholder:
            kwargs["default"] = placeholder
        if remember_value and tag in self.cfg:
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

        Args:
            tag (str): The tag to identify the widget.
            func: The function to call when the button is clicked.
            label (str): The label for the button.
            funcargs (dict): The arguments to pass to the function.
            args: Args for the widget.
            kwargs: Kwargs for the widget.
        """
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
        Add a text prompt to the GUI.

        Args:
            tag (str): Tag to identify the widget.
            message (str): The message to display.
            remember_value (bool, optional): Remember the last value. Defaults to False.

        Returns:
            str: The text entered.
        """
        if placeholder:
            kwargs["default"] = placeholder
        if remember_value and tag in self.cfg:
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
        Add an integer range to the GUI.

        Args:
            tag (str): Tag to identify the widget.
            message (str): The message to display.
            vmin (int): Minimum value of the range.
            vmax (int): Maximum value of the range.
            remember_value (bool, optional): Remember the last value. Defaults to False.

        Returns:
            int: The integer entered.
        """
        if "default" in kwargs and isinstance(kwargs["default"], int):
            kwargs["default"] = str(kwargs["default"])

        if remember_value and tag in self.cfg:
            kwargs["default"] = str(self.cfg[tag])

        value = prompt(  # type: ignore[misc]
            *args,
            message=description + f" ({vmin}-{vmax}): ",
            validator=Validator.from_callable(
                lambda x: vmin <= float(x) <= vmax,
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
        Add an integer range to the GUI.

        Args:
            tag (str): Tag to identify the widget.
            message (str): The message to display.
            vmin (int): Minimum value of the range.
            vmax (int): Maximum value of the range.
            remember_value (bool, optional): Remember the last value. Defaults to False.

        Returns:
            int: The integer entered.
        """
        if "default" in kwargs and isinstance(kwargs["default"], int):
            kwargs["default"] = str(kwargs["default"])

        if remember_value and tag in self.cfg:
            kwargs["default"] = str(self.cfg[tag])

        value = prompt(  # type: ignore[misc]
            *args,
            message=description + f" ({vmin}-{vmax}): ",
            validator=Validator.from_callable(
                lambda x: vmin <= int(x) <= vmax,
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

        Args:
            tag (str): Tag to identify the widget.
            message (str): The message to display.
            remember_value (bool, optional): Remember the last value. Defaults to False.

        Returns:
            bool: True if yes, False if no.
        """
        if "default" in kwargs and isinstance(kwargs["default"], bool):
            kwargs["default"] = "yes" if kwargs["default"] else "no"

        if remember_value and tag in self.cfg:
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

        Args:
            tag (str): Tag to identify the widget.
            message (str): The message to display.
            remember_value (bool, optional): Remember the last value. Defaults to False.

        Returns:
            int: The integer entered.
        """
        if "default" in kwargs and isinstance(kwargs["default"], int):
            kwargs["default"] = str(kwargs["default"])

        if remember_value and tag in self.cfg:
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
        Add an integer range to the GUI.

        Args:
            tag (str): Tag to identify the widget.
            message (str): The message to display.
            vmin (int): Minimum value of the range.
            vmax (int): Maximum value of the range.
            remember_value (bool, optional): Remember the last value. Defaults to False.

        Returns:
            int: The integer entered.
        """
        if "default" in kwargs and isinstance(kwargs["default"], int):
            kwargs["default"] = str(kwargs["default"])

        if remember_value and tag in self.cfg:
            kwargs["default"] = str(self.cfg[tag])

        value = prompt(  # type: ignore[misc]
            *args,
            message=description + f" ({vmin}-{vmax}): ",
            validator=Validator.from_callable(
                lambda x: vmin <= int(x) <= vmax,
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

        Args:
            tag (str): Tag to identify the widget.
            message (str): The message to display.
            remember_value (bool, optional): Remember the last value. Defaults to False.

        Returns:
            int: The integer entered.
        """
        if "default" in kwargs and isinstance(kwargs["default"], float):
            kwargs["default"] = str(kwargs["default"])

        if remember_value and tag in self.cfg:
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
        Add an integer range to the GUI.

        Args:
            tag (str): Tag to identify the widget.
            message (str): The message to display.
            vmin (int): Minimum value of the range.
            vmax (int): Maximum value of the range.
            remember_value (bool, optional): Remember the last value. Defaults to False.

        Returns:
            int: The integer entered.
        """
        if "default" in kwargs and isinstance(kwargs["default"], int):
            kwargs["default"] = str(kwargs["default"])

        if remember_value and tag in self.cfg:
            kwargs["default"] = str(self.cfg[tag])

        value = prompt(  # type: ignore[misc]
            *args,
            message=description + f" ({vmin}-{vmax}): ",
            validator=Validator.from_callable(
                lambda x: vmin <= float(x) <= vmax,
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
        Add a dropdown prompt to the GUI.

        Args:
            tag (str): Tag to identify the widget.
            message (str): The message to display.
            choices (list): List of choices for the dropdown.
            remember_value (bool, optional): Remember the last value. Defaults to False.

        Returns:
            str: The selected choice.
        """
        if remember_value and tag in self.cfg:
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
        self, tag: str, message: str, *args, remember_value=False, **kwargs
    ) -> Path:
        """
        @prompt
        Add a path completer to the GUI.

        Args:
            tag (str): Tag to identify the widget.
            message (str): The message to display.
            remember_value (bool, optional): Remember the last value. Defaults to False.

        Returns:
            Path: The path entered.
        """
        if remember_value and tag in self.cfg:
            kwargs["default"] = str(self.cfg[tag])

        value = prompt(  # type: ignore[misc]
            *args,
            message=message + ": ",
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

    def show(self):
        """
        @unified
        Does nothing, just enables full copy-pasting
        """
        pass

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
        save_config(self.title, self.cfg)


def get_config(title: Optional[str]):
    """
    Get the configuration dictionary without needing to initialize the GUI.

    Args:
        title (str): Title of the GUI. If None, returns the entire configuration dictionary.

    Returns:
        dict: The configuration dictionary.
    """

    config_file = CONFIG_PATH / f"{title}_prompt.yml"

    if not config_file.exists():
        return {}

    with open(config_file, "r") as f:
        cfg = yaml.load(f, Loader=yaml.SafeLoader)

    return cfg


def save_config(title: str, cfg: dict):
    """
    Save the configuration dictionary to a file.

    Args:
        title (str): Title of the GUI.
        cfg (dict): Configuration dictionary.
    """
    config_file = CONFIG_PATH / f"{title}_prompt.yml"
    config_file.parent.mkdir(exist_ok=True)

    base_config = get_config(title)  # loads the config file
    for key, value in cfg.items():
        base_config[key] = value

    with open(config_file, "w") as f:
        yaml.dump(base_config, f)
