import pytest
from unittest.mock import patch


@pytest.mark.parametrize(
    "catalog, expected_products",
    [
        ([{"Name": "Product1"}, {"Name": "Product2"}], "Product1, Product2"),
        (
            [{"Name": "Laptop"}, {"Name": "Mouse"}, {"Name": "Keyboard"}],
            "Laptop, Mouse, Keyboard",
        ),
        ([], ""),
    ],
)
def test_get_all_products(
    catalog, expected_products, setup_handler, setup_mock_tool, run_id
):
    """Verify that the product names from catalogs are returned properly when get_all_products
    is called."""

    handler = setup_handler

    mock_data = setup_mock_tool("get_all_products", {})

    with patch("app.catalog", catalog):
        handler.handle_requires_action(mock_data, run_id)

    tool_outputs = handler.submit_tool_outputs.call_args[0][0]

    expected_output = f"The available products are: {expected_products}."

    assert any(
        expected_output == output["output"] for output in tool_outputs
    ), f"Expected output not found in tool_outputs: {tool_outputs}"
