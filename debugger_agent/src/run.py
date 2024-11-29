from graph_construction.graph_builder import GraphConstructor
from graph_construction.db_manager import JSONManager

graph_manager = JSONManager()
graph_constructor = GraphConstructor(graph_manager)
graph_constructor.build_graph("src", "python")


from person import Person

person3 = Person("Alice", 30)
