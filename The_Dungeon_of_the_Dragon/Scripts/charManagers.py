import numpy as np
import objectsDnD
import Reading
import objectHelperTools as oHT


class Inventory:

    def __init__(self):
        self.inventory = {}
        self.money = {
            "cp": 0,
            "sp": 0,
            "ep": 0,
            "gp": 0,
            "pp": 0
        }

    def add_money(self, amount, denominations):
        """

        :param amount: amount to be added. To subtract, set negative
        :param denominations:
        :return:
        """
        denominations.casefold()
        if np.sign(amount) == -1:
            if self.money[denominations] < amount:
                raise ValueError("Amount subtracted is less than amount had")
        self.money[denominations] += amount

    def get_money(self, denominations=None):
        """

        :param denominations:
        :return: list[cp, sp, ep, gp]
        """
        if denominations is None:
            return [self.money["cp"], self.money["sp"], self.money["ep"], self.money["gp"], self.money["pp"]]
        else:
            return [self.money[denominations]]

    def add_item(self, key: str, item: objectsDnD.Item, amount):
        key = key.casefold()
        if key in self.inventory.keys():  # if item already present, add to amount
            self.inventory[key].add_amount(amount)
        else:
            self.inventory[key] = item
            self.inventory[key].add_amount(amount)

        # add to list by type

    def subtract_item(self, key, amount):
        self.inventory[key].subtract_amount(amount)
        if self.inventory[key].get_amount() == 0:
            del self.inventory[key]

    def get_list_by(self, order:str, reverse=False):
        """
        :param reverse:
        :param function: [name, cost, weight, amount]
        :return: symbol table
        """
        functions = {
            "name": lambda x: x.get_name(),
            "cost": lambda x: x.get_normal_cost(),
            "weight": lambda x: x.get_weight(),
            "amount": lambda x: x.get_amount(),
            "type": lambda x: x.get_amount(),
        }

        key_values = [functions[order](item) for item in list(self.inventory.values())]
        keys = list(self.inventory)
        new_list = list(zip(keys, key_values))
        new_list = sorted(new_list, key=lambda x: x[1], reverse=reverse)

        return [i[0] for i in new_list]

    def find_keys_of_item(self, query_item):
        return oHT.regexSearch(query_item, list(self.inventory))

    def get_items(self, query_item):
        """
        :param query_item:
        :return:
        """
        key_matches = self.find_keys_of_item(query_item)

        item_matches = []  # list[items]
        for key in list(key_matches):
            if key == "":
                item_matches = list(self.inventory.values())
                return sorted(item_matches, key=lambda x: x.get_name())
            else:
                item_matches += [self.inventory[key]]


        return sorted(item_matches, key=lambda x: x.get_name())

    def get_specific_item(self, query_item: str):
        query_item.casefold()
        return self.inventory[query_item]

    def get_all_items(self, order: str = "alphabetical", reverse=False):
        """
        :return: list of all items in order of "order"
        """
        order.casefold()
        orders = {
            "alphabetical": lambda x: x.get_name(),
            "weight": lambda x: x.get_weight(),
            "cost": lambda x: x.get_cost()[0],  # TODO: FIX FOR DENOMINATION
            "amount": lambda x: x.get_amount()
        }
        all_items = self.get_items("")

        return sorted(all_items, key=orders[order], reverse=reverse)




# t = InventoryTypeList()
# t.add_item("key",objectsDnD.Item("1AAAA_pre",0))
# t.add_item("key",objectsDnD.Item("0AAAA_one",0))
# t.add_item("key",objectsDnD.Item("ABAA_two",0))
# t.add_item("key",objectsDnD.Item("AABA_three",0))
#
# test = t.get_all_of_key("key")
# for i in range(len(test)):
#     print(test[i].get_name())
#
# print("_________________")
#
# test = t.get_sorted_tuples()
# print(test[0][1])  # returns all objects of key 0

# inventory = Inventory()
# apple = objectsDnD.Item("apple", 1, category=["Food"])
# pear = objectsDnD.Item("pear", 1)
# ear = objectsDnD.Item("ear", 10, cost=(100, "gp"))
# sword = objectsDnD.Weapon("sword", 10, (10000, "gp"), (1, 4), "piercing", ["Throw"], "Simple")
#
# inventory.add_item(sword.get_name(), sword, 1)
# inventory.add_item(apple.get_name(), apple, 1)
# inventory.add_item(pear.get_name(), pear, 1)
# inventory.add_item(ear.get_name(), ear, 1)
# inventory.add_money(10, "gp")
#
# # listquery = inventory.get_all_of_type("w")
# # for k in range(len(listquery)):
# #     print(listquery[k].get_name())
# #
# # print("Inividual Search: ",inventory.get_items("sw")[0].get_name())
#
# inventory.add_item(sword.get_name(),sword,2)
# inventory.subtract_item("sword",2)
# query = inventory.get_all_items("cost")
# for i in range(len(query)):
#     print(query[i].get_name())
