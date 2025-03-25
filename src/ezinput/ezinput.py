import os
import yaml
import ipywidgets as widgets

from pathlib import Path
from typing import Optional
from ipyfilechooser import FileChooser
from IPython.display import display, clear_output

from .ezinput_jupyter import EZInputJupyter
from .ezinput_prompt import EZInputPrompt


"""
A module to help simplify the create of GUIs in Jupyter notebooks using ipywidgets.
"""

CONFIG_PATH = Path.home() / ".config" / "ezgui4jupyter"

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


class EZInput:
    def __init__(self, title: str = "base", mode="prompt", width: str = "50%"):
        """
        Initializes an instance of the EZInput class.
        Args:
            title (str): The title of the input interface. Defaults to "base".
            mode (str): The mode of the input interface. Can be either "jupyter" or "prompt". Defaults to "prompt".
            width (str): The width of the input interface layout. Defaults to "50%".
        """
        
            self._layout = widgets.Layout(width=width)
            self._style = {"description_width": "initial"}
            self._widgets = {}
            self._nLabels = 0
            self._main_display = widgets.VBox()
            self._title = title
            self._cfg = get_config(title)
            self.__class__ = EZInputJupyter

        elif mode == "prompt":
            self.title = title
            self.cfg = get_config(title)
            self.__class__ = EZInputPrompt
        else:
            raise ValueError(
                "Invalid mode. Must be either 'jupyter' or 'prompt'."
            )

