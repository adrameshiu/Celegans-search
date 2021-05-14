# Minimal Network(Deprecated)

## Objective

- To have a flag that will denote whether the user wants all edges in the subnetwork to be visible, or only the minimal network with the most commonly occurring edges.

## Approach

> Lets look at this from a nodes(vertices) lens. 
>
> Our aim is reduce the network to choose the path with fewer nodes. 
>
> We are doing this because it is very hard to investigate a large complex network with many intermediate nodes and derive any insights from them.

Since we need the source and target nodes no matter what, we are not going to touch them at all.

## Files

- All the algorithms used can be found under `filter_graph.py`

## Current Algorithms

### Minimize Intensity = 1 `(MEDIUM MINIMIZATION)`

- We can do the same thing we did in the new_minimization_algo(intensity=2), but now group them based on classes before performing the minimization
- this way we will have them as paths through classes



### Minimize Intensity = 2  `(LIGHT MINIMIZATION)`

Minimize algorithm where we

​	1) find the count of occurrence's of inter neurons

​	2) sort the interneurons in the order of occurrence's(descending)

 	3) use the path from source to target that passes through a frequently traversed interneuron

​	4) We do this to remove those interneurons that have very few paths when there exists a path through a frequently traversed interneuron

### Minimize Intensity = 3 `(STRONG MINIMIZATION)`

Minimize algorithm where we 

​	1) find the count of occurrence's of inter neurons

​	2) only keep the interneurons that have a lot of paths

​	3) Some source neurons might not get paths

## Future Scope

- One thing we can try is defining the paths as flow and trying to identify the `max flows` by giving `capacity based on the required paths`

-------------------------------------------------------------------------------

# Old Notes



## Algorithm V1

- try to find the most frequent inter neurons that appear in the network
- if there are some interneurons which appear in multiple paths, then we choose that
- we do this by creating a set and using a counter to identify common paths
- if there are some frequent paths that connect all source to vertex, then we try to remove the infrequent ones
- Keep in mind that we do this minimization in terms of classes and not just cells



## Algorithm 2

Lets play around with the intermediate neurons(nodes/vertices).

- We look at all paths between the source and target nodes. 
- Lets approach this from a bottom up approach and take into the consideration the most limiting paths first

### First phase/round

- We sort all paths between the source and target in the order of the number of paths between each pair of source and target(increasing order)
- If there is only one path between two nodes(say, through one intermediate node), we decide to keep the  intermediate node. -> No other option
- If there is a path between a certain source and target node through the intermediate nodes already present, then we choose that path
- We keep doing the same till we reach a state where we have options

### Second phase/ round

- For each path between source and target nodes in the remaining paths, we make a set of intermediate nodes in the path.
- Of all the remaining sets, we find the most commonly occurring subset and the count of their occurrences(most frequently occurring subset).
- We choose the most frequently occurring intermediate paths, use the paths that consist of these intermediate nodes and continue the process till all source->targets have a path 

## Why not directly use the 2nd phase?

> We cant directly use the 2nd phase as it might cause a problem when some paths require certain intermediary nodes which might be given enough importance if we do the 2nd phase first. 

