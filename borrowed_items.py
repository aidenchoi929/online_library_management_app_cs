#Represents each rental transaction by borrowers, stored in list
class Rent:
    def __init__(self, account_number, item, date_borrowed, return_date, late_charge=0):
        self.account_number = account_number
        self.item = item
        self.date_borrowed = date_borrowed
        self.return_date = return_date
        self.late_charge = late_charge

    def to_dict(self):
        return {
            'account_number': self.account_number,
            'item_id': self.item.ID,
            'date_borrowed': self.date_borrowed,
            'return_date': self.return_date,
            'late_charge': self.late_charge
        }

#Add rent to the list, return rent, get rental transaction list(Each rent list)
class RentList:
    def __init__(self, account_number):
        self.account_number = account_number
        self.rents = []

    def add_rent(self, rent):
        self.rents.append(rent)

    def return_rent(self, item_id):
        for rent in self.rents:
            if rent.item.ID == item_id:
                self.rents.remove(rent)
                return rent
        return None

    def get_rents(self):
        return self.rents
