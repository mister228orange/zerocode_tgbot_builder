from xml.etree.ElementTree import ElementTree
from models import JobTypeNode
from typing import Dict, List

def xml2graph(xml_data:str) -> Dict[JobTypeNode, List[JobTypeNode]]:
    pass

path = "graph.xml"
tree = ElementTree(file=path)
print(tree, dir(tree))

root = tree.getroot()
print(root)