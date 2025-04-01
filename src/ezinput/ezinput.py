import os
import sys
import yaml
import ipywidgets as widgets

from pathlib import Path
from typing import Optional

from .ezinput_prompt import EZInputPrompt
from .ezinput_prompt import get_config as get_config_prompt
from .ezinput_jupyter import EZInputJupyter
from .ezinput_jupyter import get_config as get_config_jupyter

"""
A module to help simplify the create of GUIs in Jupyter notebooks and CLIs.
"""

CONFIG_PATH = Path.home() / ".config" / "ezinput"

if not os.path.exists(CONFIG_PATH):
    os.makedirs(CONFIG_PATH)


class EZInput:
    def __init__(self, title: str = "base", width: str = "50%", mode=None):
        """
        Initializes an instance of the EZInput class.
        Args:
            title (str): The title of the input interface. Defaults to "base".
            width (str): The width of the input interface layout. Defaults to "50%".
        """

        self.title = title
        self.mode = None

        if mode is None:
            self._detect_env(width)

    def _detect_env(self, width):
        try:
            get_ipython = sys.modules["IPython"].get_ipython
            if "IPKernelApp" in get_ipython().config:
                self._layout = widgets.Layout(width=width)
                self._style = {"description_width": "initial"}
                self.elements = {}
                self._nLabels = 0
                self._main_display = widgets.VBox()
                self.mode = "jupyter"
                self.cfg = get_config_jupyter(self.title)
                self.__class__ = EZInputJupyter
            else:
                self.elements = {}
                self.mode = "prompt"
                self._nLabels = 0
                self.cfg = get_config_prompt(self.title)
                self.__class__ = EZInputPrompt
        except Exception:
            self.elements = {}
            self.mode = "prompt"
            self._nLabels = 0
            self.cfg = get_config_prompt(self.title)
            self.__class__ = EZInputPrompt
