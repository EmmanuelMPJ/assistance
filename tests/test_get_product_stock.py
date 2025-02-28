import pytest
from unittest.mock import patch


@pytest.mark.parametrize(
    "catalog, name_argument, expected_output",
    [
        (
            [
                {
                    "Name": "Tablet",
                    "Description": "10 Kg",
                    "Price": 20,
                    "Stock_availabiility": 1,
                }
            ],
            "TabletXYZ",
            "Product not found.",
        ),
        (
            [
                {
                    "Name": "Laptop",
                    "Description": "16GB RAM, 1TB NVMe",
                    "Price": 1000,
                    "Stock_availabiility": 10,
                }
            ],
            "Laptop",
            "The product Laptop is in stock with availability: 10.",
        ),
        ([], "Laptop", "Product not found."),
    ],
)
def test_get_product_stock(
    catalog, name_argument, expected_output, setup_handler, setup_mock_tool, run_id
):
    """Verify that the get_product_stock correctly reports stock availability."""
    handler = setup_handler

    mock_data = setup_mock_tool("get_product_stock", {"Name": name_argument})

    with patch("app.catalog", catalog):
        handler.handle_requires_action(mock_data, run_id)

    tool_outputs = handler.submit_tool_outputs.call_args[0][0]

    assert any(
        expected_output == output["output"] for output in tool_outputs
    ), f"Expected output not found in tool_outputs: {tool_outputs}"
