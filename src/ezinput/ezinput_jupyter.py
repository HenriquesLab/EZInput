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
    A class to create GUIs in Jupyter notebooks using `ipywidgets`.

    Parameters
    ----------
    title : str, optional
        Title of the GUI, used to store settings. Defaults to "basic_gui".
    width : str, optional
        Width of the widget container. Defaults to "50%".
    """

    def __init__(self, title="basic_gui", width="50%"):
        """
        Container for widgets.

        Parameters
        ----------
        title : str, optional
            The title of the widget container, used to store settings.
        width : str, optional
            The width of the widget container.
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

    def __getitem__(self, tag: str) -> widgets.Widget:
        """
        Get a widget by tag.

        Parameters
        ----------
        tag : str
            The tag of the widget.

        Returns
        -------
        widgets.Widget
            The widget.
        """
        return self.elements[tag]

    def __len__(self) -> int:
        """
        Get the number of widgets.

        Returns
        -------
        int
            The number of widgets.
        """
        return len(self.elements)

    def add_label(self, tag, label="", *args, **kwargs):
        """
        @unified
        Add a label widget to the container.

        Parameters
        ----------
        tag : str
            Tag to identify the widget.
        label : str, optional
            The label text to display. Defaults to "".
        *args : tuple
            Additional positional arguments for the widget.
        **kwargs : dict
            Additional keyword arguments for the widget.
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

        Parameters
        ----------
        tag : str
            Tag to identify the widget.
        description : str, optional
            The message to display. Defaults to "".
        placeholder : str, optional
            Placeholder text for the input field. Defaults to "".
        remember_value : bool, optional
            Whether to remember the last entered value. Defaults to False.
        *args : tuple
            Additional positional arguments for the widget.
        **kwargs : dict
            Additional keyword arguments for the widget.
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

        Parameters
        ----------
        tag : str
            Tag to identify the widget.
        label : str, optional
            The label for the button. Defaults to "Run".
        *args : tuple
            Additional positional arguments for the widget.
        **kwargs : dict
            Additional keyword arguments for the widget.
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

        Parameters
        ----------
        tag : str
            Tag to identify the widget.
        description : str, optional
            The message to display. Defaults to "".
        placeholder : str, optional
            Placeholder text for the input field. Defaults to "".
        remember_value : bool, optional
            Whether to remember the last entered value. Defaults to False.
        *args : tuple
            Additional positional arguments for the widget.
        **kwargs : dict
            Additional keyword arguments for the widget.
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
        Add an integer slider widget to the container.

        Parameters
        ----------
        tag : str
            Tag to identify the widget.
        description : str
            The message to display.
        vmin : int
            Minimum value of the slider.
        vmax : int
            Maximum value of the slider.
        remember_value : bool, optional
            Whether to remember the last selected value. Defaults to False.
        *args : tuple
            Additional positional arguments for the widget.
        **kwargs : dict
            Additional keyword arguments for the widget.
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
        Add a float slider widget to the container.

        Parameters
        ----------
        tag : str
            Tag to identify the widget.
        description : str
            The message to display.
        vmin : float
            Minimum value of the slider.
        vmax : float
            Maximum value of the slider.
        remember_value : bool, optional
            Whether to remember the last selected value. Defaults to False.
        *args : tuple
            Additional positional arguments for the widget.
        **kwargs : dict
            Additional keyword arguments for the widget.
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
        @unified
        Add a checkbox widget to the container.

        Parameters
        ----------
        tag : str
            Tag to identify the widget.
        description : str
            The message to display.
        remember_value : bool, optional
            Whether to remember the last selected value. Defaults to False.
        *args : tuple
            Additional positional arguments for the widget.
        **kwargs : dict
            Additional keyword arguments for the widget.
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
        @unified
        Add an integer text widget to the container.

        Parameters
        ----------
        tag : str
            Tag to identify the widget.
        description : str, optional
            The message to display. Defaults to "".
        remember_value : bool, optional
            Whether to remember the last entered value. Defaults to False.
        *args : tuple
            Additional positional arguments for the widget.
        **kwargs : dict
            Additional keyword arguments for the widget.
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
        @unified
        Add a bounded integer text widget to the container.

        Parameters
        ----------
        tag : str
            Tag to identify the widget.
        description : str
            The message to display.
        vmin : int
            Minimum value of the input field.
        vmax : int
            Maximum value of the input field.
        remember_value : bool, optional
            Whether to remember the last entered value. Defaults to False.
        *args : tuple
            Additional positional arguments for the widget.
        **kwargs : dict
            Additional keyword arguments for the widget.
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
        @unified
        Add a float text widget to the container.

        Parameters
        ----------
        tag : str
            Tag to identify the widget.
        description : str, optional
            The message to display. Defaults to "".
        remember_value : bool, optional
            Whether to remember the last entered value. Defaults to False.
        *args : tuple
            Additional positional arguments for the widget.
        **kwargs : dict
            Additional keyword arguments for the widget.
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
        @unified
        Add a bounded float text widget to the container.

        Parameters
        ----------
        tag : str
            Tag to identify the widget.
        description : str
            The message to display.
        vmin : int
            Minimum value of the input field.
        vmax : int
            Maximum value of the input field.
        remember_value : bool, optional
            Whether to remember the last entered value. Defaults to False.
        *args : tuple
            Additional positional arguments for the widget.
        **kwargs : dict
            Additional keyword arguments for the widget.
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

        Parameters
        ----------
        tag : str
            Tag to identify the widget.
        options : list
            List of choices for the dropdown.
        description : str, optional
            The message to display. Defaults to "".
        remember_value : bool, optional
            Whether to remember the last selected value. Defaults to False.
        *args : tuple
            Additional positional arguments for the widget.
        **kwargs : dict
            Additional keyword arguments for the widget.
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

        Parameters
        ----------
        tag : str
            Tag to identify the widget.
        accept : str, optional
            The file types to accept. Defaults to None.
        multiple : bool, optional
            Allow multiple files to be uploaded. Defaults to False.
        *args : tuple
            Additional positional arguments for the widget.
        **kwargs : dict
            Additional keyword arguments for the widget.
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
        Display the widgets in the container.
        """
        self._main_display.children = tuple(self.elements.values())
        clear_output()
        display(self._main_display)

    def clear_elements(self):
        """
        @unified
        Clear all widgets from the container.
        """
        self.elements = {}
        self._nLabels = 0
        self._main_display.children = ()


def get_config(title: Optional[str]) -> dict:
    """
    @unified
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

    config_file = CONFIG_PATH / f"{title}_jupyter.yml"

    if not config_file.exists():
        return {}

    with open(config_file, "r") as f:
        cfg = yaml.load(f, Loader=yaml.SafeLoader)

    return cfg


def save_config(title: str, cfg: dict):
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
    config_file = CONFIG_PATH / f"{title}_jupyter.yml"
    config_file.parent.mkdir(exist_ok=True)

    base_config = get_config(title)  # loads the config file
    for key, value in cfg.items():
        base_config[key] = value

    with open(config_file, "w") as f:
        yaml.dump(base_config, f)
