from flask import Blueprint, request, jsonify

from src.unit_of_work import SqlAlchemyUnitOfWork
from src.services import (OrderService,
                          OrderNotFoundError,
                          ProductNotFoundError,
                          OutOfStockError)

orders_bp = Blueprint("orders", __name__, url_prefix="/api/orders")


@orders_bp.route("/", methods=["GET"])
def ping():
    """
        Ping endpoint
        ---
        responses:
          200:
            description: Returns pong
            schema:
              type: object
              properties:
                ping:
                  type: string
                  example: pong
        """
    return jsonify({"ping": "pong"})



@orders_bp.route("/<int:order_id>/items", methods=["POST"])
def add_item(order_id):
    """
        Add item to order
        ---
        tags:
          - Order Items
        parameters:
          - name: order_id
            in: path
            type: integer
            required: true
            description: ID of the order
          - name: body
            in: body
            required: true
            schema:
              type: object
              required:
                - product_id
                - quantity
              properties:
                product_id:
                  type: integer
                  description: ID of the product to add
                  example: 1
                quantity:
                  type: integer
                  description: Quantity of the product
                  example: 2
        responses:
          201:
            description: Item added successfully
            schema:
              type: object
              properties:
                id:
                  type: integer
                  description: ID of the created order item
                order_id:
                  type: integer
                  description: ID of the order
                product_id:
                  type: integer
                  description: ID of the product
                quantity:
                  type: integer
                  description: Quantity of the product
                unit_price:
                  type: string
                  description: Unit price as string (decimal)
          400:
            description: Bad request - missing or invalid parameters
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "product_id and quantity required"
          404:
            description: Order or product not found
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Order not found"
          409:
            description: Conflict - product out of stock
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Product out of stock"
          500:
            description: Internal server error
        """
    data = request.get_json(force=True)
    product_id = data.get("product_id")
    qty = data.get("quantity")

    if product_id is None or qty is None:
        return jsonify({"error": "product_id and quantity required"}), 400
    try:
        qty = int(qty)
    except ValueError:
        return jsonify({"error": "quantity must be integer"}), 400

    with SqlAlchemyUnitOfWork() as uow:
        service = OrderService(uow)
        try:
            item = service.add_item(order_id, product_id, qty)
            uow.commit()
            return jsonify({
                "id": item.id,
                "order_id": item.order_id,
                "product_id": item.product_id,
                "quantity": item.quantity,
                "unit_price": str(item.unit_price),
            }), 201
        except OrderNotFoundError as e:
            return jsonify({"error": str(e)}), 404
        except ProductNotFoundError as e:
            return jsonify({"error": str(e)}), 404
        except OutOfStockError as e:
            return jsonify({"error": str(e)}), 409
        except Exception as e:
            uow.rollback()
            return jsonify({"error": f"Internal error: {e}"}), 500