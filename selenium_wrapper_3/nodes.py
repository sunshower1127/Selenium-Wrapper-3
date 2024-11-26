from __future__ import annotations

from .node import Div, Node, _


class Nodes:
    def __init__(self, xpath: str | Node = ""):
        self.xpath = str(xpath)

    def __repr__(self):
        return self.xpath

    def __getitem__(self, index: int):
        new_node = Node()
        if index < 0:
            new_node.xpath = f"({self})[last(){index if index != -1 else ''}]"
        else:
            new_node.xpath = f"({self})[{index+1}]"
        return new_node

    def get_one(self, expr):
        new_node = Node()
        new_node.xpath = f"{self}[{expr}]"
        return new_node

    def get_many(self, expr):
        new_nodes = Nodes()
        new_nodes.xpath = f"{self}[{expr}]"
        return new_nodes


def All(node: Node):
    new_nodes = Nodes(f"{node}")
    return new_nodes


if __name__ == "__main__":
    print(All(_ // Div())[4] / Div())
