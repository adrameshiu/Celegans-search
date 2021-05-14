# Subgraphs

- We are using multi- directed graphs(multiDiGraphs) in networkx->https://networkx.org/documentation/stable/reference/classes/multidigraph.html

- We are restricted to use this because we have various types of edges(chemical, assymetric gap etc...) that can be present between the same nodes and each path is directed. 

Based on the main graph we construct, we can find various different types of view depending on the kind of filters we want to apply

- Filter subgraph based on nodes list -
  - We pass a list of nodes that needs to be present in the subgraph
- [Filter subgraphs based on edges list](https://networkx.org/documentation/stable/reference/classes/generated/networkx.MultiDiGraph.edge_subgraph.html#networkx.MultiDiGraph.edge_subgraph)
  - We pass a list of edges that are to be present in the subgraph
  - [Use this link to refer to how to get the relevant details of the edges that are needed](https://jfinkels-networkx.readthedocs.io/en/latest/reference/classes/generated/networkx.MultiGraph.edge_subgraph.html)
  - Since there can be multiple edges between the same nodes, networkx indexes them. we need to include all of them in our subgraphs
- Create a sub VIEW based on nodes and edges present
  - just creates a view based on the nodes and edges comparison function passed



## Useful Links

- [MultiDiGraph API reference](https://networkx.org/documentation/stable/reference/classes/multidigraph.html)