import logging
from flask import Blueprint, request, jsonify, current_app
from app.models import db, Product
from app.schemas import ProductSchema
from marshmallow import ValidationError

bp = Blueprint('api', __name__)

# Initialize schema instances
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


@bp.route('/products', methods=['GET'])
def get_all_products():
    """
    Get all products
    ---
    tags:
      - Products
    responses:
      200:
        description: List of all products
    """
    products = Product.query.all()
    current_app.logger.info("Fetched all products")
    return jsonify(products_schema.dump(products))


@bp.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    """
    Get product by ID
    ---
    tags:
      - Products
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: integer
    responses:
      200:
        description: A single product
      404:
        description: Product not found
    """
    product = Product.query.get_or_404(id)
    current_app.logger.info(f"Fetched product with ID {id}")
    return jsonify(product_schema.dump(product))


@bp.route('/products', methods=['POST'])
def add_product():
    """
    Add a new product
    ---
    tags:
      - Products
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Product'
    responses:
      201:
        description: Product added successfully
      400:
        description: Validation error
    """
    try:
        data = product_schema.load(request.get_json())
    except ValidationError as err:
        current_app.logger.error(f"Validation error while adding product: {err.messages}")
        return jsonify(err.messages), 400

    product = Product(**data)
    db.session.add(product)
    db.session.commit()
    current_app.logger.info(f"Added new product: {product.name}")
    return jsonify({"message": "Product added"}), 201


@bp.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    """
    Update a product
    ---
    tags:
      - Products
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: integer
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Product'
    responses:
      200:
        description: Product updated
      400:
        description: Validation error
      404:
        description: Product not found
    """
    product = Product.query.get_or_404(id)

    try:
        data = product_schema.load(request.get_json(), partial=True)
    except ValidationError as err:
        current_app.logger.error(f"Validation error while updating product ID {id}: {err.messages}")
        return jsonify(err.messages), 400

    for key, value in data.items():
        setattr(product, key, value)
    db.session.commit()
    current_app.logger.info(f"Updated product with ID {id}")
    return jsonify({"message": "Product updated"})


@bp.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    """
    Delete a product
    ---
    tags:
      - Products
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: integer
    responses:
      200:
        description: Product deleted
      404:
        description: Product not found
    """
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    current_app.logger.info(f"Deleted product with ID {id}")
    return jsonify({"message": "Product deleted"})


@bp.route('/api/health', methods=['GET'])
def health():
    """
    Health check endpoint
    ---
    tags:
      - Utility
    responses:
      200:
        description: API is healthy
    """
    current_app.logger.info("Health check endpoint hit")
    return {"status": "ok"}
