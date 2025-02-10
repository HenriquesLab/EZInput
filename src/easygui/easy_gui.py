import os
import yaml
import ipywidgets as widgets

from pathlib import Path
from typing import Optional
from ipyfilechooser import FileChooser
from IPython.display import display, clear_output

from .easy_gui_jupyter import EasyGUIJupyter
from .easy_gui_prompt import EasyGUIPrompt


"""
A module to help simplify the create of GUIs in Jupyter notebooks using ipywidgets.
"""

CONFIG_PATH = Path.home() / ".config" / "easy_gui"

if not os.path.exists(CONFIG_PATH):
    os.makedirs(CONFIG_PATH)


def get_config(title: Optional[str]):
    """
    Get the configuration dictionary without needing to initialize the GUI.

    Args:
        title (str): Title of the GUI. If None, returns the entire configuration dictionary.

    Returns:
        dict: The configuration dictionary.
    """

    config_file = CONFIG_PATH / f"{title}.yml"

    if not config_file.exists():
        return {}

    with open(config_file, "r") as f:
        cfg = yaml.load(f, Loader=yaml.SafeLoader)

    if title is None:
        return cfg
    elif title in cfg:
        return cfg[title]
    else:
        return {}


def save_config(title: str, cfg: dict):
    """
    Save the configuration dictionary to a file.

    Args:
        title (str): Title of the GUI.
        cfg (dict): Configuration dictionary.
    """
    config_file = CONFIG_PATH / f"{title}.yml"
    config_file.parent.mkdir(exist_ok=True)

    base_config = get_config(None)  # loads the config file
    base_config[title] = cfg

    with open(config_file, "w") as f:
        yaml.dump(base_config, f)


class EasyGUI:
    def __init__(
        self, title: str = "base", mode="jupyter", width: str = "50%"
    ):
        if mode == "jupyter":
            self.__class__ = EasyGUIJupyter
            """
            Container for widgets.

            Args:
                title (str): The title of the widget container, used to store settings.
                width (str): The width of the widget container.
            """
            self._layout = widgets.Layout(width=width)
            self._style = {"description_width": "initial"}
            self._widgets = {}
            self._nLabels = 0
            self._main_display = widgets.VBox()
            self._title = title
            self._cfg = get_config(title)
            self.__class__ = EasyGUIJupyter

        elif mode == "prompt":
            """
            Initialize the GUI.

            Args:
                title (str): Title of the GUI.
            """
            self.title = title
            self.cfg = get_config(title)
            self.__class__ = EasyGUIPrompt
        else:
            raise ValueError(
                "Invalid mode. Must be either 'jupyter' or 'prompt'."
            )

    def __getitem__(self, tag: str) -> widgets.Widget:
        """
        Get a widget by tag.

        Args:
            tag (str): The tag of the widget.

        Returns:
            widgets.Widget: The widget.
        """
        return self._widgets[tag]

    def __len__(self) -> int:
        """
        Get the number of widgets.

        Returns:
            int: The number of widgets.
        """
        return len(self._widgets)

    def __getvalue__(self, tag: str):
        """
        Get the value of a widget.

        Args:
            tag (str): Tag to identify the widget.

        Returns:
            Any: The value of the widget.
        """
        return self.cfg[tag]
