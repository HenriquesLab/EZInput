from ezinput import EZInput


def test_env_detection():
    gui = EZInput(title="Test_prompt_1")
    assert gui.mode == "prompt"


def test_label():
    gui = EZInput("Test_prompt_2")
    gui.add_label(value="Test Header")


def test_text(mock_input):
    gui = EZInput("Test_prompt_3")
    mock_input.send_text("Example text\n")
    gui.add_text(
        "test_text",
        "Enter text:",
        placeholder="Example text",
        remember_value=True,
    )


def test_text_area(mock_input):
    gui = EZInput("Test_prompt_4")
    mock_input.send_text("Example text\n")
    gui.add_text_area(
        "test_text",
        "Enter text:",
        placeholder="Example text",
        remember_value=True,
    )
    gui.show()


def test_callback(mock_input):
    def custom_sum_text(values):
        sum = values["test_text"].value + values["test_text_2"].value
        gui.add_label(
            value=f"Sum of text: {sum}",
        )
        gui.show()

    gui = EZInput("Test_prompt_5")
    gui.add_label(value="Test Header")

    mock_input.send_text("a\n")
    gui.add_text(
        "test_text",
        description="Enter text:",
        placeholder="Enter text here",
        remember_value=True,
    )
    mock_input.send_text("b\n")
    gui.add_text(
        "test_text_2",
        description="Enter text:",
        placeholder="Enter text here",
        remember_value=True,
    )
    gui.add_callback(
        "button", custom_sum_text, gui.elements, description="Sum Text"
    )
    gui.show()


def test_int_range(mock_input):
    gui = EZInput("Test_prompt_6")
    mock_input.send_text("10\n")
    gui.add_int_range("int_slider", "Int Slider", 0, 100)
    gui.show()


def test_float_range(mock_input):
    gui = EZInput("Test_prompt_7")
    mock_input.send_text("0.5\n")
    gui.add_float_range("int_slider", "Int Slider", 0.0, 1.0)


def test_check(mock_input):
    gui = EZInput("Test_prompt_8")
    mock_input.send_text("yes\n")
    gui.add_check("check", "Check")


def test_numerical_text(mock_input):
    gui = EZInput("Test_prompt_9")
    mock_input.send_text("10\n")
    gui.add_int_text(
        "tag",
        description="Enter an integer:",
        remember_value=True,
    )
    mock_input.send_text("5\n")
    gui.add_bounded_int_text(
        "tag2",
        "Enter a bounded integer:",
        0,
        10,
        remember_value=True,
    )
    mock_input.send_text("2.\n")
    gui.add_float_text(
        "tag3",
        "Enter a float:",
        remember_value=True,
    )
    mock_input.send_text("2.\n")
    gui.add_bounded_float_text(
        "tag4",
        "Enter a bounded float:",
        0.0,
        10.0,
        remember_value=True,
    )
    gui.show()
    gui.save_parameters("")
    gui.save_parameters("test_params.yml")


def test_dropdown(mock_input):
    gui = EZInput("Test_prompt_10")
    mock_input.send_text("Option 3\n")
    gui.add_dropdown(
        "dropdown",
        ["Option 1", "Option 2", "Option 3"],
        "Select an option:",
        remember_value=True,
    )
    gui.show()


def test_save_config(mock_input):
    gui = EZInput("Test_prompt_11")
    mock_input.send_text("10\n")
    gui.add_int_text(
        "tag",
        description="Enter an integer:",
        remember_value=True,
    )
    gui.save_settings()
    gui.show()


def test_path_completion(mock_input):
    gui = EZInput("Test_prompt_12")
    mock_input.send_text("./\n")
    gui.add_path_completer(
        "path",
        description="Enter a file path:",
        remember_value=True,
    )
    gui.show()


def test_param_loading(mock_input):
    gui = EZInput("Test_prompt_13", params_file="test_params.yml")
    mock_input.send_text("10\n")
    gui.add_int_text(
        "tag",
        description="Enter an integer:",
        remember_value=True,
    )
    mock_input.send_text("\n")
    gui.add_bounded_int_text(
        "tag2",
        "Enter a bounded integer:",
        0,
        10,
        remember_value=True,
    )
    mock_input.send_text("\n")
    gui.add_float_text(
        "tag3",
        "Enter a float:",
        remember_value=True,
    )
    mock_input.send_text("\n")
    gui.add_bounded_float_text(
        "tag4",
        "Enter a bounded float:",
        0.0,
        10.0,
        remember_value=True,
    )
    gui.show()


def test_param_loading_auto(mock_input):
    gui = EZInput("Test_prompt_14", params_file="Test_prompt_9_parameters.yml")
    mock_input.send_text("\n")
    gui.add_int_text(
        "tag",
        description="Enter an integer:",
        remember_value=True,
    )
    mock_input.send_text("\n")
    gui.add_bounded_int_text(
        "tag2",
        "Enter a bounded integer:",
        0,
        10,
        remember_value=True,
    )
    mock_input.send_text("\n")
    gui.add_float_text(
        "tag3",
        "Enter a float:",
        remember_value=True,
    )
    mock_input.send_text("\n")
    gui.add_bounded_float_text(
        "tag4",
        "Enter a bounded float:",
        0.0,
        10.0,
        remember_value=True,
    )
    gui.show()

def test_param_loading_non_existing(mock_input):
    gui = EZInput("Test_prompt_15", params_file="False_parameters.yml")
    mock_input.send_text("2\n")
    gui.add_int_text(
        "tag",
        description="Enter an integer:",
        remember_value=True,
    )
    mock_input.send_text("5\n")
    gui.add_bounded_int_text(
        "tag2",
        "Enter a bounded integer:",
        0,
        10,
        remember_value=True,
    )
    mock_input.send_text("0.5\n")
    gui.add_float_text(
        "tag3",
        "Enter a float:",
        remember_value=True,
    )
    mock_input.send_text("5.0\n")
    gui.add_bounded_float_text(
        "tag4",
        "Enter a bounded float:",
        0.0,
        10.0,
        remember_value=True,
    )
    gui.show()