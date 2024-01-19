import unittest
from collections import Counter

from servers import ListServer, Product, Client, MapServer, TooManyProductsFoundError

server_types = (ListServer, MapServer)


class ServerTest(unittest.TestCase):

    def test_get_entries_returns_proper_entries(self):
        products = [Product('D12', 1), Product('DF123', 2), Product('DF234', 5)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(Counter([products[2], products[1]]), Counter(entries))

    def test_exceeding_n_max_returned_entries(self):
        products = [Product('DF12', 1), Product('DF123', 2), Product('DG123', 5), Product('DG234', 9),
                    Product('OK23', 1.5), Product('KP235', 6), Product('DF45', 2.5), Product('HH333', 4)]
        for server_type in server_types:
            server = server_type(products)
            with self.assertRaises(TooManyProductsFoundError):
                server.get_entries(2)

    def test_returned_list_sorted(self):
        products = [Product('DR12', 1), Product('DF123', 4), Product('DF234', 2)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(entries, [Product('DR12', 1), Product('DF234', 2), Product('DF123', 4)])


class ClientTest(unittest.TestCase):
    def test_total_price_for_normal_execution(self):
        products = [Product('PP234', 2), Product('PP235', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(5, client.get_total_price(2))

    def test_total_price_for_exception(self):
        products1 = [Product('PS15', 4), Product('PP636', 3.5), Product('FS235', 5)]
        products2 = [Product('PS12', 1), Product('PP234', 2), Product('PS235', 5), Product('PD245', 9),
                     Product('OK23', 1.5), Product('KP235', 6), Product('PW25', 2.5), Product('ZZ111', 4)]
        for server_type in server_types:
            server = server_type(products1)
            client1 = Client(server)
            total_price = client1.get_total_price(4)
            self.assertIsNone(total_price)
        for server_type in server_types:
            server = server_type(products2)
            client2 = Client(server)
            total_price = client2.get_total_price(2)
            self.assertIsNone(total_price)


if __name__ == '__main__':
    unittest.main()