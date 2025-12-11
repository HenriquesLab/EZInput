import pytest
import tempfile
from pathlib import Path
from prompt_toolkit.application import create_app_session
from prompt_toolkit.input import create_pipe_input
from prompt_toolkit.output import DummyOutput


@pytest.fixture(scope="function")
def mock_input():
    with create_pipe_input() as pipe_input:
        with create_app_session(input=pipe_input, output=DummyOutput()):
            yield pipe_input


@pytest.fixture(scope="function")
def temp_config_dir(monkeypatch):
    """
    Use a temporary directory for EZInput config files during tests.

    This fixture isolates tests from existing user config files.
    Use this fixture (by adding it as a parameter) for tests that should
    NOT be affected by pre-existing config files in ~/.ezinput/

    For tests that need to test config loading behavior,
    don't use this fixture.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Patch the CONFIG_PATH in both ezinput modules
        import ezinput.ezinput
        import ezinput.ezinput_prompt

        monkeypatch.setattr(ezinput.ezinput, "CONFIG_PATH", temp_path)
        monkeypatch.setattr(ezinput.ezinput_prompt, "CONFIG_PATH", temp_path)

        yield temp_path


@pytest.fixture(scope="function", autouse=True)
def isolate_tests(request, monkeypatch):
    """
    Automatically isolate most tests from user config files.

    Tests can opt-out by using the 'use_real_config' marker:
        @pytest.mark.use_real_config
        def test_that_needs_real_config():
            ...
    """
    # Check if test is marked to use real config
    if "use_real_config" in request.keywords:
        # Don't isolate - let test use real config directory
        yield
    else:
        # Isolate test with temp directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            import ezinput.ezinput
            import ezinput.ezinput_prompt

            monkeypatch.setattr(ezinput.ezinput, "CONFIG_PATH", temp_path)
            monkeypatch.setattr(
                ezinput.ezinput_prompt, "CONFIG_PATH", temp_path
            )

            yield temp_path
