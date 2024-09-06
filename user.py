#Super class to Borrower and Administrator
class User:
    def __init__(self, first_name, last_name, username, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password

#Sub class to User, comes with an unique attribute account_number to identify in each rental transaction
class Borrower(User):
    def __init__(self, first_name, last_name, username, password, account_number):
        super().__init__(first_name, last_name, username, password)
        self.account_number = account_number

#Sub class to User, administrator info is registered in main.py(Line 30)
class Administrator(User):
    def __init__(self, first_name, last_name, username, password):
        super().__init__(first_name, last_name, username, password)
