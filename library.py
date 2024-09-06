#Superclass to Book, Periodical, Audiobook
class Library:
    def __init__(self, ID, type, title, category, language, author, year_published, audio_format=""):
        self.ID = ID
        self.type = type
        self.title = title
        self.category = category
        self.language = language
        self.author = author
        self.year_published = year_published
        self.audio_format = audio_format

#Attribute audio_format is included but will not be used. Upon item registration, audio_format will not be asked
class Book(Library):
    def __init__(self, ID, type, title, category, language, author, year_published, audio_format="N/A"):
        super().__init__(ID, type, title, category, language, author, year_published, audio_format)
    def __lt__(self, other):
        return self.title < other.title

#Attribute audio_format is included but will not be used. Upon item registration, audio_format will not be asked
class Periodical(Library):
    def __init__(self, ID, type, title, category, language, author, year_published, audio_format="N/A"):
        super().__init__(ID, type, title, category, language, author, year_published, audio_format)
    def __lt__(self, other):
        return self.title < other.title

#The only class with attribute "audio_format"
class Audiobook(Library):
    def __init__(self, ID, type, title, category, language, author, year_published, audio_format=""):
        super().__init__(ID, type, title, category, language, author, year_published)
        self.audio_format = audio_format
    def __lt__(self, other):
        return self.title < other.title
