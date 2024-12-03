from function import function_one
from person import Person
from book import Book

person = Person(name="Bob", age=20)
book = Book(title="bok", author=person, pages=100)
function_one(person)
