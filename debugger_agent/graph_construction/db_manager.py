import json
import uuid
from typing import List, Any

class JSONManager:
    def __init__(self, default_path: str = "graph.json"):
        self.default_path = default_path

    def save_graph(self, nodes: List[Any], edges: List[Any], path: str = None):
        if path is None:
            path = self.default_path
        with open(path, "w") as f:
            formatted_nodes = list(map(self.format_node, nodes))
            formatted_edges = list(map(self.format_edge, edges))
            json.dump({"nodes": formatted_nodes, "edges": formatted_edges}, f, indent=4)

    def format_node(self, node):
        formatted_node = {
            "id": node["attributes"]["node_id"],
            "properties": {
                **node["attributes"],
                "label": node["type"]
            }
        }
        return formatted_node

    def format_edge(self, edge):
        formatted_edge = {
            "id": str(uuid.uuid4()),
            "start": edge["sourceId"],
            "end": edge["targetId"],
            "properties": {
                "label": edge["type"]
            }
        }
        return formatted_edge
