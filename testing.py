from book import Book

new_book = Book("bob", "testing", 100)
new_book.summary()
new_book.info()


old_book = Book("alice", "testing", 200)
old_book.summary()

book = Book("alice", "testing", 200)
book.summary()
book.is_long_book()
book = Book("titulo", "alice", 100)
book.summary()
book = Book("The Great Adventure", "John Doe", 500)
book.add_chapter("The Beginning", 1, 30)
book.add_chapter("The Conflict", 2, 45)

writer = book.get_writer_info()
print(writer.bio())  # Prints writer information

print(book.generate_review()) 
