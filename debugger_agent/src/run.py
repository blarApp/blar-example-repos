from graph_construction.graph_builder import GraphConstructor
from graph_construction.db_manager import JSONManager

graph_manager = JSONManager()
graph_constructor = GraphConstructor(graph_manager)
graph_constructor.build_graph("src", "python")


from person import Person
from book import Book

person3 = Person("Alice", 30)
book = Book("Alice", "title", 30)
book1 = Book("Test", "test", 10)

book.summarize()
book1.summarize()
