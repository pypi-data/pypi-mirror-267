from __future__ import annotations  # for Class forward reference
import random
import uuid

from typing import ClassVar

class Node:
    """
    Should be subclassed only
    """
    # Class Var for statistics
    deepest_level: ClassVar[int] = 0
    largest_sibling_number: ClassVar[int] = 0
    all_nodes: ClassVar[list[Node]] = []

    def __init_subclass__(cls):
        """ each subclass must define its own ClassVar """
        # TODO to be renamed for clarity
        super().__init_subclass__()
        cls.deepest_level: ClassVar[int] = 0
        cls.largest_sibling_number: ClassVar[int] = 0
        cls.all_nodes: ClassVar[list[Node]] = []
        return cls

    def __new__(cls, name: str, parent: Node | None = None) -> None:
        """
        prevent the user to set the same name for 2 nodes
        ??? better to do it with uuid?
        """
        for n in cls.all_nodes:
            if name == n.name:
                raise AttributeError('Node with this name already exists')
        else:
            return super().__new__(cls)

    def __init__(self, name: str, parent: Node | None = None) -> None:
        self.name = name
        self.parent = parent  # is set with add_child
        self.children: list[Node] = []
        self.id = uuid.uuid4()
        type(self).all_nodes.append(self)

    def add_child(self, child: Node) -> None:
        """
        Add new child node to current instance

        :param child: Node object
        """
        child.parent = self
        if child.name not in [c.name for c in self.children]:
            self.children.append(child)
            if child.level > type(self).deepest_level:
                type(self).deepest_level = child.level
            if len(self.children) > type(self).largest_sibling_number:
                type(self).largest_sibling_number = len(self.children)
        else:
            raise Exception('Child with same name already exists')

    @property
    def siblings(self) -> list[Node]:
        """
        Returns all the siblings of the Node object
        """
        if self.has_siblings():
            return self.parent.children

    @property
    def parents(self) -> list[Node]:
        """
        Returns all the ancestors of the Node object
        """
        parents = []
        p = self
        while p.has_parent():
            p = p.parent
            parents.append(p)
        return parents

    @property
    def level(self) -> int:
        """
        Returns the level of the Node object
        """
        level = 0
        p = self
        while p.has_parent():
            level += 1
            p = p.parent
        return level

    @property
    def path(self) -> str:
        """
        Returns a representation of the ancestor lineage of self
        """
        path = ''
        for p in reversed(self.parents):
            path += p.name+'.'
        path += self.name
        return path

    def is_sibling(self, other: str) -> bool:
        """
        Check if Node object is a sibling of the other Node object

        :param other: Other Node object to be compared with
        """
        if other in [s.name for s in self.siblings]:
            return True
        else:
            return False

    def is_child(self, other: str) -> bool:
        """
        Check if Node object is a child of the other Node object
        """
        if other in [s.name for s in self.children]:
            return True
        else:
            return False

    def pretty_print(self, option: str = 'default') -> None:
        """
        Print children tree from current instance
        """
        dashes = '   '*self.level+'|'+'--'*self.level+' '
        if option == 'id':
            dashes += f'[{self.id}] '
        print(f'{dashes}{self.name}')
        for c in self.children:
            c.pretty_print(option)

    def has_parent(self) -> bool:
        """ check if Node object has a parent or not """
        if self.parent is not None:
            return True
        return False

    def has_children(self) -> bool:
        """ check if Node object has one child at least """
        if self.children is not None:
            return True
        return False

    def has_siblings(self) -> bool:
        """ check if Node object has one sibling at least """
        if self.has_parent() and self.parent.has_children() \
           and len(self.parent.children) > 0:
            return True
        return False

    def get_child(self, name: str) -> Node | None:
        """ find and returns a child with specified name. None if nothing found """
        for c in self.children:
            if c.name == name:
                return c
        return None

    def get_sibling(self, name: str) -> Node | None:
        """ find and returns a sibling with specified name. None if nothing
        found """
        for c in self.siblings:
            if c.name == name:
                return c
        return None

    def get_children(self, name: str) -> list[Node]:
        # refactoring, recursion is not good
        results = []
        if self.name == name:
            results.append(self)
        for c in self.children:
            results += c.get_children(name)
        return results

    @staticmethod
    def check_lineage(nodes: list[Node]) -> bool:
        """
        check if the list of nodes is a straight lineage:
            node 1 (ancestor) -> node 2 -> node 3 -> ... -> node n (grand
            children)

        """
        for i in range(1, len(nodes)):
            if nodes[i].parent != nodes[i-1]:
                return False

        return True

    @classmethod
    def reset_stats(cls) -> None:
        """
        reset all the ClassVar members
        """
        cls.deepest_level = 0
        cls.largest_sibling_number = 0
        cls.all_nodes = []

    @classmethod
    def create_random_nodes(cls, type_: str = 'cmd', depth: int = 0) -> Node:
        """
        Creates random tree of nodes for testing purpose
        """
        def create_node(level, i):
            id_ = len(cls.all_nodes) + 1
            return cls(f'{type_}_'+str(id_))
        def create_node_list(level: int, width: int = 5):
            return [create_node(level, i)
                    for i in range(random.randint(1, width))]
        def create_arg_tree(arg: cls):
            if arg.level < depth:
                for a in create_node_list(arg.level):
                    arg.add_child(a)
                    create_arg_tree(a)
            return arg
        arg = cls('parser')
        return create_arg_tree(arg)

    def __lt__(self, other):
        return self.level < other.level

    def __gt__(self, other):
        return self.level > other.level

    def __le__(self, other):
        return self.level <= other.level

    def __ge__(self, other):
        return self.level >= other.level

    def __str__(self) -> str:
        return self.name

if __name__ == "__main__":
    pass
