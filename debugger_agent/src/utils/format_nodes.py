from llama_index.core.schema import BaseNode
import os
import uuid


def format_function_node(
    node: BaseNode, scope: dict, function_calls: list[str]
) -> dict:
    name = scope["name"]
    signature = scope["signature"]

    processed_node = {
        "type": "FUNCTION",
        "attributes": {
            "name": name,
            "signature": signature,
            "text": node.text,
            "node_id": node.node_id,
            "function_calls": function_calls,
        },
    }

    return processed_node


def format_class_node(node: BaseNode, scope: dict) -> dict:
    name = scope["name"]
    signature = scope["signature"]

    processed_node = {
        "type": "CLASS",
        "attributes": {
            "name": name,
            "signature": signature,
            "text": node.text,
            "node_id": node.node_id,
        },
    }

    return processed_node


def format_file_node(node: BaseNode) -> dict:
    processed_node = {
        "type": "FILE_ROOT",
        "attributes": {
            "text": node.text,
            "node_id": node.node_id,
        },
    }

    return processed_node


def format_directory_node(path: str, package: bool) -> dict:
    processed_node = {
        "attributes": {
            "path": path + "/",
            "name": os.path.basename(path),
            "node_id": str(uuid.uuid4),
        },
        "type": "PACKAGE" if package else "FOLDER",
    }

    return processed_node