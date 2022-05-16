from flask import Flask
from refactor_example.main import sample_orders
from refactor_example.orders.output.receipt_formatter import JSONAPIReceipt

app = Flask(__name__)

sample_orders = {
    order.order_id: JSONAPIReceipt()._serialize_order(order)
    for order in sample_orders()
}


@app.route("/orders")
def orders():
    return sample_orders


@app.route("/receipt/<string:order_id>")
def receipt(order_id):
    pass


if __name__ == "__main__":
    app.run(debug=True)
