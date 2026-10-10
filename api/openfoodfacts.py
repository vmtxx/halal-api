import requests

BASE_URL = "https://world.openfoodfacts.org/api/v3/product"

HEADERS = {
    "User-Agent": "Halalify/1.0"
}

def getProduct(barcode: str) -> dict | None:
    url = f"{BASE_URL}/{barcode}.json"

    response = requests.get(
        url,
        params={
            "fields": (
                "product_name,"
                "product_quantity,product_quantity_unit,"
                "ingredients_text,"
                "ingredients_text_with_allergens"
            )
        },
        headers=HEADERS,
        timeout=10,
    )

    response.raise_for_status()
    data = response.json()

    product = data.get("product")

    if not isinstance(product, dict) or not product:
        print("API response:", data)
        return None

    return {
        "name": product.get("product_name", ""),
        "quantity": product.get("product_quantity", ""),
        "quantity_unit": product.get("product_quantity_unit", ""),
        "ingredients": product.get("ingredients_text", ""),
        "ingredients_with_allergens": product.get(
            "ingredients_text_with_allergens", ""
        ),
    } 