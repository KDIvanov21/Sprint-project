class Asset:
    def __init__(self, asset_type, balance):
        self.asset_type = asset_type
        self.balance = balance
 
    def transfer(self, amount, to):
        
        print(f"Transferring {amount} {self.asset_type} to {to}")
        self.balance -= amount
 
 
class Inheritor:
    def __init__(self, name, relationship, contact_info):
        self.name = name
        self.relationship = relationship
        self.contact_info = contact_info
 
    def notify(self, amount, asset_type):
        print(f"{self.name} has been notified of inheriting {amount} {asset_type}.")
 
 
class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.assets = []
        self.inheritors = []
 
    def add_asset(self, asset_type, initial_balance):
        self.assets.append(Asset(asset_type, initial_balance))
 
    def transfer_asset(self, amount, asset_type, to):
        for asset in self.assets:
            if asset.asset_type == asset_type:
                asset.transfer(amount, to)
                self.notify_inheritor(amount, asset_type, to)
                return
        print(f"Asset type not found: {asset_type}")
 
    def add_inheritor(self, name, relationship, contact_info):
        self.inheritors.append(Inheritor(name, relationship, contact_info))
 
    def remove_inheritor(self, name):
        self.inheritors = [inheritor for inheritor in self.inheritors if inheritor.name != name]
 
    def display_assets(self):
        print(f"User: {self.username}'s Assets:")
        for asset in self.assets:
            print(f" - {asset.asset_type}: {asset.balance}")
 
    def display_inheritors(self):
        print(f"User: {self.username}'s Inheritors:")
        for inheritor in self.inheritors:
            print(f" - {inheritor.name} ({inheritor.relationship}): {inheritor.contact_info}")
 
    def notify_inheritor(self, amount, asset_type, to):
        for inheritor in self.inheritors:
            if inheritor.relationship == "Inherits" and inheritor.contact_info == to:
                inheritor.notify(amount, asset_type)
                return
            
def print_menu():
    print("1. Add Asset")
    print("2. Transfer Asset")
    print("3. Add Inheritor")
    print("4. Remove Inheritor")
    print("5. Display Assets")
    print("6. Display Inheritors")
    print("0. Exit")
 
 
user = User("JohnDoe", "password123", "john.doe@email.com")
user.add_asset("Bitcoin", 5.0)
user.add_asset("Ethereum", 10.0)
user.add_inheritor("Alice", "Inherits", "Alice's contact")
 
while True:
    print_menu()
    choice = input("Enter your choice: ")
 
    if choice == "1":
        asset_type = input("Enter asset type: ")
        initial_balance = float(input("Enter initial balance: "))
        user.add_asset(asset_type, initial_balance)
    elif choice == "2":
        asset_type = input("Enter asset type to transfer: ")
        amount = float(input("Enter transfer amount: "))
        to = input("Enter recipient: ")
        user.transfer_asset(amount, asset_type, to)
    elif choice == "3":
        name = input("Enter inheritor name: ")
        relationship = input("Enter relationship: ")
        contact_info = input("Enter contact information: ")
        user.add_inheritor(name, relationship, contact_info)
    elif choice == "4":
        name_to_remove = input("Enter inheritor name to remove: ")
        user.remove_inheritor(name_to_remove)
    elif choice == "5":
        user.display_assets()
    elif choice == "6":
        user.display_inheritors()
    elif choice == "0":
        break
    else:
        print("Invalid choice. Please try again.")