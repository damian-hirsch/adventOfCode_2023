import networkx as nx


# Get data from .txt file
def get_input() -> nx.Graph:
    with open('input/Day25.txt', 'r') as file:
        # Split lines
        data = file.read().splitlines()
        # Initialize graph
        graph = nx.Graph()
        for line in data:
            connector, cns = line.split(': ')
            for cn in cns.split():
                # Add edges to graph
                graph.add_edge(connector, cn)
    return graph


# Solves part 1
def part_one(graph: nx.Graph) -> int:
    # Minimum edge cut finds the smallest set of edges that you can remove to disconnect the graph, which will be our 3
    # edges. We then remove these edges from the graph.
    graph.remove_edges_from(nx.minimum_edge_cut(graph))

    # Initialize result
    result = 1
    # connected_components returns the set of components belonging to each subgraph (there should be two now, because we
    # disconnected it before)
    for components in nx.connected_components(graph):
        # Count the length and multiply
        result *= len(components)

    return result


def main():

    print('If you multiply the sizes of these two groups together you get:', part_one(get_input()))
    print('The last star you get automatically for gathering all others')


if __name__ == '__main__':
    main()
