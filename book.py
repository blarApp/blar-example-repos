class Book:
    def __init__(self, title, author, pages):
        self.title = titl
        self.author = author
        self.pages = pages

    def summary(self):
        print(f"'{self.title}' by {self.author}, {self.pages} pages long to modified.")

    def is_long_book(self, title):
        return self.pages > 300

