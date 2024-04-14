# Inventory class for target inventory
class Inventory:
    typeList = []
    def __init__(self, item_number, item, number_items, location):
        self.item_number = item_number
        self.item = item
        self.number_items = number_items
        self.location = location
        