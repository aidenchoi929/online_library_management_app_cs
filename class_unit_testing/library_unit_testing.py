#unit testing for library.py
from library import *

def run_tests():
    library_item = Library(1, 'General', 'Sample Title', 'Fiction', 'English', 'John Doe', 2020)
    assert library_item.ID == 1, f"Expected 1, got {library_item.ID}"
    assert library_item.type == 'General', f"Expected 'General', got {library_item.type}"
    assert library_item.title == 'Sample Title', f"Expected 'Sample Title', got {library_item.title}"
    assert library_item.category == 'Fiction', f"Expected 'Fiction', got {library_item.category}"
    assert library_item.language == 'English', f"Expected 'English', got {library_item.language}"
    assert library_item.author == 'John Doe', f"Expected 'John Doe', got {library_item.author}"
    assert library_item.year_published == 2020, f"Expected 2020, got {library_item.year_published}"
    assert library_item.audio_format == '', f"Expected '', got {library_item.audio_format}"
    print("Library tests passed")

    book = Book(2, 'Book', 'Sample Book', 'Non-Fiction', 'Spanish', 'Jane Doe', 2019)
    assert book.ID == 2, f"Expected 2, got {book.ID}"
    assert book.type == 'Book', f"Expected 'Book', got {book.type}"
    assert book.title == 'Sample Book', f"Expected 'Sample Book', got {book.title}"
    assert book.category == 'Non-Fiction', f"Expected 'Non-Fiction', got {book.category}"
    assert book.language == 'Spanish', f"Expected 'Spanish', got {book.language}"
    assert book.author == 'Jane Doe', f"Expected 'Jane Doe', got {book.author}"
    assert book.year_published == 2019, f"Expected 2019, got {book.year_published}"
    assert book.audio_format == 'N/A', f"Expected 'N/A', got {book.audio_format}"
    print("Book tests passed")

    periodical = Periodical(3, 'Periodical', 'Sample Periodical', 'Science', 'French', 'Jean Dupont', 2018)
    assert periodical.ID == 3, f"Expected 3, got {periodical.ID}"
    assert periodical.type == 'Periodical', f"Expected 'Periodical', got {periodical.type}"
    assert periodical.title == 'Sample Periodical', f"Expected 'Sample Periodical', got {periodical.title}"
    assert periodical.category == 'Science', f"Expected 'Science', got {periodical.category}"
    assert periodical.language == 'French', f"Expected 'French', got {periodical.language}"
    assert periodical.author == 'Jean Dupont', f"Expected 'Jean Dupont', got {periodical.author}"
    assert periodical.year_published == 2018, f"Expected 2018, got {periodical.year_published}"
    assert periodical.audio_format == 'N/A', f"Expected 'N/A', got {periodical.audio_format}"
    print("Periodical tests passed")

    audiobook = Audiobook(4, 'Audiobook', 'Sample Audiobook', 'Drama', 'German', 'Hans Müller', 2021, 'MP3')
    assert audiobook.ID == 4, f"Expected 4, got {audiobook.ID}"
    assert audiobook.type == 'Audiobook', f"Expected 'Audiobook', got {audiobook.type}"
    assert audiobook.title == 'Sample Audiobook', f"Expected 'Sample Audiobook', got {audiobook.title}"
    assert audiobook.category == 'Drama', f"Expected 'Drama', got {audiobook.category}"
    assert audiobook.language == 'German', f"Expected 'German', got {audiobook.language}"
    assert audiobook.author == 'Hans Müller', f"Expected 'Hans Müller', got {audiobook.author}"
    assert audiobook.year_published == 2021, f"Expected 2021, got {audiobook.year_published}"
    assert audiobook.audio_format == 'MP3', f"Expected 'MP3', got {audiobook.audio_format}"
    print("Audiobook tests passed")

if __name__ == '__main__':
    run_tests()
