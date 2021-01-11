# OPP_ex3 - Directed Weighted Graph

An implementation of directed weighted graph in Python

### Node class

* Node hold node's information
key, position, distance, compenent and boolean prameter -visited.     the last 3 parameter help us in the algorthem part.

* There is a getters and setters for all but the key for him there is just a getter.

### Directed Weighted Graph class

* DiGraph holds three Dictionaries.
**the first** is for the nodes - the key is the key of the node, 
and the value is the node himself.
**the second** is for the edges - the key is a node key,
and the value is a dictionary of all his neighbors.
**the third** represents the edges that enter the nodes.
So the key is the key of the node the value is another dictionary so the key is the key 
of the node from which the edge came out and the value is the weight.

* `add_node()` add a given node to the graph
* `add_edge` make a new edge between two nodes with a given weight.
* `all_in_edges_of_node()` return a dictionary of all the nodes connected to (into) the given node.
* `all_out_edges_of_node()` return a dictionary of all the nodes connected from the given node.

* `remove_edge()` simply delete the edge between two givens nodes.

* `remove_node()` delete the node from the graph and delete all the edges that connected to him.

* `get_all_v()` the method simply return a collection of all the nodes in the graph.
*`getE(key)` return a collection of all the neighbors of a specific node.


* `v_size()` return the number of nodes in the graph

* `e_size()` return the number of the edges in the graph

### Directed Weighted Graph Algorithm class

* GraphAlgo holds a graph, all the algorithms works on the graph.

* the method `init()` change the class's graph to a given graph.
`getGraph()` return the class's graph.

* the method `shortestPathDist()` return the shortest path distance between two givens nodes.
 and return also a list of the shortest path between two givens nodes. 
 The method returns both results in the form of a tuple.
 
 * the method `connected_components()` finds all the Strongly Connected Component(SCC) in the graph. and return list with all SCC.

 
* the method `save_to_json()` simply save the class's graph to given file in json format.
 the method `load_from_json()` simply load a graph to the class's graph from a given json file.
  
