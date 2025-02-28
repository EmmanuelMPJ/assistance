from app import catalog


def test_catalog_loading():
    """Verify that the catalog is loaded correctly and contains the expected format."""

    assert isinstance(catalog, list), "catalog must be a list"
    assert len(catalog) > 0, "catalog must not be empty"

    required_fields = {"Name", "Description", "Price", "Stock_availabiility"}

    for product in catalog:
        assert isinstance(product, dict), "Every single product must be a dictionary"
        assert required_fields.issubset(
            product.keys()
        ), f"Missing fields in a product: {product}"
