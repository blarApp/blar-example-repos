from book import Book

new_book = Book("bob", "testing", 100)
new_book.summary()


old_book = Book("alice", "testing", 200)
old_book.summary()

book = Book("alice", "testing", 200)
book.summary()
book.call_book()
print(book.is_long_book())
