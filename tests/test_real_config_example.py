"""
Example test showing how to use real config directory.

This demonstrates how to write tests that need to interact with
actual user config files in ~/.ezinput/
"""

import pytest
from ezinput import EZInput


@pytest.mark.use_real_config
def test_with_real_config():
    """
    Example test that uses the real ~/.ezinput/ directory.

    Mark tests with @pytest.mark.use_real_config to opt-out of
    the automatic config isolation and use the real config directory.

    This is useful for:
    - Testing config file loading/saving behavior
    - Testing interaction with existing saved preferences
    - Integration tests that need persistent config
    """
    gui = EZInput("test_real_config_example")
    gui.add_label("lbl", value="This test uses the real config directory.")

    # This will use the real ~/.ezinput/ directory
    # Any saved config will persist after the test
    assert gui.cfg is not None


def test_with_isolated_config():
    """
    Example test that uses temporary isolated config (default behavior).

    By default, all tests use a temporary config directory that is
    cleaned up after the test. This prevents:
    - Tests from interfering with each other
    - Tests from being affected by user's existing config files
    - Tests from leaving behind config files
    """
    gui = EZInput("test_isolated_example")
    gui.add_label("lbl", value="This test uses the real config directory.")

    # This will use a temporary directory that's cleaned up after the test
    # No files will persist in ~/.ezinput/
    assert gui.cfg is not None
