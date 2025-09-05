from __future__ import annotations
from dataclasses import dataclass, field

from typing import List


@dataclass
class JobTypeNode:
    id: int
    title: str
    childs: List[JobTypeNode] = field(default_factory=list)
    weight: int = 0
