import subprocess
import sys
import pytest
import time
import re
from unittest.mock import patch


def get_outputs(input: str):
    """Run app.py and send inputs."""

    process = subprocess.Popen(
        [sys.executable, "app.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )

    time.sleep(1)
    process.stdin.write(f"{input}\n")
    process.stdin.flush()

    time.sleep(1)
    process.stdin.write("END\n")
    process.stdin.flush()

    stdout, stderr = process.communicate()

    process.wait()

    return stdout, stderr


@pytest.fixture
def run_assistant():
    return get_outputs


@pytest.mark.parametrize(
    "input, expected_patterns",
    [
        ("I want to buy a Laptop", [r"assistant > i'm searching..."]),
        (
            "~*^",
            [
                r"It (seem(s)*|look(s)*) like",
                r"message.*(incomplete|cut)",
                r"provide.*details",
            ],
        ),
        (
            "",
            [
                r"It (seem(s)*|look(s)*) like",
                r"message.*(incomplete|cut)",
                r"provide.*details",
            ],
        ),
    ],
)
def test_complete_interaction(input, expected_patterns, run_assistant):
    """Check the correct flow of the assistance"""
    stdout, stderr = run_assistant(input)

    assert stderr == "", f"Detected Errors:\n{stderr}"
    assert any(
        re.search(pattern, stdout, re.IGNORECASE) for pattern in expected_patterns
    ), f"Unexpected output:\n{stdout}"
    assert re.search(
        r"Chat is finished\.", stdout, re.IGNORECASE
    ), "The end of the chat was not detected."
