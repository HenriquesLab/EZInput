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

CONFIG_PATH = Path.home() / ".ezinput"

if not os.path.exists(CONFIG_PATH):
    os.makedirs(CONFIG_PATH)


class EZInputJupyter:
    """A class to create GUIs in Jupyter notebooks using `ipywidgets`.

    This class provides a simple interface for building interactive GUIs in
    Jupyter notebooks. Widgets are displayed in a container and settings are
    automatically saved between sessions.

    Parameters
    ----------
    title : str, optional
        Title of the GUI, used to identify the configuration file for
        storing settings. Default is "basic_gui".
    width : str, optional
        Width of the widget container (CSS format). Default is "50%".

    Examples
    --------
    >>> from ezinput import EZInputJupyter
    >>> gui = EZInputJupyter("my_notebook", width="70%")
    >>> gui.add_text("name", "Enter name:")
    >>> gui.add_int_slider("count", "Count:", min=1, max=100)
    >>> gui.show()
    """

    def __init__(self, title="basic_gui", width="50%"):
        """Initialize the Jupyter GUI container.

        Creates a new GUI instance with a widget container and loads any
        previously saved settings from the configuration file.

        Parameters
        ----------
        title : str, optional
            The title used to identify the configuration file. Default is "basic_gui".
        width : str, optional
            The CSS width specification for the widget container. Default is "50%".
        """
        self.title = title
        self.elements = {}
        self.cfg = self._get_config(title)
        self.params = None
        self._nLabels = 0
        self._layout = widgets.Layout(width=width)
        self._style = {"description_width": "initial"}
        self._main_display = widgets.VBox()

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
        """Get a widget by its tag using dictionary-style access.

        Allows accessing widgets using square bracket notation.

        Parameters
        ----------
        tag : str
            The tag identifier of the widget.

        Returns
        -------
        widgets.Widget
            The ipywidget object.

        Examples
        --------
        >>> gui['name'].value = 'Alice'
        >>> print(gui['count'].value)
        """
        return self.elements[tag]

    def __len__(self) -> int:
        """Get the number of widgets in the container.

        Returns
        -------
        int
            The count of widgets currently in the GUI.
        """
        return len(self.elements)

    def add_label(self, tag: Optional[str] = None, value="", *args, **kwargs):
        """**@unified** - Add a label widget to the container.

        Creates a non-interactive label for displaying text, useful for
        section headers or informational messages.

        Parameters
        ----------
        tag : str, optional
            Unique identifier for this widget. If None, auto-generates a tag.
        value : str, optional
            The label text to display. Default is "".
        *args : tuple
            Additional positional arguments for ipywidgets.Label.
        **kwargs : dict
            Additional keyword arguments for ipywidgets.Label.

        Examples
        --------
        >>> gui.add_label(value="Configuration Settings")
        >>> gui.add_label("header", "Input Parameters")
        """
        self._nLabels += 1
        if tag is None:
            tag = f"label_{self._nLabels}"
        style = kwargs.pop("style", self._style)
        self.elements[tag] = widgets.Label(
            value=value,
            *args,
            **kwargs,
            layout=self._layout,
            style=style,
        )

        return self.elements[tag]

    def add_text(
        self,
        tag: str,
        description: str = "",
        placeholder: str = "",
        *args,
        remember_value=True,
        **kwargs,
    ):
        """**@unified** - Add a single-line text input widget.

        Creates a text input field for short text entry with optional
        placeholder text and value persistence.

        Parameters
        ----------
        tag : str
            Unique identifier for this widget.
        description : str, optional
            Label text displayed next to the input field. Default is "".
        placeholder : str, optional
            Placeholder text shown when the field is empty. Default is "".
        remember_value : bool, optional
            If True, remembers and restores the last entered value.
            Default is True.
        value : str, optional
            Initial value for the text field (passed via kwargs).
        *args : tuple
            Additional positional arguments for ipywidgets.Text.
        **kwargs : dict
            Additional keyword arguments for ipywidgets.Text.

        Examples
        --------
        >>> gui.add_text("username", "Username:", placeholder="Enter name")
        >>> gui.add_text("email", "Email:", value="user@example.com")
        """
        if self.params is not None:
            if tag in self.params:
                kwargs["value"] = self.params[tag]
        elif remember_value and tag in self.cfg:
            kwargs["value"] = str(self.cfg[tag])

        style = kwargs.pop("style", self._style)
        self.elements[tag] = widgets.Text(
            description=description,
            placeholder=placeholder,
            continuous_update=True,
            *args,
            **kwargs,
            layout=self._layout,
            style=style,
        )

        return self.elements[tag]

    def add_callback(
        self, tag, func, values: dict, description="Run", *args, **kwargs
    ):
        """**@unified** - Add a button widget with callback function.

        Creates a clickable button that executes a callback function when
        clicked, saving settings before execution.

        Parameters
        ----------
        tag : str
            Unique identifier for this button widget.
        func : callable
            The function to execute when the button is clicked. Should accept
            one argument (the values dictionary).
        values : dict
            Dictionary of widget values to pass to the callback. Often set to
            `gui.get_values()` to pass all current values.
        description : str, optional
            The label text displayed on the button. Default is "Run".
        *args : tuple
            Additional positional arguments for ipywidgets.Button.
        **kwargs : dict
            Additional keyword arguments for ipywidgets.Button.

        Examples
        --------
        >>> def process_data(values):
        ...     print(f"Processing: {values}")
        >>> gui.add_callback("process", process_data, gui.get_values(),
        ...                  description="Process Data")
        """
        style = kwargs.pop("style", self._style)
        self.elements[tag] = widgets.Button(
            description=description,
            *args,
            **kwargs,
            layout=self._layout,
            style=style,
        )

        def wrapped(button):
            self._save_settings()
            func(values)

        self.elements[tag].on_click(wrapped)
        return self.elements[tag]

    def add_text_area(
        self,
        tag: str,
        description: str = "",
        placeholder: str = "",
        *args,
        remember_value=True,
        on_change: Optional[callable] = None,
        **kwargs,
    ):
        """**@unified** - Add a multi-line text area widget.

        Creates a textarea that allows users to enter multi-line text,
        ideal for longer text inputs like descriptions or comments.

        Parameters
        ----------
        tag : str
            Unique identifier for this widget.
        description : str, optional
            Label text displayed next to the textarea. Default is "".
        placeholder : str, optional
            Placeholder text shown when the textarea is empty. Default is "".
        remember_value : bool, optional
            If True, remembers and restores the last entered text.
            Default is True.
        on_change : callable, optional
            Callback function executed when the text changes.
            Should accept one argument (the change dictionary).
            Default is None.
        value : str, optional
            Initial text content for the textarea (passed via kwargs).
        *args : tuple
            Additional positional arguments for ipywidgets.Textarea.
        **kwargs : dict
            Additional keyword arguments for ipywidgets.Textarea.

        Notes
        -----
        Value priority (highest to lowest):
        1. Loaded parameters (if params_file was provided)
        2. Remembered value (if remember_value=True)
        3. Explicit value kwarg
        4. Empty string

        Examples
        --------
        >>> gui.add_text_area("notes", "Notes:")
        >>> gui.add_text_area("description", "Enter description:",
        ...                   placeholder="Type here...")
        """
        if remember_value and tag in self.cfg:
            kwargs["value"] = str(self.cfg[tag])
        if self.params is not None and tag in self.params:
            kwargs["value"] = self.params[tag]
        style = kwargs.pop("style", self._style)
        self.elements[tag] = widgets.Textarea(
            description=description,
            placeholder=placeholder,
            continuous_update=True,
            *args,
            **kwargs,
            layout=self._layout,
            style=style,
        )

        if on_change is not None:
            self.elements[tag].observe(on_change, names="value")

        return self.elements[tag]

    def add_HTML(
        self, tag: str, value: str, description: str = "", *args, **kwargs
    ):
        """**@jupyter** - Add an HTML widget to display rich content.

        Creates a widget that renders HTML content, enabling rich text
        formatting, links, images, and styled content in the GUI.

        Parameters
        ----------
        tag : str
            Unique identifier for this widget.
        value : str
            HTML content to display. Can include any valid HTML markup.
        description : str, optional
            Label text displayed before the HTML content. Default is "".
        *args : tuple
            Additional positional arguments for ipywidgets.HTML.
        **kwargs : dict
            Additional keyword arguments for ipywidgets.HTML.

        Notes
        -----
        This widget is Jupyter-specific and has no equivalent in the
        terminal-based EZInputPrompt interface.

        Examples
        --------
        >>> gui.add_HTML("info", "<b>Important:</b> Fill all fields")
        >>> gui.add_HTML("link", '<a href="url">Documentation</a>')
        >>> gui.add_HTML("styled", '<p style="color:red">Warning</p>')
        """
        style = kwargs.pop("style", self._style)
        self.elements[tag] = widgets.HTML(
            value=value,
            description=description,
            *args,
            **kwargs,
            layout=self._layout,
            style=style,
        )

        return self.elements[tag]

    def add_int_range(
        self,
        tag: str,
        description: str,
        vmin: int,
        vmax: int,
        *args,
        remember_value=True,
        on_change: Optional[callable] = None,
        **kwargs,
    ):
        """**@unified** - Add an integer slider widget.

        Creates a slider for selecting integer values within a specified range
        by dragging a handle or clicking.

        Parameters
        ----------
        tag : str
            Unique identifier for this widget.
        description : str
            Label text displayed next to the slider.
        vmin : int
            Minimum slider value (inclusive).
        vmax : int
            Maximum slider value (inclusive).
        remember_value : bool, optional
            If True, remembers and restores the last selected value.
            Default is True.
        on_change : callable, optional
            Callback function executed when the slider value changes.
            Should accept one argument (the change dictionary).
            Default is None.
        value : int, optional
            Initial slider value (passed via kwargs).
        step : int, optional
            Increment step for the slider (passed via kwargs). Default is 1.
        *args : tuple
            Additional positional arguments for ipywidgets.IntSlider.
        **kwargs : dict
            Additional keyword arguments for ipywidgets.IntSlider.

        Examples
        --------
        >>> gui.add_int_range("iterations", "Iterations:", 10, 1000)
        >>> gui.add_int_range("count", "Count:", 0, 100, value=50, step=5)
        """
        if (
            remember_value
            and tag in self.cfg
            and vmin <= self.cfg[tag] <= vmax
        ):
            kwargs["value"] = int(self.cfg[tag])
        if self.params is not None:
            if tag in self.params and vmin <= self.params[tag] <= vmax:
                kwargs["value"] = self.params[tag]

        if "continuous_update" not in kwargs:
            update = True
        else:
            update = kwargs["continuous_update"]
            kwargs.pop("continuous_update")

        style = kwargs.pop("style", self._style)
        self.elements[tag] = widgets.IntSlider(
            description=description,
            min=vmin,
            max=vmax,
            continuous_update=update,
            *args,
            **kwargs,
            layout=self._layout,
            style=style,
        )

        if on_change is not None:
            self.elements[tag].observe(on_change, names="value")

        return self.elements[tag]

    def add_int_slider(
        self,
        tag: str,
        description: str,
        min: int,
        max: int,
        *args,
        remember_value=True,
        on_change: Optional[callable] = None,
        **kwargs,
    ):
        """**@jupyter** - Add an integer slider widget (alias).

        This is an alias for `add_int_range` with `min`/`max` parameter names
        instead of `vmin`/`vmax`. Provides more intuitive naming for Jupyter users.

        Parameters
        ----------
        tag : str
            Unique identifier for this widget.
        description : str
            Label text displayed next to the slider.
        min : int
            Minimum slider value (inclusive).
        max : int
            Maximum slider value (inclusive).
        remember_value : bool, optional
            If True, remembers and restores the last selected value.
            Default is True.
        on_change : callable, optional
            Callback function executed when the slider value changes.
            Default is None.
        *args : tuple
            Additional positional arguments.
        **kwargs : dict
            Additional keyword arguments.

        See Also
        --------
        add_int_range : The underlying implementation
        """
        self.add_int_range(
            tag,
            description,
            vmin=min,
            vmax=max,
            *args,
            remember_value=remember_value,
            **kwargs,
        )

        if on_change is not None:
            self.elements[tag].observe(on_change, names="value")

        return self.elements[tag]

    def add_float_range(
        self,
        tag: str,
        description: str,
        vmin: float,
        vmax: float,
        *args,
        remember_value=True,
        on_change: Optional[callable] = None,
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
        if (
            remember_value
            and tag in self.cfg
            and vmin <= self.cfg[tag] <= vmax
        ):
            kwargs["value"] = float(self.cfg[tag])
        if (
            self.params is not None
            and tag in self.params
            and vmin <= self.params[tag] <= vmax
        ):
            kwargs["value"] = self.params[tag]

        if "continuous_update" not in kwargs:
            update = True
        else:
            update = kwargs["continuous_update"]
            kwargs.pop("continuous_update")

        style = kwargs.pop("style", self._style)
        self.elements[tag] = widgets.FloatSlider(
            description=description,
            min=vmin,
            max=vmax,
            continuous_update=update,
            *args,
            **kwargs,
            layout=self._layout,
            style=style,
        )

        if on_change is not None:
            self.elements[tag].observe(on_change, names="value")

        return self.elements[tag]

    def add_float_slider(
        self,
        tag: str,
        description: str,
        min: int,
        max: int,
        *args,
        remember_value=True,
        on_change: Optional[callable] = None,
        **kwargs,
    ):
        """**@jupyter** - Add a float slider widget (alias).

        This is an alias for `add_float_range` with `min`/`max` parameter names
        instead of `vmin`/`vmax`. Provides more intuitive naming for Jupyter users.

        Parameters
        ----------
        tag : str
            Unique identifier for this widget.
        description : str
            Label text displayed next to the slider.
        min : float
            Minimum slider value (inclusive).
        max : float
            Maximum slider value (inclusive).
        remember_value : bool, optional
            If True, remembers and restores the last selected value.
            Default is True.
        on_change : callable, optional
            Callback function executed when the slider value changes.
            Default is None.
        *args : tuple
            Additional positional arguments.
        **kwargs : dict
            Additional keyword arguments.

        See Also
        --------
        add_float_range : The underlying implementation
        """
        self.add_float_range(
            tag,
            description,
            vmin=min,
            vmax=max,
            *args,
            remember_value=remember_value,
            **kwargs,
        )

        if on_change is not None:
            self.elements[tag].observe(on_change, names="value")

        return self.elements[tag]

    def add_check(
        self,
        tag: str,
        description: str,
        *args,
        remember_value=True,
        on_change: Optional[callable] = None,
        **kwargs,
    ):
        """**@unified** - Add a checkbox widget.

        Creates a checkbox for boolean (True/False) selection.

        Parameters
        ----------
        tag : str
            Unique identifier for this widget.
        description : str
            Label text displayed next to the checkbox.
        remember_value : bool, optional
            If True, remembers and restores the last selected value.
            Default is True.
        on_change : callable, optional
            Callback function executed when the checkbox state changes.
            Should accept one argument (the change dictionary).
            Default is None.
        value : bool, optional
            Initial checkbox state (passed via kwargs). Default is False.
        *args : tuple
            Additional positional arguments for ipywidgets.Checkbox.
        **kwargs : dict
            Additional keyword arguments for ipywidgets.Checkbox.

        Examples
        --------
        >>> gui.add_check("verbose", "Enable verbose output")
        >>> gui.add_check("confirm", "I agree", value=True)
        """
        if remember_value and tag in self.cfg:
            kwargs["value"] = self.cfg[tag]
        if self.params is not None and tag in self.params:
            kwargs["value"] = self.params[tag]
        style = kwargs.pop("style", self._style)
        self.elements[tag] = widgets.Checkbox(
            description=description,
            *args,
            **kwargs,
            layout=self._layout,
            style=style,
        )

        if on_change is not None:
            self.elements[tag].observe(on_change, names="value")

        return self.elements[tag]

    def add_int_text(
        self,
        tag,
        description: str = "",
        *args,
        remember_value=True,
        on_change: Optional[callable] = None,
        **kwargs,
    ):
        """**@unified** - Add an integer text input widget.

        Creates a text field that accepts only integer values.

        Parameters
        ----------
        tag : str
            Unique identifier for this widget.
        description : str, optional
            Label text displayed next to the input. Default is "".
        remember_value : bool, optional
            If True, remembers and restores the last entered value.
            Default is True.
        on_change : callable, optional
            Callback function executed when the value changes.
            Default is None.
        value : int, optional
            Initial integer value (passed via kwargs).
        *args : tuple
            Additional positional arguments for ipywidgets.IntText.
        **kwargs : dict
            Additional keyword arguments for ipywidgets.IntText.

        Examples
        --------
        >>> gui.add_int_text("age", "Age:")
        >>> gui.add_int_text("population", "Population:", value=1000000)
        """
        if remember_value and tag in self.cfg:
            kwargs["value"] = self.cfg[tag]
        if self.params is not None and tag in self.params:
            kwargs["value"] = self.params[tag]

        style = kwargs.pop("style", self._style)
        self.elements[tag] = widgets.IntText(
            description=description,
            continuous_update=True,
            *args,
            **kwargs,
            layout=self._layout,
            style=style,
        )

        if on_change is not None:
            self.elements[tag].observe(on_change, names="value")

        return self.elements[tag]

    def add_bounded_int_text(
        self,
        tag,
        description: str,
        vmin: int,
        vmax: int,
        *args,
        remember_value=True,
        on_change: Optional[callable] = None,
        **kwargs,
    ):
        """**@unified** - Add a bounded integer text input widget.

        Creates a text field that accepts only integers within a specified range.
        Values outside the range are automatically clamped.

        Parameters
        ----------
        tag : str
            Unique identifier for this widget.
        description : str
            Label text displayed next to the input.
        vmin : int
            Minimum allowed value (inclusive).
        vmax : int
            Maximum allowed value (inclusive).
        remember_value : bool, optional
            If True, remembers and restores the last entered value.
            Default is True.
        on_change : callable, optional
            Callback function executed when the value changes.
            Default is None.
        value : int, optional
            Initial value (passed via kwargs).
        *args : tuple
            Additional positional arguments for ipywidgets.BoundedIntText.
        **kwargs : dict
            Additional keyword arguments for ipywidgets.BoundedIntText.

        Examples
        --------
        >>> gui.add_bounded_int_text("percentage", "Percentage:", 0, 100)
        """
        if remember_value and tag in self.cfg:
            kwargs["value"] = self.cfg[tag]
        if self.params is not None and tag in self.params:
            kwargs["value"] = self.params[tag]
        style = kwargs.pop("style", self._style)
        self.elements[tag] = widgets.BoundedIntText(
            min=vmin,
            max=vmax,
            description=description,
            continuous_update=True,
            *args,
            **kwargs,
            layout=self._layout,
            style=style,
        )

        if on_change is not None:
            self.elements[tag].observe(on_change, names="value")

        return self.elements[tag]

    def add_float_text(
        self,
        tag,
        description: str = "",
        *args,
        remember_value=True,
        on_change: Optional[callable] = None,
        **kwargs,
    ):
        """**@unified** - Add a float text input widget.

        Creates a text field that accepts floating-point numbers.

        Parameters
        ----------
        tag : str
            Unique identifier for this widget.
        description : str, optional
            Label text displayed next to the input. Default is "".
        remember_value : bool, optional
            If True, remembers and restores the last entered value.
            Default is True.
        on_change : callable, optional
            Callback function executed when the value changes.
            Default is None.
        value : float, optional
            Initial float value (passed via kwargs).
        *args : tuple
            Additional positional arguments for ipywidgets.FloatText.
        **kwargs : dict
            Additional keyword arguments for ipywidgets.FloatText.

        Examples
        --------
        >>> gui.add_float_text("temperature", "Temperature (°C):")
        >>> gui.add_float_text("pi", "Pi:", value=3.14159)
        """
        if remember_value and tag in self.cfg:
            kwargs["value"] = self.cfg[tag]
        if self.params is not None and tag in self.params:
            kwargs["value"] = self.params[tag]
        style = kwargs.pop("style", self._style)
        self.elements[tag] = widgets.FloatText(
            description=description,
            continuous_update=True,
            *args,
            **kwargs,
            layout=self._layout,
            style=style,
        )

        if on_change is not None:
            self.elements[tag].observe(on_change, names="value")

        return self.elements[tag]

    def add_bounded_float_text(
        self,
        tag,
        description: str,
        vmin: int,
        vmax: int,
        *args,
        remember_value=True,
        on_change: Optional[callable] = None,
        **kwargs,
    ):
        """**@unified** - Add a bounded float text input widget.

        Creates a text field that accepts only floats within a specified range.
        Values outside the range are automatically clamped.

        Parameters
        ----------
        tag : str
            Unique identifier for this widget.
        description : str
            Label text displayed next to the input.
        vmin : float
            Minimum allowed value (inclusive).
        vmax : float
            Maximum allowed value (inclusive).
        remember_value : bool, optional
            If True, remembers and restores the last entered value.
            Default is True.
        on_change : callable, optional
            Callback function executed when the value changes.
            Default is None.
        value : float, optional
            Initial value (passed via kwargs).
        *args : tuple
            Additional positional arguments for ipywidgets.BoundedFloatText.
        **kwargs : dict
            Additional keyword arguments for ipywidgets.BoundedFloatText.

        Examples
        --------
        >>> gui.add_bounded_float_text("alpha", "Alpha:", 0.0, 1.0)
        >>> gui.add_bounded_float_text("temp", "Temperature:", -273.15, 1000.0)
        """
        if remember_value and tag in self.cfg:
            kwargs["value"] = self.cfg[tag]
        if self.params is not None and tag in self.params:
            kwargs["value"] = self.params[tag]
        style = kwargs.pop("style", self._style)
        self.elements[tag] = widgets.BoundedFloatText(
            min=vmin,
            max=vmax,
            description=description,
            continuous_update=True,
            *args,
            **kwargs,
            layout=self._layout,
            style=style,
        )

        if on_change is not None:
            self.elements[tag].observe(on_change, names="value")

        return self.elements[tag]

    def add_dropdown(
        self,
        tag,
        options: list,
        description: str = "",
        *args,
        remember_value=True,
        on_change: Optional[callable] = None,
        **kwargs,
    ):
        """**@unified** - Add a dropdown selection widget.

        Creates a dropdown menu for selecting one option from a list.

        Parameters
        ----------
        tag : str
            Unique identifier for this widget.
        options : list
            List of options to display in the dropdown.
        description : str, optional
            Label text displayed next to the dropdown. Default is "".
        remember_value : bool, optional
            If True, remembers and restores the last selected value.
            Default is True.
        on_change : callable, optional
            Callback function executed when selection changes.
            Default is None.
        value : Any, optional
            Initially selected value (passed via kwargs). Must be in options.
        *args : tuple
            Additional positional arguments for ipywidgets.Dropdown.
        **kwargs : dict
            Additional keyword arguments for ipywidgets.Dropdown.

        Examples
        --------
        >>> gui.add_dropdown("color", ["red", "green", "blue"], "Color:")
        >>> gui.add_dropdown("method", ["A", "B", "C"], value="B")
        """
        if remember_value and tag in self.cfg and self.cfg[tag] in options:
            kwargs["value"] = self.cfg[tag]
        if self.params is not None and tag in self.params:
            kwargs["value"] = self.params[tag]
        style = kwargs.pop("style", self._style)
        self.elements[tag] = widgets.Dropdown(
            options=options,
            description=description,
            *args,
            **kwargs,
            layout=self._layout,
            style=style,
        )

        if on_change is not None:
            self.elements[tag].observe(on_change, names="value")

        return self.elements[tag]

    def add_checkbox(
        self,
        tag: str,
        description: str,
        *args,
        remember_value=True,
        on_change: Optional[callable] = None,
        **kwargs,
    ):
        """**@jupyter** - Add a checkbox widget (alias).

        This is an alias for `add_check`. Both methods create identical
        checkbox widgets.

        Parameters
        ----------
        tag : str
            Unique identifier for this widget.
        description : str
            Label text displayed next to the checkbox.
        remember_value : bool, optional
            If True, remembers and restores the last selected value.
            Default is True.
        on_change : callable, optional
            Callback function executed when the checkbox state changes.
            Default is None.
        *args : tuple
            Additional positional arguments.
        **kwargs : dict
            Additional keyword arguments.

        See Also
        --------
        add_check : The underlying implementation
        """
        self.add_check(
            tag,
            description=description,
            remember_value=remember_value,
            *args,
            **kwargs,
        )

        if on_change is not None:
            self.elements[tag].observe(on_change, names="value")

        return self.elements[tag]

    def add_select_multiple(
        self, tag: str, options: list, description: str = "", *args, **kwargs
    ):
        """**@jupyter** - Add a multiple selection widget.

        Creates a selection box that allows choosing multiple options from a list.
        This widget is specific to Jupyter notebooks.

        Parameters
        ----------
        tag : str
            Unique identifier for this widget.
        options : list
            List of available options to select from.
        description : str, optional
            Label text displayed next to the selection box. Default is "".
        *args : tuple
            Additional positional arguments for ipywidgets.SelectMultiple.
        **kwargs : dict
            Additional keyword arguments for ipywidgets.SelectMultiple.

        Notes
        -----
        This widget is Jupyter-specific with no terminal equivalent.
        The value will be a tuple of selected items.

        Examples
        --------
        >>> gui.add_select_multiple("features", ["A", "B", "C", "D"],
        ...                         "Select features:")
        """
        style = kwargs.pop("style", self._style)
        self.elements[tag] = widgets.SelectMultiple(
            options=options,
            description=description,
            *args,
            **kwargs,
            layout=self._layout,
            style=style,
        )

        return self.elements[tag]

    def add_file_upload(
        self, tag, *args, accept=None, remember_value=True, **kwargs
    ):
        """**@jupyter** - Add a file chooser widget.

        Creates a file browser widget for selecting files from the filesystem.
        Uses ipyfilechooser for an intuitive file selection interface.

        Parameters
        ----------
        tag : str
            Unique identifier for this widget.
        accept : str, optional
            File type filter pattern (e.g., "*.txt", "*.csv"). Default is None.
        remember_value : bool, optional
            If True, remembers and restores the last selected file path.
            Default is True.
        *args : tuple
            Additional positional arguments.
        **kwargs : dict
            Additional keyword arguments.

        Notes
        -----
        This widget is Jupyter-specific and uses the FileChooser widget.
        Not available in the terminal interface (use `add_path_completer` instead).

        Examples
        --------
        >>> gui.add_file_upload("data_file", accept="*.csv")
        >>> gui.add_file_upload("config", accept="*.yml")
        """
        self.elements[tag] = FileChooser()
        if tag in self.cfg and remember_value:
            selected_file = self.cfg[tag]
            if selected_file is None:
                selected_file = ""
            self.elements[tag].default_path = os.path.dirname(selected_file)
            self.elements[tag].default_filename = os.path.basename(
                selected_file
            )
            self.elements[tag].reset()

        self.elements[tag].register_callback(self._save_settings)
        if accept is not None:
            self.elements[tag].filter_pattern = accept

        return self.elements[tag]

    def add_output(self, tag: str, *args, **kwargs):
        """**@unified** - Add an output widget for displaying results.

        Creates an output area that can capture and display printed output,
        plots, and other content.

        Parameters
        ----------
        tag : str
            Unique identifier for this widget.
        *args : tuple
            Additional positional arguments for ipywidgets.Output.
        **kwargs : dict
            Additional keyword arguments for ipywidgets.Output.

        Notes
        -----
        Use with context manager syntax to capture output:
        ```python
        with gui['output']:
            print("This appears in the output widget")
        ```

        Examples
        --------
        >>> gui.add_output("results")
        >>> with gui['results']:
        ...     print("Analysis complete!")
        """
        style = kwargs.pop("style", self._style)
        self.elements[tag] = widgets.Output(
            *args,
            **kwargs,
            layout=self._layout,
            style=style,
        )

        return self.elements[tag]

    def add_custom_widget(
        self,
        tag: str,
        custom_widget,
        *args,
        remember_value=True,
        on_change: Optional[callable] = None,
        **kwargs,
    ):
        """**@jupyter** - Add a custom ipywidget to the container.

        Allows adding any ipywidget that isn't directly supported by
        the built-in methods.

        Parameters
        ----------
        tag : str
            Unique identifier for this widget.
        custom_widget : type
            The ipywidget class to instantiate (e.g., widgets.ColorPicker).
        remember_value : bool, optional
            If True, attempts to remember and restore the last value.
            Default is True.
        on_change : callable, optional
            Callback function executed when the widget value changes.
            Default is None.
        *args : tuple
            Positional arguments passed to the widget constructor.
        **kwargs : dict
            Keyword arguments passed to the widget constructor.

        Examples
        --------
        >>> gui.add_custom_widget("color", widgets.ColorPicker,
        ...                       description="Pick a color:")
        >>> gui.add_custom_widget("date", widgets.DatePicker, value=date.today())
        """
        if remember_value and tag in self.cfg:
            kwargs["value"] = self.cfg[tag]
        if self.params is not None and tag in self.params:
            kwargs["value"] = self.params[tag]
        style = kwargs.pop("style", self._style)
        self.elements[tag] = custom_widget(
            *args,
            **kwargs,
            layout=self._layout,
            style=style,
        )

        if on_change is not None:
            self.elements[tag].observe(on_change, names="value")

        return self.elements[tag]

    def save_parameters(self, path: str):
        """**@unified** - Save current widget values to a YAML file.

        Exports all widget values to a YAML file that can be loaded later.

        Parameters
        ----------
        path : str
            The file path for saving parameters. If it doesn't end with '.yml',
            the filename will be auto-generated as '{title}_parameters.yml'.

        Examples
        --------
        >>> gui.save_parameters("my_config.yml")
        >>> gui.save_parameters("/path/to/")  # Auto-named file

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

    def load_parameters(self, path: str):
        """**@unified** - Load widget values from a YAML file.

        Loads parameters from a previously saved file. Values will be used
        as defaults when creating widgets.

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
        >>> gui.load_parameters("my_config.yml")
        >>> # Subsequent widgets will use loaded values

        See Also
        --------
        save_parameters : Save parameters to a file
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"The file {path} does not exist.")
        with open(path, "r") as f:
            params = yaml.load(f, Loader=yaml.SafeLoader)
        self.params = params

    def _save_settings(self):
        """**@unified** - Internal method to save settings automatically.

        Saves current widget values to the persistent configuration file.
        This method is called automatically and should not be called directly.

        Notes
        -----
        Configuration files are stored in `~/.ezinput/{title}.yml`.
        Tuple values (from SelectMultiple) are excluded from saving.
        """
        for tag in self.elements:
            if hasattr(self.elements[tag], "value"):
                if type(self.elements[tag].value) != tuple:
                    self.cfg[tag] = self.elements[tag].value
        config_file = CONFIG_PATH / f"{self.title}.yml"
        config_file.parent.mkdir(exist_ok=True)

        base_config = self._get_config(self.title)  # loads the config file
        for key, value in self.cfg.items():
            base_config[key] = value

        with open(config_file, "w") as f:
            yaml.dump(base_config, f)

    def _on_value_change(self, change):
        """**@jupyter** - Internal callback for automatic settings persistence.

        Automatically saves settings whenever a widget value changes.
        This method is called internally and should not be called directly.

        Parameters
        ----------
        change : dict
            The change event dictionary from ipywidgets.
        """
        self._save_settings()

    def show(self):
        """**@unified** - Display all widgets in the Jupyter notebook.

        Renders the widget container in the notebook output cell and enables
        automatic value change tracking for all widgets.

        Notes
        -----
        This should be called after adding all desired widgets. Widgets
        can still be added after calling show(), but you'll need to call
        show() again to display them.

        Examples
        --------
        >>> gui.add_text("name", "Name:")
        >>> gui.add_int_slider("age", "Age:", min=0, max=120)
        >>> gui.show()  # Displays all widgets
        """
        for tag in self.elements:
            self.elements[tag].observe(self._on_value_change, names="value")
        self._main_display.children = tuple(self.elements.values())
        clear_output()
        display(self._main_display)

    def clear_elements(self):
        """**@unified** - Clear all widgets from the container.

        Removes all widgets and resets the display. Useful for rebuilding
        the GUI dynamically.

        Notes
        -----
        This does not delete saved configuration files.
        """
        self.elements = {}
        self._nLabels = 0
        self._main_display.children = ()

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
        {'name': 'Alice', 'age': 30, 'active': True}
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
