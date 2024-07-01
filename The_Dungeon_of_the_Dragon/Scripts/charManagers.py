import numpy as np
import objectsDnD
import objectHelperTools as oHT
import ruleTools


class Inventory:

    def __init__(self, encumberance:ruleTools.Encumbrance):
        self.inventory = {}
        self.money = {
            "cp": 0,
            "sp": 0,
            "ep": 0,
            "gp": 0,
            "pp": 0
        }
        self.order = "name"
        self.reverse= False
        self.encumberance = encumberance

    def update(self):
        mark_for_deletion = []
        for key in self.inventory:
            if self.inventory[key].get_amount() == 0:
                mark_for_deletion += [key]
        for i in range(len(mark_for_deletion)):
            print(self.inventory[mark_for_deletion[i]])
            del self.inventory[mark_for_deletion[i]]
        self.encumberance.update()

    def add_money(self, amount, denominations):
        """
        :param amount: amount to be added. To subtract, set negative
        :param denominations:
        """
        denominations.casefold()
        if np.sign(amount) == -1:
            if self.money[denominations] < amount:
                raise ValueError("Amount subtracted is less than amount had")
        self.money[denominations] += amount

    def add_item(self, key: str, item: objectsDnD.Item, amount=1):
        key = key.casefold()
        if key in self.inventory.keys():  # if item already present, add to amount
            self.encumberance.subtract_weight(self.inventory[key].get_total_weight())
            self.inventory[key].add_amount(amount)
            self.encumberance.add_weight(self.inventory[key].get_total_weight())
        else:
            self.inventory[key] = item
            self.inventory[key].add_amount(amount)
            self.encumberance.add_weight(self.inventory[key].get_total_weight())
        self.update()

        # add to list by type

    def subtract_item(self, key, amount):
        self.encumberance.subtract_weight(self.inventory[key].get_total_weight())
        self.inventory[key].subtract_amount(amount)
        self.encumberance.add_weight(self.inventory[key].get_total_weight())
        if self.inventory[key].get_amount() == 0:
            del self.inventory[key]
        self.update()

    def remove_item(self,key):
        self.encumberance.subtract_weight(self.inventory[key].get_total_weight())
        del self.inventory[key]

    def find_keys_of_item(self, query_item):
        return oHT.regexSearch(query_item, list(self.inventory))

    def set_sorting(self,order:str):
        self.order = order

    def set_reversal(self,reverse:bool):
        self.reverse = reverse

    def get_all_items(self):
        """
        :return: symbol table
        """
        functions = {
            "name": lambda x: x.get_name(),
            "cost": lambda x: x.get_normal_cost(),
            "weight": lambda x: x.get_total_weight(),
            "amount": lambda x: x.get_amount(),
            "type": lambda x: x.get_type(),
        }
        items = list(self.inventory.values())
        key_values = [functions[self.order](item) for item in items]

        new_list = list(zip(items, key_values))

        new_list = sorted(new_list, key=lambda x: x[1], reverse=self.reverse)
        return [i[0] for i in new_list]

    def get_weight(self):
        return self.encumberance.get_weight()

    def get_encumberance_status(self):
        return self.encumberance.get_encumberance_status()

    def get_money(self, denominations=None):
        """

        :param denominations:
        :return: list[cp, sp, ep, gp]
        """
        if denominations is None:
            return [self.money["cp"], self.money["sp"], self.money["ep"], self.money["gp"], self.money["pp"]]
        else:
            return [self.money[denominations]]

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

    def __getitem__(self, item:str):
        item = oHT.name_to_key(item)
        return self.inventory[item]



