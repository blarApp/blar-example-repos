from book import Book

new_book = Book("bob", "testing", 100)
new_book.summary()
new_book.info()


old_book = Book("alice", "testing", 200)
old_book.summary()

book = Book("alice", "testing", 200)
book.summary()
book.is_long_book()
