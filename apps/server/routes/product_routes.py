from flask import Blueprint, request, jsonify
from database.services.product_service import (
    create_product,
    get_products,
    get_product,
)

bp = Blueprint("products", __name__, url_prefix="/products")


@bp.post("/")
def add_product():
    product = create_product(request.json)
    return jsonify(product), 201


@bp.get("/")
def list_products():
    limit = request.args.get("limit", type=int)
    return jsonify(get_products(limit))


@bp.get("/<identifier>")
def get_single_product(identifier):
    try:
        identifier = int(identifier)
    except ValueError:
        pass

    product = get_product(identifier)
    if not product:
        return {"error": "Product not found"}, 404

    return jsonify(product)
