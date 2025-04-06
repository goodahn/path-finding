from typing import Set

from .graph import Node


class Tree:
    def __init__(self, value: Node):
        self.value: Node = value
        self.parent: "Tree" | None = None
        self.children: Set["Tree"] = set()

    def set_parent(self, parent: "Tree"):
        if self.parent is not None:
            self.parent.remove_child(self)

        self.parent = parent

        self.parent.add_child(self)

    def add_child(self, child: "Tree"):
        self.children.add(child)

    def remove_child(self, child: "Tree"):
        self.children.remove(child)
