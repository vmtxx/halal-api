import json
from flask import Flask, jsonify

from api.gemini import checkProduct
from api.openfoodfacts import getProduct
from api.database import addProduct, getDBProduct

app = Flask(__name__)


@app.route("/api/product/<barcode>")
def check(barcode):
    result = getDBProduct(barcode)

    if result is not None:
        return jsonify(result)

    try:
        product = getProduct(barcode)

        if not product:
            return jsonify({"error": "Nie znaleziono produktu"}), 404

        name = product.get("name")
        quantity = product.get("quantity")
        quantity_unit = product.get("quantity_unit")
        ingredients = product.get("ingredients")
        ingredients_with_allergens = product.get(
            "ingredients_with_allergens"
        )

        response = json.loads(
            checkProduct(
                name,
                quantity,
                quantity_unit,
                ingredients,
                ingredients_with_allergens
            )
        )

        is_halal = response["isHalal"]
        description = response["explanation"]

        addProduct(barcode, description, is_halal)

        result = getDBProduct(barcode)

        if result is None:
            return jsonify({
                "error": "Nie udało się odczytać zapisanego produktu"
            }), 500

        return jsonify(result)

    except (ValueError, KeyError, TypeError) as error:
        app.logger.exception("Błąd przetwarzania produktu")
        return jsonify({"error": str(error)}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)