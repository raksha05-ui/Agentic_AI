import unittest
from src.models.order import Order
from src.services.orders_service import OrdersService

class TestOrders(unittest.TestCase):

    def setUp(self):
        self.orders_service = OrdersService()

    def test_create_order(self):
        order_data = {
            'product_id': 1,
            'quantity': 2
        }
        order = self.orders_service.create_order(order_data)
        self.assertIsNotNone(order)
        self.assertEqual(order.product_id, order_data['product_id'])
        self.assertEqual(order.quantity, order_data['quantity'])

    def test_get_order(self):
        order_data = {
            'product_id': 1,
            'quantity': 2
        }
        order = self.orders_service.create_order(order_data)
        fetched_order = self.orders_service.get_order(order.order_id)
        self.assertEqual(fetched_order.order_id, order.order_id)

    def test_update_order(self):
        order_data = {
            'product_id': 1,
            'quantity': 2
        }
        order = self.orders_service.create_order(order_data)
        updated_data = {
            'quantity': 3
        }
        updated_order = self.orders_service.update_order(order.order_id, updated_data)
        self.assertEqual(updated_order.quantity, updated_data['quantity'])

    def test_delete_order(self):
        order_data = {
            'product_id': 1,
            'quantity': 2
        }
        order = self.orders_service.create_order(order_data)
        self.orders_service.delete_order(order.order_id)
        fetched_order = self.orders_service.get_order(order.order_id)
        self.assertIsNone(fetched_order)

if __name__ == '__main__':
    unittest.main()