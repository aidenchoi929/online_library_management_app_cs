from library_tree import *
from library import Book, Periodical, Audiobook

def test_search_items_by_author():
    library_tree = LibraryTree()

    book1 = Book("B001", "Book", "Book 1", "Fiction", "English", "Author A", 2000)
    book2 = Book("B002", "Book", "Book 2", "Non-Fiction", "English", "Author B", 2010)
    periodical1 = Periodical("P001", "Periodical", "Periodical 1", "Magazine", "English", "Author C", 2020)
    audiobook1 = Audiobook("A001", "Audiobook", "Audiobook 1", "Fiction", "English", "Author A", 2015, "MP3")

    library_tree.insert(book1)
    library_tree.insert(book2)
    library_tree.insert(periodical1)
    library_tree.insert(audiobook1)

    table, author_exists = library_tree.search_items_by_author("Author A")
    expected_table = [
        ["Audiobook", "A001", "Audiobook 1", "Fiction", "English", "Author A", 2015, "MP3"],
        ["Book", "B001", "Book 1", "Fiction", "English", "Author A", 2000, "N/A"]
    ]
    assert author_exists, "Expected author_exists to be True for Author A"
    assert table == expected_table, f"Expected table to be {expected_table}, but got {table}"

    table, author_exists = library_tree.search_items_by_author("Nonexistent Author")
    assert not author_exists, "Expected author_exists to be False for Nonexistent Author"
    assert table == [], f"Expected table to be empty for Nonexistent Author, but got {table}"

    print("All tests passed successfully.")

test_search_items_by_author()

