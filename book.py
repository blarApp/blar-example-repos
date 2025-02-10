class Book:
    def __init__(self, title, author, pages):
        self.title = titl
        self.author = author
        self.pages = pages

    def summary(self):
        print(f"'the book {self.title}' by {self.author}, {self.pages} pages long.")

    def is_long_book(self):
        return self.pages > 400

    def info(self):
        print(f"'{self.title}' is a book.")
