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
    print("Splitting cells into nodes and edges...")
    edge_cells = []
    nodes_cells = []
    for cell in cells:
        if cell.get("edge") == '1':
            edge_cells.append(cell)
        else:
            nodes_cells.append(cell)
    print(f"Found {len(nodes_cells)} node cells and {len(edge_cells)} edge cells.")
    return edge_cells, nodes_cells

def xml2graph(xml_tree:ElementTree) -> Graph:
    print("Parsing XML to graph...")
    namespace = {'mx': 'http://www.w3.org/1998/Math/MathML'}
    root = xml_tree.getroot()
    print("Finding all mxCell elements...")
    cells = root.findall('.//mxCell', namespace)
    print(f"Total mxCell elements found: {len(cells)}")
    edge_cells, nodes_cells = split_cells(cells)
    print(f"Building alias map for node IDs...\n  {nodes_cells}")
    alias = {node_cell.get('id', -1): i for i, node_cell in enumerate(nodes_cells)}
    print(f"Alias map: {alias}")
    nodes_amount = len(alias)
    print(f"Total nodes: {nodes_amount}")
    edges = []
    degrees = [[0, 0] for _ in range(nodes_amount)]
    print("Processing edge cells...")
    for cell in edge_cells:
        src = alias[cell.get('source')]
        dst = alias[cell.get('target')]
        degrees[src][0] += 1
        degrees[dst][1] += 1
        edges.append((src, dst, cell.get("value")))
        print(f"Edge: {src} -> {dst}, value: {cell.get('value')}")
    print(f"Degrees: {degrees}")
    root_id = [i for i, degree in enumerate(degrees) if degree[0] and not degree[1]]
    print(f"Root node candidates: {root_id}")
    print("Building Node objects...")
    nodes:List[Node] = [
        Node(
            id=i,
            value=nodes_cells[i].get("value", ""),
            is_leaf=degrees[i][0] == 0
        ) if degrees[i][0] + degrees[i][1]
        else None
        for i in range(nodes_amount)
    ]
    print(f"Nodes: {nodes}")
    print("Building Edge objects...")
    edge_objs:List[Edge] = [
        Edge(
            source=nodes[e[0]],
            target=nodes[e[1]],
                value=e[2] if e[2] else None
        )
        for e in edges
    ]
    print(f"Edges: {edge_objs}")
    print("Graph construction complete.")
    return  Graph(nodes, edge_objs)

path = "graph.xml"
tree = ElementTree(file=path)
print(tree, dir(tree))

g = xml2graph(tree)
