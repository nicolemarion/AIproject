import sqlite3
import csv
class InventoryDB:

    # inventorydb constructor
    def __init__(self):
        # change to your directory
        self.filename = "/Users/nicolemarion/Downloads/T&L Project/inventory.db"
        self.csvfilename = "/Users/nicolemarion/Downloads/T&L Project/target_inventory.csv"

        table_names = self.get_table_names()
        if not "Inventory" in table_names:
            self.create_inventory_table()

    # return table names in database
    def get_table_names(self):
        con = sqlite3.connect(self.filename)
        cur = con.cursor()        
        res = cur.execute("SELECT name FROM sqlite_master")
        table_names = [x[0] for x in res.fetchall()]
        con.close()
        return table_names
    
    # create inventory table and read data from csv file into it
    def create_inventory_table(self):
        con = sqlite3.connect(self.filename)
        cur = con.cursor()            
        sqlstr = "CREATE TABLE Inventory ( \
                    ItemNumber INTEGER, \
                    Item TEXT, \
                    NumberItems INTEGER, \
                    Location INTEGER)"
        cur.execute(sqlstr)
        fields = []
        data = []

        #reading from csv file
        with open(self.csvfilename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)  
            for row in csvreader:
                data.append(row)

        # Use executemany to insert data into the table
        cur.executemany("INSERT INTO Inventory (ItemNumber, Item, NumberItems, Location) VALUES (?, ?, ?, ?)", data)
        
        # Commit changes and close connection
        con.commit()
        con.close()

    # return all information from Inventory table 
    def get_inventory_data(self):
        data = []
        con = sqlite3.connect(self.filename)
        cur = con.cursor()        
        res = cur.execute("SELECT * FROM Inventory")
        rows = res.fetchall()
        for row in rows:
            data.append(row)  # Append each row (as a tuple) to the data list
        return data