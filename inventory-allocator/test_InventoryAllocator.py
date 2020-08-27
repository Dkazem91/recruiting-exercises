"""
This file contains unittests for the InventoryAllocator class

Author: Daniel Kazemian <Dkazemian@gmail.com>
"""
from InventoryAllocator import InventoryAllocator
import unittest

class TestInventoryAllocator(unittest.TestCase):

    def test_init_success_no_strict(self):
        """
        tests InventoryAllocator initiates successfully with good args
        """

        orders = {'apple': 1}
        warehouses = [{'name': 'owd', 'inventory': { 'apple': 1 } }]

        test_allocator = InventoryAllocator(orders, warehouses)

        assert test_allocator.orders == orders
        assert test_allocator.warehouses == warehouses
    
    def test_init_success_strict(self):
        """
        tests InventoryAllocator initiates successfully with good args, strict
        """

        orders = {'apple': 1}
        warehouses = [{'name': 'owd', 'inventory': { 'apple': 1 } }]

        test_allocator = InventoryAllocator(orders, warehouses, strict=True)

        assert test_allocator.orders == orders
        assert test_allocator.warehouses == warehouses

    def test_init_fail_no_strict(self):
        """
        tests InventoryAllocator init, will succeed to initiate with bad args without strict parameter on
        """

        orders = []
        warehouses = 'warehouse'

        # without strict, no parameter checks, it will pass
        test_allocator = InventoryAllocator(orders, warehouses)

        assert test_allocator.orders == orders
        assert test_allocator.warehouses == warehouses

    def test_init_fail_strict(self):
        """
        tests InventoryAllocator init fails with strict, wrong parameter type
        """

        orders = []
        warehouses = 'warehouse'

        self.assertRaises(AssertionError, InventoryAllocator,orders, warehouses, True)

    def test_init_fail_strict_empty(self):
        """
        tests InventoryAllocator init fails with strict, no data
        """

        orders = {}
        warehouses = []

        self.assertRaises(AssertionError, InventoryAllocator,orders, warehouses, True)

    def test_init_fail_strict_incorrect_order(self):
        """
        tests InventoryAllocator init fails with strict, incorrect key values
        """

        orders = {'bad':'nothing'}
        warehouses = ['nothing']

        self.assertRaises(AssertionError, InventoryAllocator,orders, warehouses, True)

    def test_init_fail_strict_incorrect_warehouse(self):
        """
        tests InventoryAllocator init fails with strict, more incorrect keys
        """

        orders = {'name': 100}
        warehouses = [{'blah': 'owd', 'blah': { 'apple': 1 } }]

        self.assertRaises(AssertionError, InventoryAllocator,orders, warehouses, True)

    def test_init_fail_strict_incorrect_warehouse_name(self):
        """
        tests InventoryAllocator init fails with strict, bad name type
        """

        orders = {'apple': 100}
        warehouses = [{'name': 0, 'inventory': { 'apple': 1 } }]

        self.assertRaises(AssertionError, InventoryAllocator,orders, warehouses, True)

    def test_init_fail_strict_missing_inventory(self):
        """
        tests InventoryAllocator init fails with strict, no inventory key
        """
        
        orders = {'apple': 5}
        warehouses = [{'name': 'owd', 'bad': { 'apple': 1 } }]

        self.assertRaises(AssertionError, InventoryAllocator,orders, warehouses, True)
    
    def test_init_fail_strict_bad_inventory_value(self):
        """
        tests InventoryAllocator init fails with strict, bad item name in inventory
        """
        
        orders = {'apple': 5}
        warehouses = [{'name': 'owd', 'inventory': { 100: 1 } }]

        self.assertRaises(AssertionError, InventoryAllocator,orders, warehouses, True)

    def test_init_fail_strict_bad_inventory_item_value(self):
        """
        tests InventoryAllocator init fails with strict, bad value of item in inventory
        """
        
        orders = {'apple': 5}
        warehouses = [{'name': 'owd', 'inventory': { 'apple': 'bad' } }]

        self.assertRaises(AssertionError, InventoryAllocator,orders, warehouses, True)

    def test_init_fail_strict_bad_inventory_item_integer(self):
        """
        tests InventoryAllocator init fails with strict, bad integer of item in inventory
        """
        
        orders = {'apple': 5}
        warehouses = [{'name': 'owd', 'inventory': { 'apple': -500 } }]
        self.assertRaises(AssertionError, InventoryAllocator, orders, warehouses, True)

    def test_getCheapestShipment_success_one_warehouse(self):
        """
        test for InventoryAllocator.getCheapestShipment success with one order, one warehouse
        """

        orders = {'apple': 5}
        warehouses = [{'name': 'owd', 'inventory': { 'apple': 5 } }]

        test_allocator = InventoryAllocator(orders, warehouses)

        result = test_allocator.getCheapestShipment()
        
        assert result == [{'owd': {'apple': 5}}], "shipment isn't correct: {}".format(result)

    def test_getCheapestShipment_success_multiple_warehouse(self):
        """
        test for InventoryAllocator.getCheapestShipment success with multiple orders, one warehouse for each order
        """

        orders = {'apple': 5, 'banana': 5, 'orange': 5}
        warehouses = [{'name': 'abc', 'inventory': { 'apple': 5 }}, {'name': '123', 'inventory': { 'banana': 5 }}, {'name': 'youandme', 'inventory': { 'orange': 5 }}]

        test_allocator = InventoryAllocator(orders, warehouses)

        result = test_allocator.getCheapestShipment()

        assert result == [{'abc': {'apple': 5}}, {'123': {'banana': 5}}, {'youandme': {'orange': 5}}], "shipment isn't correct: {}".format(result)

    def test_getCheapestShipment_success_multiple_warehouse_big_order(self):
        """
        test for InventoryAllocator.getCheapestShipment success with multiple orders, warehouses have all inventory, but various amounts
        """

        # multiple orders, multiple warehouses, partial allocations from multiple warehouses, cheapest get filled first
        orders = {'apple': 8, 'banana': 90, 'orange': 100}
        warehouses = [
            {
                'name': 'abc',
                'inventory': { 'apple': 0, 'banana': 2, 'orange': 3 }
            },
            {
                'name': '123',
                'inventory': { 'apple': 0, 'banana': 4, 'orange': 2 }
            },
            {
                'name': 'youandme',
                'inventory': { 'apple': 100, 'orange': 5, 'banana': 500, 'orange': 1000 }
            }
        ]

        test_allocator = InventoryAllocator(orders, warehouses)

        result = test_allocator.getCheapestShipment()

        assert result == [
            {'youandme': {'apple': 8, 'banana': 84, 'orange': 95}},
            {'abc': {'banana': 2, 'orange': 3}},
            {'123': {'banana': 4, 'orange': 2}},
        ], "shipment isn't correct: {}".format(result)

    def test_getCheapestShipment_fail_small_inventory2(self):
        """
        test for when there isn't enough inventory to fulfill the order, much more items and warehouses, some could have been filled
        """
        orders = {'apple': 80, 'banana': 90, 'orange': 100}

        # not enough oranges or apples to fulfill this entire order
        warehouses = [
            {
                'name': 'abc',
                'inventory': { 'apple': 4, 'banana': 2, 'orange': 300 }
            },
            {
                'name': '123',
                'inventory': { 'apple': 8, 'banana': 90, 'orange': 2 }
            },
            {
                'name': 'youandme',
                'inventory': {'apple': 0, 'orange': 5, 'banana': 500}
            }
        ]

        test_allocator = InventoryAllocator(orders, warehouses)

        result = test_allocator.getCheapestShipment()

        assert result == [], "no order should be made: {}".format(result)

    def test_getCheapestShipment_fail_small_inventory1(self):
        """
        test for when there isn't enough inventory to fulfill the order, simple
        """
        orders = {'apple': 800}

        # not enough oranges or apples to fulfill this entire order
        warehouses = [{'name': 'abc', 'inventory': { 'apple': 799}}]

        test_allocator = InventoryAllocator(orders, warehouses)

        result = test_allocator.getCheapestShipment()

        assert result == [], "no order should be made: {}".format(result)        