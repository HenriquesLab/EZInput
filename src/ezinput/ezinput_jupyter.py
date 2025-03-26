import os
import yaml
from ipyfilechooser import FileChooser
import ipywidgets as widgets
from IPython.display import display, clear_output
from pathlib import Path

from typing import Optional

"""
A module to help simplify the create of GUIs in Jupyter notebooks using ipywidgets.
"""

CONFIG_PATH = Path.home() / ".config" / "ezinput"

if not os.path.exists(CONFIG_PATH):
    os.makedirs(CONFIG_PATH)


class EZInputJupyter:
    """
    A class to help simplify the creation of GUIs in Jupyter notebooks using ipywidgets.
    """

    def __init__(self, title="basic_gui", width="50%"):
        """
        Container for widgets.

        Args:
            title (str): The title of the widget container, used to store settings.
            width (str): The width of the widget container.
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

    def __getitem__(self, tag: str) -> widgets.Widget:
        """
        @jupyter
        Get a widget by tag.

        Args:
            tag (str): The tag of the widget.

        Returns:
            widgets.Widget: The widget.
        """
        return self.elements[tag]

    def __len__(self) -> int:
        """
        @jupyter
        Get the number of widgets.

        Returns:
            int: The number of widgets.
        """
        return len(self.elements)

    def add_label(self, tag, label="", *args, **kwargs):
        """
        @unified
        Add a label widget to the container.

        Args:
            args: Args for the widget.
            kwargs: Kwargs for the widget.
        """
        self._nLabels += 1
        self.elements[tag] = widgets.Label(
            value=label,
            *args,
            **kwargs,
            layout=self._layout,
            style=self._style,
        )

    def add_text(
        self,
        tag: str,
        description: str = "",
        placeholder: str = "",
        *args,
        remember_value=False,
        **kwargs,
    ):
        """
        @unified
        Add a text widget to the container.

        Args:
            tag (str): The tag to identify the widget.
            args: Args for the widget.
            remember_value (bool): Remember the last value.
            kwargs: Kwargs for the widget.

        Example:
            The following example demonstrates how to add a text widget to the GUI:

            >>> gui = EZGUI()
            >>> gui.add_text("text", "Enter some text:")
            >>> gui.show()
        """
        if remember_value and tag in self.cfg:
            kwargs["value"] = str(self.cfg[tag])

        self.elements[tag] = widgets.Text(
            description=description,
            placeholder=placeholder,
            *args,
            **kwargs,
            layout=self._layout,
            style=self._style,
        )

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
        self.elements[tag] = widgets.Button(
            description=description,
            *args,
            **kwargs,
            layout=self._layout,
            style=self._style,
        )

        def wrapped(button):
            func(values)

        self.elements[tag].on_click(wrapped)

    def add_button(self, tag, label="Run", *args, **kwargs):
        """
        @jupyter
        Add a button widget to the container.

        Args:
            tag (str): The tag to identify the widget.
            args: Args for the widget.
            kwargs: Kwargs for the widget.
        """
        self.elements[tag] = widgets.Button(
            *args, **kwargs, layout=self._layout, style=self._style
        )

    def add_text_area(
        self,
        tag: str,
        description: str = "",
        placeholder: str = "",
        *args,
        remember_value=False,
        **kwargs,
    ):
        """
        @unified
        Add a textarea widget to the container.

        Args:
            tag (str): The tag to identify the widget.
            args: Args for the widget.
            remember_value (bool): Remember the last value.
            kwargs: Kwargs for the widget.
        """
        if remember_value and tag in self.cfg:
            kwargs["value"] = str(self.cfg[tag])
        self.elements[tag] = widgets.Textarea(
            description=description,
            placeholder=placeholder,
            *args,
            **kwargs,
            layout=self._layout,
            style=self._style,
        )

    def add_int_range(
        self,
        tag: str,
        description: str,
        vmin: int,
        vmax: int,
        *args,
        remember_value=False,
        **kwargs,
    ):
        """
        @unified
        Add a integer slider widget to the container.

        Args:
            tag (str): The tag to identify the widget.
            args: Args for the widget.
            remember_value (bool): Remember the last value.
            kwargs: Kwargs for the widget.
        """
        if remember_value and tag in self.cfg and min <= self.cfg[tag] <= max:
            kwargs["value"] = int(self.cfg[tag])
        self.elements[tag] = widgets.IntSlider(
            description=description,
            min=vmin,
            max=vmax,
            *args,
            **kwargs,
            layout=self._layout,
            style=self._style,
        )

    def add_float_range(
        self,
        tag: str,
        description: str,
        vmin: float,
        vmax: float,
        *args,
        remember_value=False,
        **kwargs,
    ):
        """
        @unified
        Add a integer slider widget to the container.

        Args:
            tag (str): The tag to identify the widget.
            args: Args for the widget.
            remember_value (bool): Remember the last value.
            kwargs: Kwargs for the widget.
        """
        if remember_value and tag in self.cfg and min <= self.cfg[tag] <= max:
            kwargs["value"] = int(self.cfg[tag])
        self.elements[tag] = widgets.FloatSlider(
            description=description,
            min=vmin,
            max=vmax,
            *args,
            **kwargs,
            layout=self._layout,
            style=self._style,
        )

    def add_check(
        self, tag: str, description: str, *args, remember_value=False, **kwargs
    ):
        """
        Add a checkbox widget to the container.

        Args:
            tag (str): The tag to identify the widget.
            args: Args for the widget.
            remember_value (bool): Remember the last value.
            kwargs: Kwargs for the widget.
        """
        if remember_value and tag in self.cfg:
            kwargs["value"] = self.cfg[tag]
        self.elements[tag] = widgets.Checkbox(
            description=description,
            *args,
            **kwargs,
            layout=self._layout,
            style=self._style,
        )

    def add_int_text(
        self, tag, description: str = "", *args, remember_value=False, **kwargs
    ):
        """
        Add a integer text widget to the container.

        Args:
            tag (str): The tag to identify the widget.
            args: Args for the widget.
            remember_value (bool): Remember the last value.
            kwargs: Kwargs for the widget.
        """
        if remember_value and tag in self.cfg:
            kwargs["value"] = self.cfg[tag]

        self.elements[tag] = widgets.IntText(
            description=description,
            *args,
            **kwargs,
            layout=self._layout,
            style=self._style,
        )

    def add_bounded_int_text(
        self,
        tag,
        description: str,
        vmin: int,
        vmax: int,
        *args,
        remember_value=False,
        **kwargs,
    ):
        """
        Add a bounded integer text widget to the container.

        Args:
            tag (str): The tag to identify the widget.
            args: Args for the widget.
            remember_value (bool): Remember the last value.
            kwargs: Kwargs for the widget.
        """
        if remember_value and tag in self.cfg:
            kwargs["value"] = self.cfg[tag]
        self.elements[tag] = widgets.BoundedIntText(
            min=vmin,
            max=vmax,
            description=description,
            *args,
            **kwargs,
            layout=self._layout,
            style=self._style,
        )

    def add_float_text(
        self, tag, description: str = "", *args, remember_value=False, **kwargs
    ):
        """
        Add a float text widget to the container.

        Args:
            tag (str): The tag to identify the widget.
            args: Args for the widget.
            remember_value (bool): Remember the last value.
            kwargs: Kwargs for the widget.
        """
        if remember_value and tag in self.cfg:
            kwargs["value"] = self.cfg[tag]
        self.elements[tag] = widgets.FloatText(
            description=description,
            *args,
            **kwargs,
            layout=self._layout,
            style=self._style,
        )

    def add_bounded_float_text(
        self,
        tag,
        description: str,
        vmin: int,
        vmax: int,
        *args,
        remember_value=False,
        **kwargs,
    ):
        """
        Add a bounded float text widget to the container.

        Args:
            tag (str): The tag to identify the widget.
            args: Args for the widget.
            remember_value (bool): Remember the last value.
            kwargs: Kwargs for the widget.
        """
        if remember_value and tag in self.cfg:
            kwargs["value"] = self.cfg[tag]
        self.elements[tag] = widgets.BoundedFloatText(
            min=vmin,
            max=vmax,
            description=description,
            *args,
            **kwargs,
            layout=self._layout,
            style=self._style,
        )

    def add_dropdown(
        self,
        tag,
        options: list,
        description: str = "",
        *args,
        remember_value=False,
        **kwargs,
    ):
        """
        @unified
        Add a dropdown widget to the container.

        Args:
            tag (str): The tag to identify the widget.
            args: Args for the widget.
            remember_value (bool): Remember the last value.
            kwargs: Kwargs for the widget.

        Example:
            >>> gui = EZGUI()
            >>> gui.add_dropdown("dropdown", options=["A", "B", "C"])
        """
        print(self.cfg)
        if remember_value and tag in self.cfg and self.cfg[tag] in options:
            print(self.cfg[tag])
            kwargs["value"] = self.cfg[tag]
            print(kwargs["value"])
        self.elements[tag] = widgets.Dropdown(
            options=options,
            description=description,
            *args,
            **kwargs,
            layout=self._layout,
            style=self._style,
        )

    def add_file_upload(
        self, tag, *args, accept=None, multiple=False, **kwargs
    ):
        """
        @jupyter
        Add a file upload widget to the container.

        Args:
            tag (str): The tag to identify the widget.
            args: Args for the widget.
            accept: The file types to accept.
            multiple (bool): Allow multiple files to be uploaded.
            kwargs: Kwargs for the widget.
        """
        self.elements[tag] = FileChooser()
        if accept is not None:
            self.elements[tag].filter_pattern = accept

    def save_settings(self):
        """
        @unified
        Save the widget values to the configuration file.
        """
        print(self.elements.keys())
        for tag in self.elements:
            if tag.startswith("label_"):
                pass
            elif hasattr(self.elements[tag], "value"):
                self.cfg[tag] = self.elements[tag].value
        save_config(self.title, self.cfg)

    def show(self):
        """
        @unified
        Show the widgets in the container.
        """
        self._main_display.children = tuple(self.elements.values())
        clear_output()
        display(self._main_display)

    def clear_elements(self):
        """
        @unified
        Clear the widgets in the container.
        """
        self.elements = {}
        self._nLabels = 0
        self._main_display.children = ()


def get_config(title: Optional[str]) -> dict:
    """
    Get the configuration dictionary without needing to initialize the GUI.

    Args:
        title (str): The title of the GUI. If None, returns the entire configuration.

    Returns:
        dict: The configuration dictionary.
    """

    config_file = CONFIG_PATH / f"{title}_jupyter.yml"

    if not config_file.exists():
        return {}

    with open(config_file, "r") as f:
        cfg = yaml.load(f, Loader=yaml.SafeLoader)

    return cfg


def save_config(title: str, cfg: dict):
    """
    Save the configuration dictionary to file.

    Args:
        title (str): The title of the GUI.
        cfg (dict): The configuration dictionary.
    """
    config_file = CONFIG_PATH / f"{title}_jupyter.yml"
    config_file.parent.mkdir(exist_ok=True)

    base_config = get_config(title)  # loads the config file
    for key, value in cfg.items():
        base_config[key] = value

    with open(config_file, "w") as f:
        yaml.dump(base_config, f)
