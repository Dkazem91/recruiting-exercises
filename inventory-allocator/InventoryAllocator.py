"""
This file contains the class InventoryAllocator

Used for computing shipment orders

Author: Daniel Kazemian <Dkazemian@gmail.com>
"""

class InventoryAllocator():
    def __init__(self, orders: dict, warehouses: list, strict=False):
        """
        class init function

        parameters:
        ============================================================
            orders(dictionary): a dictionary containing items to order with key/value of item(str)/amount(int) 
                i.e. {'apple':5}

            warehouses(list): a list of dictionaries composed of 'name' and 'inventory' keys, sorted based on inventory costs, least expensive -> most expensive
                i.e. [
                        {
                            'name': 'warehouse_1:',
                            'inventory': {'apple': 5} 
                        },
                        {
                            'name': 'warehouse_2:',
                            'inventory': {'apple': 6} 
                        }
                    ]
        """
        if strict:
            # check for any bad parameter values
            assert type(orders) is dict, "wrong type: {}".format(orders)
            assert orders, "empty orders: {}".format(orders)

            for item in orders:
                assert type(item) is str, "item should be a string: {}".format(item)

                assert type(orders[item]) is int and orders[item] > 0, "wrong item value: {}, {}".format(item, orders[item])

            assert type(warehouses) is list, "wrong type".format(warehouses)
            assert warehouses, 'empty warehouses: {}'.format(warehouses)

            for warehouse in warehouses:
                assert 'name' in warehouse and 'inventory' in warehouse, "warehouse in list does not contain 'name' and/or 'inventory' key(s): {}".format(warehouse)

                assert type(warehouse['name']) is str, "warehouse name should be a string: {}".format(warehouse['name'])

                assert type(warehouse['inventory']) is dict, "warehouse inventory should be a dictionary: {}".format(warehouse['inventory'])

                for item in warehouse['inventory']:
                    assert type(item) is str, "inventory item is not a string: {}".format(item)
                    assert type(warehouse['inventory'][item]) is int and warehouse['inventory'][item] >= 0, "invalid value for warehouse inventory: {} {}".format(item, warehouse['inventory'][item])

        self.orders = orders
        self.warehouses = warehouses

    def getCheapestShipment(self)->list:
        """
        function that will parse through our orders and return a list of warehouses with the amounts to order from them
        """
        warehouse_orders = {}

        for order_item in self.orders:
            order_amount = self.orders[order_item]

            for warehouse in self.warehouses:
                warehouse_name = warehouse['name']
                warehouse_inventory = warehouse['inventory']

                if order_item in warehouse_inventory and warehouse_inventory[order_item] > 0:
                    # we will order something from this warehouse, make sure we have the name in our warehouse_orders
                    if not warehouse_orders.get(warehouse_name):
                            warehouse_orders[warehouse_name] = {}

                    # update our current order amount based on this warehouse's inventory
                    if warehouse_inventory[order_item] >= order_amount:
                        warehouse_orders[warehouse_name][order_item] = order_amount
                        order_amount = 0
                    else:
                        warehouse_orders[warehouse_name][order_item] = warehouse_inventory[order_item]
                        order_amount -= warehouse_inventory[order_item]
                
                if order_amount == 0:
                    # we have ordered the amount we needed, stop searching warehouses
                    break
            
            if order_amount != 0:
                # an item was not able to be fully ordered, we cannot 100% fulfill our entire order, no allocations 
                return []
        
        return [{name: warehouse_orders[name]} for name in warehouse_orders]
        
        
            



                    


    