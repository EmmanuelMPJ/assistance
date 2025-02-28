import pytest
from unittest.mock import patch


@pytest.mark.parametrize(
    "catalog, name_argument, expected_output",
    [
        (
            [{"Name": "Tablet", "Description": "10 Kg", "Price": 20}],
            "TabletXYZ",
            "Product not found.",
        ),
        (
            [{"Name": "Laptop", "Description": "16GB RAM, 1TB NVMe", "Price": 1000}],
            "Laptop",
            "The product is Laptop with description: 16GB RAM, 1TB NVMe and price: 1000.",
        ),
        ([], "Laptop", "Product not found."),
    ],
)
def test_get_product_info(
    catalog, name_argument, expected_output, setup_handler, setup_mock_tool, run_id
):
    """Verify that the information about the product requested, such as the name,
    description and price is returned properly when get_product_info is called.
    """
    handler = setup_handler

    mock_data = setup_mock_tool("get_product_info", {"Name": name_argument})

    with patch("app.catalog", catalog):
        handler.handle_requires_action(mock_data, run_id)

    tool_outputs = handler.submit_tool_outputs.call_args[0][0]

    assert any(
        expected_output == output["output"] for output in tool_outputs
    ), f"Expected output not found in tool_outputs: {tool_outputs}"
