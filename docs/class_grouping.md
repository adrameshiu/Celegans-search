# Viewing the network

## Objective

- A flag to choose whether to view the connectome graph as a network of  `cells` or a network of `classes`.

## Approach

- Since the intermediate paths still need to the nodes to be investigated and filtered as `cells`, a study of the classes would help derive a lot more conclusions.
- These cells can be grouped to classes again in various ways. 

- Lets give the user the flexibility to view the graph in 3 sensitivities-
  - **Strong/Tight** -> Only show the connection between two nodes if `all the components of the source class`(cells corresponding to the class) are connected to `all components of the target class`(cells corresponding to the target class)
  - **Medium Intensity**-> that `all cells in the from class` have to connect to `at least one cell in the “to” class`
  - **Weak Connections** ->that `any one cell in the from set` can `connect to any one cell in the to set`

## Thoughts

- Should we create a class for the graphs/network  and  have placeholders that hold the networkx sub graph corresponding to each of these flags and switch based on option selected.