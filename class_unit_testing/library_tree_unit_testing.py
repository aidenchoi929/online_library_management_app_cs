from library_tree import LibraryTree
from library import Book, Periodical, Audiobook

def test_insert_and_search():
    library_tree = LibraryTree()
    book1 = Book("B001", "Book", "Book 1", "Fiction", "English", "Author A", 2000)
    book2 = Book("B002", "Book", "Book 2", "Non-Fiction", "English", "Author B", 2010)
    periodical1 = Periodical("P001", "Periodical", "Periodical 1", "Magazine", "English", "Author C", 2020)
    audiobook1 = Audiobook("A001", "Audiobook", "Audiobook 1", "Fiction", "English", "Author A", 2015, "MP3")

    library_tree.insert(book1)
    library_tree.insert(book2)
    library_tree.insert(periodical1)
    library_tree.insert(audiobook1)

    assert library_tree.search("B001").library_item == book1, "Search by ID failed for B001"
    assert library_tree.search("A001").library_item == audiobook1, "Search by ID failed for A001"

    assert library_tree.search_by_title("Book 1") == book1, "Search by title failed for 'Book 1'"
    assert library_tree.search_by_title("Audiobook 1") == audiobook1, "Search by title failed for 'Audiobook 1'"

def test_delete():
    library_tree = LibraryTree()
    book1 = Book("B001", "Book", "Book 1", "Fiction", "English", "Author A", 2000)
    book2 = Book("B002", "Book", "Book 2", "Non-Fiction", "English", "Author B", 2010)

    library_tree.insert(book1)
    library_tree.insert(book2)

    library_tree.delete(book1)
    assert library_tree.search("B001") is None, "Delete failed for B001"
    
    library_tree.delete(book2)
    assert library_tree.search("B002") is None, "Delete failed for B002"

if __name__ == "__main__":
    test_insert_and_search()
    test_delete()
    print("All tests passed successfully.")

