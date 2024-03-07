import math
import numpy as np
import ruleTools
import objectHelperTools as oHT

line = "________________________________________________________________________\n"


class Item:

    def __init__(self, name: str, weight: float, cost: tuple = (0,"gp"), category:str = "Misc"):
        self.name = name
        self.key_name = oHT.name_to_key(self.name)
        self.cost = cost
        self.weight = weight
        self.amount = 0
        self.type = category

        # None Objects

        self.weapon_stats = {
            "damage_dice": ruleTools.Dice(1, 4),
            "damage_type": None,
            "properties": None,
            "weapon_class": None
        }

    def __str__(self):
        object_type = "Item Type | "

        types = self.get_type()
        for i in range(len(types)):
            object_type += types[i] + ", "
        object_type = object_type.rstrip(", ")
        object_type += "\n"

        name = "Name      | " + self.get_name().replace("_", " ") + '\n'
        cost = "Cost      | " + str(self.get_cost()[0]) + " " + self.get_cost()[1] + '\n'
        weight = "Weight    | " + str(self.get_weight()) + " lbs" + '\n'
        amount = "Amount    | " + str(self.get_amount())  + "x" + '\n'

        return line + object_type + name + cost + weight + amount + line

    def get_name(self):
        """
        :return: str
        """
        return self.name

    def get_key_name(self):
        return self.key_name

    def get_amount(self):
        """
        :return: int
        """
        return self.amount

    def get_weight(self):
        """
        :return: float
        """
        return self.weight

    def get_cost(self):
        """
        :return: tuple
        """
        return self.cost

    def get_type(self):
        """
        :return: list[str]
        """
        return self.type

    def get_damage_dice(self):
        """
        :return: dice
        """
        return self.weapon_stats["damage_dice"]

    def get_damage_type(self):
        """
        :return: str
        """
        return self.weapon_stats["damage_type"]

    def get_weapon_class(self):
        """
        :return: str
        """
        return self.weapon_stats["weapon_class"]

    def get_properties(self):
        """
        :return: list[str]
        """
        return self.weapon_stats["properties"]

    # ___________________________________________________________________

    def update_amount(self, new_amount):
        self.amount = new_amount

    def add_amount(self,amount_added):
        self.amount += amount_added

    def subtract_amount(self,amount_subtracted:int):

        if self.amount < amount_subtracted:
            raise ValueError("Amount subtracted is less than amount had")
        else:
            self.amount -= amount_subtracted


class Weapon(Item):
    def __init__(self,name: str, weight: float, cost: tuple, damage_dice: tuple,
                 damage_type: str, properties: list[str], weapon_class: str):
        super().__init__(name, weight, cost)

        self.type = "Weapon"
        self.weapon_stats = {
            "damage_dice": ruleTools.Dice(damage_dice[0], damage_dice[1]),
            "damage_type": damage_type,
            "properties": properties,
            "weapon_class": weapon_class
        }

    def __str__(self):
        weapon_class = "Class      | " + self.get_weapon_class() + "\n"
        name = "Name       | " + self.name.replace("_", " ") + '\n'
        cost = "Cost       | " + str(self.cost[0]) + " " + self.cost[1] + '\n'
        damage = "Damage     | " + str(self.get_damage_dice()) + " " + self.get_damage_type() + '\n'
        weight = "Weight     | " + str(self.weight) + " lbs" + '\n'
        properties = "Properties | "
        existing_properties = self.get_properties()
        for i in range(len(existing_properties)):
            properties += existing_properties[i] + ", "
        properties = properties.rstrip(", ")
        properties += "\n"
        return line + weapon_class + name + cost + damage + weight + properties + line
