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

CONFIG_PATH = Path.home() / ".config" / "easy_gui"

if not os.path.exists(CONFIG_PATH):
    os.makedirs(CONFIG_PATH)


def get_config(title: Optional[str]) -> dict:
    """
    Get the configuration dictionary without needing to initialize the GUI.

    Args:
        title (str): The title of the GUI. If None, returns the entire configuration.

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
    Save the configuration dictionary to file.

    Args:
        title (str): The title of the GUI.
        cfg (dict): The configuration dictionary.
    """
    config_file = CONFIG_PATH / f"{title}.yml"
    config_file.parent.mkdir(exist_ok=True)

    base_config = get_config(title)  # loads the config file
    base_config[title] = cfg

    with open(config_file, "w") as f:
        yaml.dump(base_config, f)


class EasyGUIJupyter:
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
        self._layout = widgets.Layout(width=width)
        self._style = {"description_width": "initial"}
        self._widgets = {}
        self._nLabels = 0
        self._main_display = widgets.VBox()
        self._title = title
        self._cfg = get_config(title)

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

    def add_label(self, *args, **kwargs):
        """
        Add a label widget to the container.

        Args:
            args: Args for the widget.
            kwargs: Kwargs for the widget.
        """
        self._nLabels += 1
        self._widgets[f"label_{self._nLabels}"] = widgets.Label(
            *args, **kwargs, layout=self._layout, style=self._style
        )

    def add_button(self, tag, *args, **kwargs):
        """
        Add a button widget to the container.

        Args:
            tag (str): The tag to identify the widget.
            args: Args for the widget.
            kwargs: Kwargs for the widget.
        """
        self._widgets[tag] = widgets.Button(
            *args, **kwargs, layout=self._layout, style=self._style
        )

    def add_text(self, tag, *args, remember_value=False, **kwargs):
        """
        Add a text widget to the container.

        Args:
            tag (str): The tag to identify the widget.
            args: Args for the widget.
            remember_value (bool): Remember the last value.
            kwargs: Kwargs for the widget.

        Example:
            The following example demonstrates how to add a text widget to the GUI:

            >>> gui = EasyGUI()
            >>> gui.add_text("text", "Enter some text:")
            >>> gui.show()
        """
        if remember_value and tag in self._cfg:
            kwargs["value"] = str(self._cfg[tag])

        self._widgets[tag] = widgets.Text(
            *args, **kwargs, layout=self._layout, style=self._style
        )

    def add_textarea(self, tag, *args, remember_value=False, **kwargs):
        """
        Add a textarea widget to the container.

        Args:
            tag (str): The tag to identify the widget.
            args: Args for the widget.
            remember_value (bool): Remember the last value.
            kwargs: Kwargs for the widget.
        """
        if remember_value and tag in self._cfg:
            kwargs["value"] = str(self._cfg[tag])
        self._widgets[tag] = widgets.Textarea(
            *args, **kwargs, layout=self._layout, style=self._style
        )

        self._widgets[tag] = widgets.Textarea(
            *args, **kwargs, layout=self._layout, style=self._style
        )

    def add_int_slider(self, tag, *args, remember_value=False, **kwargs):
        """
        Add a integer slider widget to the container.

        Args:
            tag (str): The tag to identify the widget.
            args: Args for the widget.
            remember_value (bool): Remember the last value.
            kwargs: Kwargs for the widget.
        """
        if (
            remember_value
            and tag in self._cfg
            and kwargs["min"] <= self._cfg[tag] <= kwargs["max"]
        ):
            kwargs["value"] = int(self._cfg[tag])
        self._widgets[tag] = widgets.IntSlider(
            *args, **kwargs, layout=self._layout, style=self._style
        )

    def add_float_slider(self, tag, *args, remember_value=False, **kwargs):
        """
        Add a float slider widget to the container.

        Args:
            tag (str): The tag to identify the widget.
            args: Args for the widget.
            remember_value (bool): Remember the last value.
            kwargs: Kwargs for the widget.
        """
        if remember_value and tag in self._cfg:
            kwargs["value"] = self._cfg[tag]
        self._widgets[tag] = widgets.FloatSlider(
            *args, **kwargs, layout=self._layout, style=self._style
        )

    def add_checkbox(self, tag, *args, remember_value=False, **kwargs):
        """
        Add a checkbox widget to the container.

        Args:
            tag (str): The tag to identify the widget.
            args: Args for the widget.
            remember_value (bool): Remember the last value.
            kwargs: Kwargs for the widget.
        """
        if remember_value and tag in self._cfg:
            kwargs["value"] = self._cfg[tag]
        self._widgets[tag] = widgets.Checkbox(
            *args, **kwargs, layout=self._layout, style=self._style
        )

    def add_int_text(self, tag, *args, remember_value=False, **kwargs):
        """
        Add a integer text widget to the container.

        Args:
            tag (str): The tag to identify the widget.
            args: Args for the widget.
            remember_value (bool): Remember the last value.
            kwargs: Kwargs for the widget.
        """
        if remember_value and tag in self._cfg:
            kwargs["value"] = self._cfg[tag]

        self._widgets[tag] = widgets.IntText(
            *args, **kwargs, layout=self._layout, style=self._style
        )

    def add_bounded_int_text(self, tag, *args, remember_value=False, **kwargs):
        """
        Add a bounded integer text widget to the container.

        Args:
            tag (str): The tag to identify the widget.
            args: Args for the widget.
            remember_value (bool): Remember the last value.
            kwargs: Kwargs for the widget.
        """
        if remember_value and tag in self._cfg:
            kwargs["value"] = self._cfg[tag]
        self._widgets[tag] = widgets.BoundedIntText(
            *args,
            **kwargs,
            layout=self._layout,
            style=self._style,
        )

    def add_float_text(self, tag, *args, remember_value=False, **kwargs):
        """
        Add a float text widget to the container.

        Args:
            tag (str): The tag to identify the widget.
            args: Args for the widget.
            remember_value (bool): Remember the last value.
            kwargs: Kwargs for the widget.
        """
        if remember_value and tag in self._cfg:
            kwargs["value"] = self._cfg[tag]
        self._widgets[tag] = widgets.FloatText(
            *args, **kwargs, layout=self._layout, style=self._style
        )

    def add_bounded_float_text(
        self, tag, *args, remember_value=False, **kwargs
    ):
        """
        Add a bounded float text widget to the container.

        Args:
            tag (str): The tag to identify the widget.
            args: Args for the widget.
            remember_value (bool): Remember the last value.
            kwargs: Kwargs for the widget.
        """
        if remember_value and tag in self._cfg:
            kwargs["value"] = self._cfg[tag]
        self._widgets[tag] = widgets.BoundedFloatText(
            *args, **kwargs, layout=self._layout, style=self._style
        )

    def add_dropdown(self, tag, *args, remember_value=False, **kwargs):
        """
        Add a dropdown widget to the container.

        Args:
            tag (str): The tag to identify the widget.
            args: Args for the widget.
            remember_value (bool): Remember the last value.
            kwargs: Kwargs for the widget.

        Example:
            >>> gui = EasyGUI()
            >>> gui.add_dropdown("dropdown", options=["A", "B", "C"])
        """
        if (
            remember_value
            and tag in self._cfg
            and self._cfg[tag] in kwargs["options"]
        ):
            kwargs["value"] = self._cfg[tag]
        self._widgets[tag] = widgets.Dropdown(
            *args, **kwargs, layout=self._layout, style=self._style
        )

    def add_file_upload(
        self, tag, *args, accept=None, multiple=False, **kwargs
    ):
        """
        Add a file upload widget to the container.

        Args:
            tag (str): The tag to identify the widget.
            args: Args for the widget.
            accept: The file types to accept.
            multiple (bool): Allow multiple files to be uploaded.
            kwargs: Kwargs for the widget.
        """
        self._widgets[tag] = FileChooser()
        if accept is not None:
            self._widgets[tag].filter_pattern = accept

    def save_settings(self):
        """
        Save the widget values to the configuration file.
        """
        for tag in self._widgets:
            if tag.startswith("label_"):
                pass
            elif hasattr(self._widgets[tag], "value"):
                self._cfg[tag] = self._widgets[tag].value

        save_config(self._title, self._cfg)

    def restore_default_settings(self):
        """
        Restore the default settings and clear the widgets.
        """
        save_config(self._title, {})
        self.clear()
        self.show()

    def show(self):
        """
        Show the widgets in the container.
        """
        self._main_display.children = tuple(self._widgets.values())
        clear_output()
        display(self._main_display)

    def clear(self):
        """
        Clear the widgets in the container.
        """
        self._widgets = {}
        self._nLabels = 0
        self._main_display.children = ()
