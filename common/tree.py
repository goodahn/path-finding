from typing import Set

from .graph import Node


class Tree:
    def __init__(self, value: Node):
        self.value: Node = value
        self.parent: "Tree" | None = None
        self.children: Set["Tree"] = set()

    def get_parent(self) -> "Tree":
        return self.parent

    def set_parent(self, parent: "Tree"):
        if self.parent is not None:
            self.parent._remove_child(self)

        self.parent = parent

        if self.parent is not None:
            self.parent._add_child(self)

    def get_children(self) -> Set["Tree"]:
        return self.children
    
    def _add_child(self, child: "Tree"):
        self.children.add(child)

    def _remove_child(self, child: "Tree"):
        self.children.remove(child)
