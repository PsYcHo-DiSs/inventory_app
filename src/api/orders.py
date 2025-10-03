from flask import Blueprint, request, jsonify

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
    data = request.get_json(force=True)
    product_id = data.get("product_id")
    qty = data.get("quantity")

    if product_id is None or qty is None:
        return jsonify({"error": "product_id and quantity required"}), 400
    try:
        qty = int(qty)
    except Exception:
        return jsonify({"error": "quantity must be integer"}), 400


    # TODO repository / service