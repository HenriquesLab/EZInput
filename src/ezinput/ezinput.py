import os
import sys
import yaml
import ipywidgets as widgets

from pathlib import Path
from typing import Optional

from .ezinput_prompt import EZInputPrompt
from .ezinput_jupyter import EZInputJupyter

try:
    from google.colab import output

    output.enable_custom_widget_manager()
except ImportError:
    pass

"""
A module to help simplify the create of GUIs in Jupyter notebooks and CLIs.
"""

CONFIG_PATH = Path.home() / ".ezinput"

if not os.path.exists(CONFIG_PATH):
    os.makedirs(CONFIG_PATH)


class EZInput:
    def __init__(
        self,
        title: str = "base",
        width: str = "50%",
        mode=None,
        params_file: Optional[str] = None,
    ):
        """
        Initializes an instance of the EZInput class.
        Args:
            title (str): The title of the input interface. Defaults to "base".
            width (str): The width of the input interface layout. Defaults to "50%".
        """

        self.title = title
        self.mode = None
        self._nLabels = 0
        self.cfg = self._get_config(title)
        if params_file is not None:
            self.params = self._load_params(params_file)
            print(self.params)
        else:
            self.params = None
        self.elements = {}

        if mode is None:
            self._detect_env(width)

    def _load_params(self, params_file: Optional[str] = None):
        """
        Loads parameters from a YAML file.
        Args:
            params_file (str): The path to the YAML file containing parameters.
        """
        if os.path.exists(params_file):
            with open(params_file, "r") as stream:
                return yaml.safe_load(stream)
        else:
            return None

    def _get_config(self, title: Optional[str] = None) -> dict:
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

        if title is None:
            title = self.title

        config_file = CONFIG_PATH / f"{title}.yml"

        if not config_file.exists():
            return {}

        with open(config_file, "r") as f:
            return yaml.load(f, Loader=yaml.SafeLoader)

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

    def _save_config(self, title: str, cfg: dict):
        """
        @unified
        Save the configuration dictionary to file.

        Parameters
        ----------
        title : str
            The title of the GUI.
        cfg : dict
            The configuration dictionary.
        """
        config_file = CONFIG_PATH / f"{title}.yml"
        config_file.parent.mkdir(exist_ok=True)

        base_config = self._get_config(title)  # loads the config file
        for key, value in cfg.items():
            base_config[key] = value

        with open(config_file, "w") as f:
            yaml.dump(base_config, f)

    def _detect_env(self, width):
        try:
            get_ipython = sys.modules["IPython"].get_ipython
            if "IPKernelApp" in get_ipython().config:
                self._layout = widgets.Layout(width=width)
                self._style = {"description_width": "initial"}
                self._main_display = widgets.VBox()
                self.mode = "jupyter"
                self.__class__ = EZInputJupyter
            else:
                self.mode = "prompt"
                self.__class__ = EZInputPrompt
        except Exception:
            self.mode = "prompt"
            self.__class__ = EZInputPrompt
