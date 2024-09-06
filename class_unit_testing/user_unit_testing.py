#unit testing for user.py
from user import *

def run_tests():
    user = User('John', 'Doe', 'johndoe', 'password123')
    assert user.first_name == 'John', f"Expected 'John', got {user.first_name}"
    assert user.last_name == 'Doe', f"Expected 'Doe', got {user.last_name}"
    assert user.username == 'johndoe', f"Expected 'johndoe', got {user.username}"
    assert user.password == 'password123', f"Expected 'password123', got {user.password}"
    print("User tests passed")

    borrower = Borrower('Jane', 'Doe', 'janedoe', 'password456', '123456789')
    assert borrower.first_name == 'Jane', f"Expected 'Jane', got {borrower.first_name}"
    assert borrower.last_name == 'Doe', f"Expected 'Doe', got {borrower.last_name}"
    assert borrower.username == 'janedoe', f"Expected 'janedoe', got {borrower.username}"
    assert borrower.password == 'password456', f"Expected 'password456', got {borrower.password}"
    assert borrower.account_number == '123456789', f"Expected '123456789', got {borrower.account_number}"
    print("Borrower tests passed")

    administrator = Administrator('Admin', 'User', 'adminuser', 'adminpass')
    assert administrator.first_name == 'Admin', f"Expected 'Admin', got {administrator.first_name}"
    assert administrator.last_name == 'User', f"Expected 'User', got {administrator.last_name}"
    assert administrator.username == 'adminuser', f"Expected 'adminuser', got {administrator.username}"
    assert administrator.password == 'adminpass', f"Expected 'adminpass', got {administrator.password}"
    print("Administrator tests passed")

if __name__ == '__main__':
    run_tests()
