from graph_construction.graph_builder import GraphConstructor
from graph_construction.db_manager import JSONManager

graph_manager = JSONManager()
graph_constructor = GraphConstructor(graph_manager)
graph_constructor.build_graph("src", "python")

print("running test 28/10")
for i in range(1, 10):
    print("example")
    print(i)
