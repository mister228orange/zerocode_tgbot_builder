from __future__ import annotations
from dataclasses import dataclass, field

from typing import List, Dict, Tuple, Optional, Sequence



# @dataclass
# class JobTypeNode:
#     id: int
#     title: str
#     childs: List[JobTypeNode] = field(default_factory=list)
#     weight: int = 0



from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Node:
    id: int
    value: str
    is_leaf: bool


@dataclass
class Edge:
    source: Node
    target: Node
    value: Optional[str] = None

@dataclass
class Graph:
    nodes: List[Node]
    adj_list: Dict[Node, List[Tuple[Edge, Node]]]

    def __init__(self, vertex_list: List[Node], edge_list: List[Edge]):
        self.nodes = vertex_list
        self.adj_list = {}
        for edge in edge_list:
            self.adj_list[edge.source] = self.adj_list.get(edge.source, []) + [(edge, edge.target)]
