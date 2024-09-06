from user import *
from borrower_list import *

def run_tests():
    borrower_list = BorrowerList()

    borrower1 = Borrower("John", "Doe", "johndoe", "password1", "johndoe0930")
    borrower2 = Borrower("Jane", "Smith", "janesmith", "password2", "janesmith0929")
    borrower3 = Borrower("Alice", "Johnson", "alicejohnson", "password3", "alicejohnson0921")

    borrower_list.append(borrower1)
    borrower_list.append(borrower2)
    borrower_list.append(borrower3)

    found_borrower = borrower_list.find("janesmith")
    assert found_borrower is not None and found_borrower.username == "janesmith", "Find method failed"

    assert borrower_list.delete("johndoe"), "Delete method failed"
    assert borrower_list.delete("nonexistentuser") is False, "Delete method failed"

    borrowers = list(borrower_list)
    assert len(borrowers) == 2, "Iterator method failed"
    assert all(borrower.username in ["janesmith", "alicejohnson"] for borrower in borrowers), "Iterator method failed"

    print("All tests passed successfully.")

if __name__ == "__main__":
    run_tests()