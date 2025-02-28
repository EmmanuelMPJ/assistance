import json
import pytest
from app import EventHandler
from unittest.mock import MagicMock


def create_mock_tool(name: str, arguments: dict):
    """Creates a mock for tool and data, where it is possible to set a customizable name
    and argument."""
    mock_tool = MagicMock()
    mock_tool.function.name = name
    mock_tool.function.arguments = json.dumps(arguments)
    mock_tool.id = "tool_123"

    mock_data = MagicMock()
    mock_data.required_action.submit_tool_outputs.tool_calls = [mock_tool]

    return mock_data


@pytest.fixture
def setup_handler():
    """Instance EventHandler and create a mock for the method submit_tool_outputs."""
    handler = EventHandler()
    handler.submit_tool_outputs = MagicMock()
    return handler


@pytest.fixture
def setup_mock_tool():
    return create_mock_tool


@pytest.fixture
def run_id():
    return "run_123"
