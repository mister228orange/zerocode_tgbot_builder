from math import degrees
from xml.etree.ElementTree import ElementTree
from models import Edge, Node, Graph
from typing import List

# edges.append(Edge({
#                 cell['source'],
#                 cell['target'],
#                 cell.get('value')
#             }
#             ))
# nodes.append(
#                 Node({
#                     cell['id'],
#                     cell.get("value")
#                 })
#             )

def split_cells(cells):
    edge_cells = []
    nodes_cells = []
    for cell in cells:
        if cell.get("edge") == '1':
            edge_cells.append(cell)
        else:
            nodes_cells.append(cell)
    return edge_cells, nodes_cells

def xml2graph(xml_tree:ElementTree) -> Graph:
    namespace = {'mx': 'http://www.w3.org/1998/Math/MathML'}
    root = xml_tree.getroot()
    cells = root.findall('.//mxCell', namespace)
    edge_cells, nodes_cells = split_cells(cells)
    alias = {node_cell["id"]: i for i, node_cell in enumerate(nodes_cells)}
    # str -> int
    nodes_amount = len(alias)
    edges = []
    degrees = [[0, 0] for _ in range(nodes_amount)]
    for cell in edge_cells:
        src = alias[cell.get('source')]
        dst = alias[cell.get('target')]
        degrees[src][0] += 1
        degrees[dst][1] += 1
        edges.append((src, dst, cell.get("value")))
    root_id = [i for i, degree in enumerate(degrees) if degree[0] and not degree[1]]
    nodes = [
        Node(
            {
                i,
                nodes_cells[i].get("value", '' ),
                degrees[i][0] == 0
            }
        ) if degrees[i][0] + degrees[i][1]
        else None
        for i in range(nodes_amount)
    ]
    edges = [
        Edge(
            {
                nodes[e[0]],
                nodes[e[1]],
                e[2]
            }
        )
        for e in edges
    ]
    return  Graph(nodes, edges)

path = "graph.xml"
tree = ElementTree(file=path)
print(tree, dir(tree))

g = xml2graph(tree)
