import sys
from PyQt6.QtWidgets import (QMainWindow, QApplication,
    QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QTreeWidget, QListWidget, QTreeWidgetItem, QPushButton, QInputDialog
)
from PyQt6.QtCore import Qt
from inventory import Inventory
from inventorydb import InventoryDB

#set the mainwindow
class MainWindow(QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()

        self.inventory_list = []

        self.setWindowTitle("Target Inventory")

        self.treeWidget = QTreeWidget()
        self.treeWidget.setColumnCount(4)
        self.treeWidget.setHeaderLabels(["Item", "Item Number", "Number of Items", "Location"])
        self.item_number = QTreeWidgetItem(self.treeWidget)
        self.item = QTreeWidgetItem(self.treeWidget)
        self.number_items = QTreeWidgetItem(self.treeWidget)
        self.location = QTreeWidgetItem(self.treeWidget)

        self.update_btn = QPushButton("Update Shipment")
        self.update_btn.clicked.connect(self.update_shipment)
        self.add_btn = QPushButton("Add Shipment")
        self.add_btn.clicked.connect(self.add_shipment)
        self.delete_btn = QPushButton("Delete Shipment")
        self.delete_btn.clicked.connect(self.delete_shipment)

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.treeWidget)

        right_layout = QGridLayout()
        right_layout.addWidget(self.update_btn, 0, 2)
        right_layout.addWidget(self.add_btn, 1, 2)
        right_layout.addWidget(self.delete_btn, 2, 2)

        #general layout
        generalLayout = QHBoxLayout()
        generalLayout.addLayout(left_layout)
        generalLayout.addLayout(right_layout)
        mainLayoutWidget = QWidget()
        mainLayoutWidget.setLayout(generalLayout)
        self.setCentralWidget(mainLayoutWidget)

        self.resize(500, 300)

        self.load_inventory_data()

    # load inventory data into tree widget
    def load_inventory_data(self):
        self.inventorydb = InventoryDB()  
        data = self.inventorydb.get_inventory_data()

        for entry in data:
            inventory = Inventory(entry[0], entry[1], entry[2], entry[3])
            self.inventory_list.append(inventory)

            # Update the QTreeWidgetItem for each item
            self.item_number = QTreeWidgetItem([str(inventory.item_number)])
            self.treeWidget.addTopLevelItem(self.item)

            self.item = QTreeWidgetItem([str(inventory.item)])
            self.treeWidget.addTopLevelItem(self.item)

            self.number_items = QTreeWidgetItem([str(inventory.number_items)])
            self.treeWidget.addTopLevelItem(self.number_items)

            self.location = QTreeWidgetItem([str(inventory.location)])
            self.treeWidget.addTopLevelItem(self.location)

        self.update_chart()
    
    #update shipment function
    def update_chart(self):
        # Clear the treeWidget
        self.treeWidget.clear()

        # Re-populate the tree widget with the updated inventory list
        for inventory in self.inventory_list:
            item = QTreeWidgetItem([str(inventory.item), str(inventory.item_number), 
                                     str(inventory.number_items), str(inventory.location)])
            self.treeWidget.addTopLevelItem(item)

    def update_shipment(self):
        selected_item = self.treeWidget.currentItem()
        if selected_item is not None:
            index = self.treeWidget.indexOfTopLevelItem(selected_item)
            if index != -1:
                # Retrieve existing data
                existing_inventory = self.inventory_list[index]
                # Display a dialog pre-filled with existing data
                new_item, ok1 = QInputDialog.getText(self, "Update Shipment", "Enter new item name:", text=existing_inventory.item)
                if ok1:
                    new_item_number, ok2 = QInputDialog.getText(self, "Update Shipment", "Enter new item number:", text=str(existing_inventory.item_number))
                    if ok2:
                        new_number_items, ok3 = QInputDialog.getInt(self, "Update Shipment", "Enter new number of items:", value=existing_inventory.number_items)
                        if ok3:
                            new_location, ok4 = QInputDialog.getText(self, "Update Shipment", "Enter new location:", text=str(existing_inventory.location))
                            if ok4:
                                # Update the existing inventory with new data
                                existing_inventory.item_number = new_item_number
                                existing_inventory.item = new_item
                                existing_inventory.number_items = new_number_items
                                existing_inventory.location = new_location
                                # Update the display
                                self.update_chart()
    #add shipment function
    def add_shipment(self):
       # Create a dialog to get shipment information
        item_number, ok = QInputDialog.getText(self, "Add Shipment", "Enter item name:")
        if ok:
            item, ok1 = QInputDialog.getInt(self, "Add Shipment", "Enter item number:")
            if ok1:
                number_items, ok2 = QInputDialog.getInt(self, "Add Shipment", "Enter number of items:")
                if ok2:
                    location, ok3 = QInputDialog.getText(self, "Add Shipment", "Enter location:")
                    if ok3:
                        # Create Inventory object with the provided information
                        inventory = Inventory(item, item_number, number_items, location)
                        # Add the inventory to the list and update the display
                        self.inventory_list.append(inventory)
                        self.update_chart()
        
    #delete shipment function
    def delete_shipment(self):
        selected_item = self.treeWidget.currentItem()
        if selected_item is not None:
            # Find the index of the selected item in the tree widget
            index = self.treeWidget.indexOfTopLevelItem(selected_item)
            if index != -1:
                # Remove the selected item from both the inventory list and the tree widget
                del self.inventory_list[index]
                self.treeWidget.takeTopLevelItem(index)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec() 