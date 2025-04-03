from book import Book

book = Book("titulo", "alice", 100)
book.summary()
book = Book("The Great Adventure", "John Doe", 500)
book.add_chapter("The Beginning", 1, 30)
book.add_chapter("The Conflict", 2, 45)

writer = book.get_writer_info()
print(writer.bio())  # Prints writer information

print(book.generate_review()) 
