from datetime import datetime
from borrowed_items import *

def run_tests():
    # Mock data for testing
    account_number = 1
    date_borrowed = datetime.now()
    return_date = date_borrowed  # Assume item is returned immediately

    # Assume Book, Audiobook classes are defined in library.py
    class Book:
        def __init__(self, ID):
            self.ID = ID

    class Audiobook:
        def __init__(self, ID):
            self.ID = ID

    # Mock instances
    book1 = Book(1)
    audiobook1 = Audiobook(2)

    rent1 = Rent(account_number, book1, date_borrowed, return_date)
    rent2 = Rent(account_number, audiobook1, date_borrowed, return_date)

    rent_list = RentList(account_number)

    rent_list.add_rent(rent1)
    rent_list.add_rent(rent2)
    assert len(rent_list.get_rents()) == 2, "Add rent method failed"

    returned_rent = rent_list.return_rent(item_id=book1.ID)
    assert returned_rent is not None and returned_rent.item.ID == book1.ID, "Return rent method failed"
    assert len(rent_list.get_rents()) == 1, "Return rent method failed"

    rents = rent_list.get_rents()
    assert len(rents) == 1, "Get rents method failed"
    assert rents[0].item.ID == audiobook1.ID, "Get rents method failed"

    print("All tests passed successfully.")

if __name__ == "__main__":
    run_tests()
