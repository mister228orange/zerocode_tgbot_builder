from xml.etree.ElementTree import ElementTree
from models import Edge, Node, Graph
from typing import Dict, List

def xml2graph(xml_data:str) -> Graph:
    pass

path = "graph.xml"
tree = ElementTree(file=path)
print(tree, dir(tree))
namespace = {'mx': 'http://www.w3.org/1998/Math/MathML'}
root = tree.getroot()
cells = root.findall('.//mxCell', namespace)
vertices = [{
    'id': cell.get('id'),
    'title': cell.get('value'),
}
    for cell in cells if cell.get("vertex") == '1'
]
edges = [
    {
        Edge(
            cell.get('source'),
            cell.get('target'),
            cell.get('value')
        )
    }
    for cell in cells if cell.get("edge") == '1'
]
edges: List[Edge] = []
nodes: List[Node] = []
for cell in cells:
    if cell.get("edge") == '1':
        edges.append(Edge({
                cell['source'],
                cell['target'],
                cell.get('value')
            }
        ))
    else:
        nodes.append(
            Node({
                cell['id'],
                cell.get("value")
            })
        )
g = Graph(nodes, edges)
print(g)
print(vertices)
print(edges)
print(cells, cells[1])
print(dir(cells[1]))