class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages
        self.chapters = []
        self.pages_read = 0

    class Chapter:
        def __init__(self, title, number, length):
            self.title = title
            self.number = number
            self.length = length
            self.pages_read = 0

        def details(self):
            return f"Chapter {self.number}: {self.title} ({self.length} pages)"

        def pages_left():
            return self.length - self.pages_read

        def read_page():
            self.pages_read += 1

    def add_chapter(self, title, number, length):
        chapter = self.Chapter(title, number, length)
        self.chapters.append(chapter)

    def get_writer_info(self):
        class Writer:
            def __init__(self, name, nationality):
                self.name = name
                self.nationality = nationality

            def bio(self):
                return f"{self.name} is a writer from {self.nationality}."

        return Writer(self.author, "Unknown")

    def generate_review(self):
        def format_review():
            return f"'{self.title}' is an engaging read with {len(self.chapters)} chapters."

        return format_review()

    def summary(self):
        print(f"'The book {self.title}' by {self.author}, {self.pages} pages long.")

    def is_long_book(self):
        return self.pages > 400

    def info(self):
        print(f"'{self.title}' is a book.")
