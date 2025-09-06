from __future__ import annotations
from dataclasses import dataclass, field

from typing import List, Dict, Tuple, Optional, Sequence

from xml2graph import adj_list


# @dataclass
# class JobTypeNode:
#     id: int
#     title: str
#     childs: List[JobTypeNode] = field(default_factory=list)
#     weight: int = 0

@dataclass
class Edge:
    source: Node
    target: Node
    value: Optional[Sequence[str], None]

@dataclass
class Node:
    id: Sequence[str]
    value: Sequence[str]

@dataclass
class Graph:
    nodes: List[Node]
    adj_list: Dict[Node, List[Tuple[Edge, Node]]]

    def __init__(self, vertex_list: List[Node], edge_list: List[Edge]):
        self.nodes = vertex_list
        for edge in edge_list:
            self.adj_list[edge.source] = self.adj_list.get(edge.source, []) + [(edge, edge.target)]
