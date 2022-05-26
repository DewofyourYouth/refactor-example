from refactor_example.orders.order import Order, OrderRow, inventory
from refactor_example.main import sample_orders
from pytest import mark

joe, peter, glenn = sample_orders()


@mark.describe("An Order Row is a class for holding data about products in an order.")
class TestOrderRow:
    @mark.it("OrderRow.row_price is the price of the row.")
    def test_order_row_price(self):
        row0 = OrderRow(item=inventory.MILK, quantity=1)
        row1 = OrderRow(item=inventory.MILK, quantity=3)
        assert row0.row_price == 416
        assert row1.row_price == 1248

    @mark.it("OrderRow.increment_quantity increases the quantity and row price")
    def test_increment_quantity(self):
        joe_milk = joe.order_items[0]
        assert joe_milk.quantity == 2
        assert joe_milk.row_price == 832
        joe_milk.increment_quantity()
        assert joe_milk.quantity == 3
        assert joe_milk.row_price == 1248

    @mark.it("OrderRow.decrement_quantity decreases the quantity and row price")
    def test_decrement_quantity(self):
        joe_milk = joe.order_items[0]
        assert joe_milk.quantity == 3
        joe_milk.decrement_quantity(2)
        assert joe_milk.quantity == 1
        assert joe_milk.row_price == 416


@mark.describe("An Order is a the itemized record of a transaction.")
class TestOrder:
    @mark.it("Order.balance is the sum of price of all the rows in the order")
    def test_order_balace(self):
        assert peter.balance == 8955
        assert joe.balance == 1471
