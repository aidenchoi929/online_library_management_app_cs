#libraries
from collections import defaultdict
import time
from datetime import datetime, timedelta
from tabulate import tabulate
import csv
import getpass

#classes
from user import User, Borrower, Administrator
from library import Library, Book, Periodical, Audiobook
from borrowed_items import RentList, Rent
from library_tree import LibraryTree
from borrower_list import BorrowerList

#DB location for rent status/library items/borrower info
rent_file_path = 'files/rents.csv'
libraries_file_path = 'files/libraries.csv'
borrower_file_path =  'files/borrowers.csv'

#main function
def main():
    global borrower_list
    global library_tree
    global rents
    library_tree = load_libraries(libraries_file_path)
    rents = load_rents(rent_file_path)
    borrower_list = load_borrowers(borrower_file_path)
    # First name, Last name, User name, Password
    admin = Administrator('Aiden', 'Choi', 'admin', 'password')  # Registered administrator account(Can only be modified in code)

    apply_rents(borrower_list, rents)

    while True:
        print("\nWelcome to SOLA! Are you a borrower of administrator? ")
        print("1. Item borrower")
        print("2. System administrator")
        print("3. End program")
        choice = input("Please enter your menu choice(1~3): ")

        if choice == '1':
            borrower_login()
        elif choice == '2':
            admin_login(admin)
        elif choice == '3':
            print("\nThank you for using SOLA, see you!")
            break
        else:
            print("\nWrong input, please try again between 1~3")

def load_borrowers(file_path):
    borrowers = BorrowerList()
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            borrower = Borrower(row['first name'], row['last name'], row['username'], row['password'], row['account number'])
            borrowers.append(borrower)
    return borrowers            

def load_rents(filepath):
    rents = []
    with open(filepath, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            item = library_tree.search_by_id(row['item_id'])
            if item:  # Only adds item when it exists in the library tree
                return_date = datetime.strptime(row['return_date'], "%Y-%m-%d")
                if return_date < datetime.now():
                    late_charge = 10
                else:
                    late_charge = int(row['late_charge']) if row['late_charge'] else 0
                rent = Rent(
                    account_number=row['account_number'],
                    item=item,
                    date_borrowed=row['date_borrowed'],
                    return_date=row['return_date'],
                    late_charge=late_charge
                )
                rents.append(rent)
    update_rent_file(filepath, rents)
    return rents

def apply_rents(borrower_list, rents):
    for rent in rents:
        borrower = borrower_list.find(rent.account_number)
        if borrower:
            borrower.rents.append(rent)

def update_rent_file(file_path, rents):
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['account_number', 'item_id', 'date_borrowed', 'return_date', 'late_charge']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for rent in rents:
            writer.writerow(rent.to_dict())

def borrower_login():
    username = input("Please enter username: ")
    password = getpass.getpass("Please enter password: ")

    borrower = borrower_list.find(username)
    
    if borrower and borrower.password == password:
        borrower_menu(borrower)
    else:
        print("\nAttempt failed. Please try again.\n\n")

def admin_login(admin):
    username = input("Please enter username: ")
    password = getpass.getpass("Please enter password: ")
    if username == admin.username and password == admin.password:
        admin_menu(admin)
    else:
        print("\nAttempt failed. Please try again.")

def borrower_menu(borrower):
    while True:
        print(f"\nWelcome to SOLA's borrower menu, {borrower.first_name} {borrower.last_name}")
        print("1. Borrower profile")
        print("2. Rent and return")
        print("3. Library Search")
        print("4. Check late charge")
        print("5. Exit")
        choice = input("\nWhat are you looking for?: ")

        if choice == '1':
            delete_flag = borrower_profile(borrower)
            if delete_flag:
                break
        elif choice == '2':
            rent_and_return(borrower)
        elif choice == '3':
            library_search()
        elif choice == '4':
            check_late_charge(borrower)
        elif choice == '5':
            break
        else:
            print("\nAttempt failed. Please try again.")

def admin_menu(admin):
    while True:
        print(f"\nWelcome to SOLA's admin menu, {admin.first_name} {admin.last_name}")
        print("1. Administrator profile")
        print("2. Manage library items")
        print("3. Access to borrower database")
        print("4. Exit")
        choice = input("\nWhat are you looking for?: ")

        if choice == '1':
            admin_profile(admin)
        elif choice == '2':
            manage_library_items()
        elif choice == '3':
            check_rent_status()
        elif choice == '4':
            break
        else:
            print("\nAttempt failed. Please try again.")

def manage_library_items():
    while True:
        print("\n1. Display all items with info")
        print("2. Search item with keyword")
        print("3. Add item")
        print("4. Delete item")
        print("5. Back to the main")
        choice = input("Select menu: ")

        if choice == '1':
            display_all_items()
        elif choice == '2':
            search_item_by_keyword()
        elif choice == '3':
            add_item()
        elif choice == '4':
            delete_item()
        elif choice == '5':
            break
        else:
            print("\nAttempt failed. Please try again.")       

def delete_item():
    title = input("\nPlease enter item title to delete: ")
    item = library_tree.search_by_title(title)

    if item:
        # Delete items
        library_tree.delete(item)
        print(f"\n'{title}' has been successfully deleted!")

        # Overwrite csv file
        update_libraries_csv(library_tree, libraries_file_path)
    else:
        print(f"\n'{title}' is not in our library.")

def update_libraries_csv(library_tree, file_path):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['What', 'ID', 'Type', 'Title', 'Category', 'Language', 'Author', 'Year Published', 'Audio Format'])
        
        def inorder_traversal(node):
            if node:
                inorder_traversal(node.left)
                item = node.library_item
                writer.writerow([
                    type(item).__name__,
                    item.ID,
                    item.type,
                    item.title,
                    item.category,
                    item.language,
                    item.author,
                    item.year_published,
                    item.audio_format if isinstance(item, Audiobook) else 'N/A'
                ])
                inorder_traversal(node.right)
        
        inorder_traversal(library_tree.root)

