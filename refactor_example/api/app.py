from flask import Flask
from refactor_example.main import sample_orders
from refactor_example.orders.output.receipt_formatter import format_api_receipt

app = Flask(__name__)

sample_orders_dict: dict[str, dict] = {
    order.order_id: format_api_receipt(order) for order in sample_orders()
}


@app.route("/")
def smoke_test():
    return {"message": "The app is running!"}


@app.route("/orders")
def orders():
    return sample_orders_dict


@app.route("/receipt/<string:order_id>")
def receipt(order_id):
    order_data = sample_orders_dict.get(order_id)
    if not order_data:
        return {
            "message": f"We couldn't find an order with an order_id of '{order_id}'."
        }, 404

    return order_data


if __name__ == "__main__":
    app.run(debug=True)
