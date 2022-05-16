from flask import Flask
from refactor_example.main import sample_orders

app = Flask(__name__)


@app.route("/orders")
def orders():
    # return {order.order_id: order for order in sample_orders()}
    api_formatter = API
    return tuple(sample_orders())


@app.route("/receipt/<string:order_id>")
def receipt(order_id):
    pass


if __name__ == "__main__":
    app.run(debug=True)