def add_item():
    item_types = [Book, Audiobook, Periodical]
    while True:
        print("\nWhich type of item would you like to add?:")
        for i, item_type in enumerate(item_types, 1):
            print(f"{i}. {item_type.__name__}")
        try:
            item_type_index = int(input()) - 1
            if not (0 <= item_type_index < len(item_types)):
                raise ValueError
            item_type = item_types[item_type_index]
            break
        except ValueError:
            print("\nWrong input, please try again between 1~3")
    
    id = input("Please enter item's ID: ")
    type = input("Please enter ID type(ISBN or ISSN): ")
    title = input("Please enter item's title: ")
    category = input("Please enter item's category: ")
    language = input("Please enter item's language: ")
    author = input("Please enter item's author: ")
    year_published = input("Please enter item's published year(YYYY): ")
    audio_format = ""
    if item_type == Audiobook:
        audio_format = input("Please enter audio format type: ")

    # Inserts item to library tree
    new_item = item_type(id, type, title, category, language, author, year_published, audio_format)
    library_tree.insert(new_item)

    # Update csv file
    with open(libraries_file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([item_type.__name__, id, type, title, category, language, author, year_published, audio_format])

    print("\nItem has been added to the library.")

def check_rent_status():
    while True:
        print("\n1. Display borrowed items")
        print("2. Check late charge")
        print("3. Display all borrowers in DB")
        print("4. Export borrower DB")
        print("5. Back to the main")
        choice = input("Select menu: ")

        if choice == '1':
            print_all_rent_info()
        elif choice == '2':
            check_all_borrowers_late_charge()
        elif choice == '3':
            display_all_borrowers_info()
        elif choice == '4':
            export_borrower_database()
        elif choice == '5':
            break
        else:
            print("Wrong input. Please try again.")

def export_borrower_database():
    headers = ["First Name", "Last Name", "Username", "Account Number"]
    table = []
    for borrower in borrower_list:
        table.append([
            borrower.first_name, 
            borrower.last_name, 
            borrower.username, 
            borrower.account_number
        ])
    filepath = input("\nPlease enter file path to store borrowers DB with preferred file name(.csv): ")
    try:
        with open(filepath, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(table)
        print("\nCompleted: Borrower database has been exported to:", filepath)
    except FileNotFoundError:
        print(f"\nError: The file path '{filepath}' is not valid.")
    except PermissionError:
        print(f"\nError: Permission denied when trying to write to '{filepath}'.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

def display_all_borrowers_info():
    table = []
    for borrower in borrower_list:
        table.append([borrower.first_name, borrower.last_name, borrower.username, borrower.password, borrower.account_number])
    headers = ["First Name", "Last Name", "Username", "Password", "Account Number"]
    print(tabulate(table, headers, tablefmt="pretty"))

def print_all_rent_info():
    table = []
    for rent in rents:
        table.append([rent.account_number, rent.item.title, rent.date_borrowed, rent.return_date, rent.late_charge])
    headers = ["Account Number", "Title Name", "Date Borrowed", "Return Date", "Late Charge"]
    print(tabulate(table, headers, tablefmt="pretty"))

def check_all_borrowers_late_charge():
    late_charges = defaultdict(int)
    for rent in rents:
        if rent.late_charge > 0:
            late_charges[rent.account_number] += rent.late_charge

    table = [[account_number, late_charge] for account_number, late_charge in late_charges.items() if late_charge > 0]
    headers = ["Account Number", "Total Late Charge"]
    if table:
        print(tabulate(table, headers, tablefmt="pretty"))
    else:
        print("\nCurrently there is no borrowers with late charges.")

def borrower_profile(borrower):
    while True:
        print("\nWelcome to SOLA's borrower menu")
        print("1. Modify profile info")
        print("2. Display profile info")
        print("3. Delete profile")
        print("4. Back to the main")
        choice = input("Select menu: ")

        if choice == '1':
            modify_profile(borrower)
        elif choice == '2':
            display_profile(borrower)
        elif choice == '3':
            delete_flag = delete_profile(borrower)
            if delete_flag:
                return True
        elif choice == '4': 
            break
        else:
            print("\nWrong input, please try again.")

def admin_profile(admin):
    while True:
        print("\nAdministrator profile")
        print("1. Modify profile info")
        print("2. Display profile info")
        print("3. Back to the main")
        choice = input("Select menu: ")

        if choice == '1':
            modify_profile(admin)
        elif choice == '2':
            display_admin_profile(admin)
        elif choice == '3':
            break
        else:
            print("\nWrong input, please try again.")

def modify_profile(user):
    print("\nModify profile info")
    user.first_name = input(f"First name ({user.first_name}): ") or user.first_name
    user.last_name = input(f"Last name ({user.last_name}): ") or user.last_name
    user.password = getpass.getpass(f"Password ({'*' * len(user.password)}): ") or user.password
    print("\nProfile has been updated.")
    update_borrowers_file(borrower_file_path)

def update_borrowers_file(file_path):
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['first name', 'last name', 'username', 'password', 'account number']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for borrower in borrower_list:
            writer.writerow({'first name': borrower.first_name, 'last name': borrower.last_name, 'username': borrower.username, 'password': borrower.password, 'account number': borrower.account_number})

def display_profile(user):
    print("\nDisplay profile info")
    table = [["First name:", user.first_name], ["Last name:", user.last_name], ["User name:", user.username], ["Account number:", user.account_number]]
    print(tabulate(table, tablefmt="plain"))

def display_admin_profile(admin):
    print("\nDisplay profile info")
    table = [["First name:", admin.first_name], ["Last name:", admin.last_name], ["User name:", admin.username]]
    print(tabulate(table, tablefmt="plain"))

def delete_profile(borrower):
    password = getpass.getpass("Please enter password to delete your profile: ")
    if password == borrower.password:
        borrower_list.delete(borrower.username)
        print("\nProfile has been deleted.")
        update_borrowers_file(borrower_file_path)  #CSV file updates after successful deletion of profile
        return True
    else:
        print("\nIncorrect password. Profile has not been deleted.")
        return False

def rent_and_return(borrower):
    while True:
        print("\nRent & Return")
        print("1. Borrow item")
        print("2. Return item")
        print("3. Check return date")
        print("4. Back to the main")
        choice = input("Select menu: ")

        if choice == '1':
            rent_item(borrower)
        elif choice == '2':
            return_item(borrower)
        elif choice == '3':
            display_borrowed_items(borrower)
        elif choice == '4':
            break
        else:
            print("\nWrong input, please try again.")

def rent_item(borrower):
    # Check late charge prior to rent for borrower
    for rent in rents:
        if rent.account_number == borrower.account_number and rent.late_charge > 0:
            print("\nCannot rent due to unpaid late charge.")
            return

    title = input("\nPlease enter the item title to borrow items: ")
    item = library_tree.search_by_title(title)
    
    if item:
        # Checks whether the item is borrowed or available
        for rent in rents:
            if rent.item.ID == item.ID:
                print(f"\n'{title}' is already borrowed.")
                return

        rent_count = sum(1 for rent in rents if rent.account_number == borrower.account_number)
        if rent_count >= 8:
            print("\nYou have reached the maximum limit for rent.")
            return

        date_borrowed = time.strftime("%Y-%m-%d")
        return_date = time.strftime("%Y-%m-%d", time.localtime(time.time() + 14 * 86400))
        new_rent = Rent(borrower.account_number, item, date_borrowed, return_date)
        rents.append(new_rent)
        update_rent_file(rent_file_path, rents)
        print(f"\n'{title}' has been successfully borrowed.")
    else:
        print(f"\n'{title}' is not in the library.")

def return_item(borrower):
    title = input("\nPlease enter the item title to return: ")
    for rent in rents:
        if rent.item.title == title:
            if rent.account_number != borrower.account_number:
                print("\nThe item is already available at the moment.")
                return
            if rent.late_charge > 0:
                print("\nCannot return, Please pay the unpaid late charge.")
                return
            rents.remove(rent)
            update_rent_file(rent_file_path, rents)
            print(f"\n'{title}' has been successfully returned.")
            return
    print(f"\n'{title}' does not exist in your borrowed item list.")

def display_borrowed_items(borrower):
    print("\nBorrowed items")
    borrowed_items = [(rent.item, rent.return_date) for rent in rents if rent.account_number == borrower.account_number]
    if borrowed_items:
        headers = ["Title", "Expected return date"]
        table = [(item.title, return_date) for item, return_date in borrowed_items]
        print(tabulate(table, headers, tablefmt="pretty"))
    else:
        print("You do not have any borrowed items.")

def library_search():
    while True:
        print("\nLibrary search")
        print("1. Display entire library inventory")
        print("2. Search item by keyword")
        print("3. Search item by author")
        print("4. Back to the main")
        choice = input("Select menu: ")

        if choice == '1':
            display_all_items()
        elif choice == '2':
            search_item_by_keyword()
        elif choice == '3':
            search_items_by_author()
        elif choice == '4':
            break
        else:
            print("\nWrong input, please try again.")

def display_all_items():
    print("\nDisplay all items")
    table = []
    def inorder_traversal(node):
        if node:
            inorder_traversal(node.left)
            item = node.library_item
            if isinstance(item, Audiobook):
                item_type = "Audiobook"
                audio_format = item.audio_format
            elif isinstance(item, Book):
                item_type = "Book"
                audio_format = "N/A"
            elif isinstance(item, Periodical):
                item_type = "Periodical"
                audio_format = "N/A"
            table.append([item_type, item.ID, item.type, item.title, item.category, item.language, item.author, item.year_published, audio_format])
            inorder_traversal(node.right)
    inorder_traversal(library_tree.root)
    headers = ["What", "ID", "Type", "Title", "Category", "Language", "Author", "Year Published", "Audio Format"]
    print(tabulate(table, headers, tablefmt="pretty", missingval="N/A"))

def load_libraries(file_path):
    libraries = LibraryTree()
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['What'] == 'Book':
                item = Book(row['ID'], row['Type'], row['Title'], row['Category'], row['Language'], row['Author'], row['Year Published'])
            elif row['What'] == 'Periodical':
                item = Periodical(row['ID'], row['Type'], row['Title'], row['Category'], row['Language'], row['Author'], row['Year Published'])
            elif row['What'] == 'Audiobook':
                item = Audiobook(row['ID'], row['Type'], row['Title'], row['Category'], row['Language'], row['Author'], row['Year Published'], row.get('Audio Format', ''))
            libraries.insert(item)
    return libraries

def search_item_by_keyword():
    keyword = input("\nEnter keyword: ").lower()
    print(f"\nKeywords with '{keyword}' will be shown...")
    table = []
    
    def inorder_search(node):
        if node:
            inorder_search(node.left)
            item = node.library_item
            if (keyword in item.ID.lower() or
                keyword in item.audio_format.lower() or
                keyword in item.type.lower() or
                keyword in item.title.lower() or
                keyword in item.category.lower() or
                keyword in item.language.lower() or
                keyword in item.author.lower() or
                keyword in item.year_published.lower()):
                if isinstance(item, Audiobook):
                    item_type = "Audiobook"
                    audio_format = item.audio_format
                elif isinstance(item, Book):
                    item_type = "Book"
                    audio_format = "N/A"
                elif isinstance(item, Periodical):
                    item_type = "Periodical"
                    audio_format = "N/A"
                table.append([item_type, item.ID, item.title, item.category, item.language, item.author, item.year_published, audio_format])
            inorder_search(node.right)
    inorder_search(library_tree.root)
    headers = ["Type", "ID", "Title", "Category", "Language", "Author", "Year Published", "Audio Format"]
    print(tabulate(table, headers, tablefmt="pretty", missingval="N/A"))

def search_items_by_author():
    author = input("\nPlease enter the author: ").lower()
    table, author_exists = library_tree.search_items_by_author(author)

    if not author_exists:
        print("\nThe author does not exist in the library.")
    else:
        headers = ["Type", "ID", "Title", "Category", "Language", "Author", "Year Published", "Audio Format"]
        print(tabulate(table, headers, tablefmt="pretty", missingval="N/A"))

def pay_late_charge_and_return_items(borrower):
    response = input("\nWould you like to return an item and pay the unpaid late charge? (yes/no): ")
    if response.lower() == 'yes':
        pay_late_charge(borrower)
        print("\nSuccessfully returned, Unpaid late charge has been cleared as well.")
    else:
        print("\nCancelled.")

def check_late_charge(borrower):
    print("\nCheck late charge")
    late_charges = calculate_late_charges(borrower)
    if late_charges > 0:
        print(f"Current late charge: ${late_charges}.")
        pay_late_charge_and_return_items(borrower)
    else:
        print("You do not have late charge.")

def pay_late_charge(borrower):
    global rents
    new_rents = []
    #Reads "rents.csv" adds items with no late charge to a new list
    with open(rent_file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            if row[0] != borrower.account_number or int(row[4]) == 0:
                rent = Rent(row[0], row[1], row[2], row[3], int(row[4]))
                new_rents.append(rent)

    with open(rent_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for rent in new_rents:
            writer.writerow([rent.account_number, rent.item, rent.date_borrowed, rent.return_date, rent.late_charge])

    rents = new_rents

def calculate_late_charges(borrower):
    late_charges = 0
    current_date = time.strftime("%Y-%m-%d")
    for rent in rents:
        if rent.account_number == borrower.account_number:
            if current_date > rent.return_date:
                late_charges += rent.late_charge
    return late_charges

if __name__ == '__main__':
    main()