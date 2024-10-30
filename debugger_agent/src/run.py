from graph_construction.graph_builder import GraphConstructor
from graph_construction.db_manager import JSONManager

graph_manager = JSONManager()
graph_constructor = GraphConstructor(graph_manager)
graph_constructor.build_graph("src", "python")

print("finalizing test 30/10")

i = 1
i += 4
print(i)
