import json

from flask.testing import FlaskClient
from pytest import mark
from refactor_example.api.app import app


@mark.describe("Test the Flask endpoints")
class TestFlaskApp:
    client = FlaskClient(app)

    @mark.it("The REST API works.")
    def test_smoke_screen(self):
        response = self.client.get("/")
        data = json.loads(response.get_data(as_text=True))
        assert response.status_code == 200
        assert data["message"] == "The app is running!"

    @mark.it(
        "Orders endpoint returns a JSON dict which has IDs as keys an Order objects as values."
    )
    def test_orders_endpoint(self):
        response = self.client.get("/orders")
        data = json.loads(response.get_data(as_text=True))
        assert response.status_code == 200
        assert (
            data["682c52a0-110a-4fc9-9bed-2392c5cab72a"]["customer_name"]
            == "Joe Swanson"
        )
        assert data["682c52a0-110a-4fc9-9bed-2392c5cab72a"]["balance"] == 14.71
        assert (
            data["09d37df9-48a1-4746-91fb-1bcd125a4ed5"]["customer_name"]
            == "Peter Griffin"
        )

    @mark.it("The /receipt/<item_id> endpoint returns an properly formatted order.")
    def test_receipt_endpoint(self):
        response = self.client.get("/receipt/682c52a0-110a-4fc9-9bed-2392c5cab72a")
        assert response.status_code == 200
        data = json.loads(response.get_data(as_text=True))
        assert data["customer_name"] == "Joe Swanson"

    @mark.it(
        "The /receipt/<item_id> endpoint returns a KeyError when querying an order_it that doesn't exist."
    )
    def test_receipt_endpoint_raises_keyerror_on_non_existant_key(self):
        response = self.client.get("/receipt/yer_mum")
        assert response.status_code == 404
        data = json.loads(response.get_data(as_text=True))
        assert (
            data["message"]
            == "We couldn't find an order with an order_id of 'yer_mum'."
        )
