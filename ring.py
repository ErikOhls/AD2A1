#bin/#!/usr/env python2.7
# -*- coding: utf-8 -*-
'''
Assignment 2: Ring Detection

Team Number:
Student Names:
'''
import unittest
import networkx as nx

"""IMPORTANT:
We're using networkx only to provide a reliable graph
object.  Your solution may NOT rely on the networkx implementation of
any graph algorithms.  You can use the node/edge creation functions to
create test data, and you can access node lists, edge lists, adjacency
lists, etc. DO NOT turn in a solution that uses a networkx
implementation of a graph traversal algorithm, as doing so will result
in a score of 0.
"""

try:
    import matplotlib.pyplot as plt
    HAVE_PLT = True
except ImportError:
    HAVE_PLT = False

class Node:
    """
    Class containing various information about nodes

    Attributes:
       node(int): Identifier
       adj(list): List of adjacent nodes
       visited(boolean): Switch intended to turn on once node is visited
       parent(int): Identifier of parent node
    """
    node = 0
    adj = None
    visited = False
    parent = -1

def ring(G):
    """
    Sig: graph G(node,edge) ==> boolean
    Pre: Graph is undirected graph
    Post: True if graph contains cycle, false if not
    Example:
        ring(g1) ==> False
        ring(g2) ==> True
    """
    if len(G) == 0:
        return False

    # Temporary list used in order to initialize node_list
    # Type: tuple[]
    init_list = list(G)
    # List holding all Nodes that make up the graph
    # Type: Node[]
    node_list = []

    for i in range(len(init_list)):
    # Variant: len(init_list)-i
    # Invariant: len(init_list)
        node_list.append(Node())
        node_list[i].node = init_list[i]
        node_list[i].adj = list(G.adj[i])

    index = 0
    found, set = is_cycle(node_list, index)
    not_visited, index = all_visited(node_list)
    while not_visited and not found:
    # Invariat: not_visited, found
        found, set = is_cycle(node_list, index)
        not_visited, index = all_visited(node_list)
    return found

def ring_extended(G):
    """
    Sig: graph G(node,edge) ==> boolean, int[0..j-1]
    Pre: Graph is undirected graph
    Post: True and list of set of cycle if cycle exists, false and empty list otherwise
    Example:
        ring(g1) ==> False, []
        ring(g2) ==>  True, [3,7,8,6,3]
    """

    if len(G) == 0:
        return False

    # Temporary list used in order to initialize node_list
    # Type: tuple[]
    init_list = list(G)
    # List holding all Nodes that make up the graph
    # Type: Node[]
    node_list = []

    for i in range(len(init_list)):
    # Variant: len(init_list)-i
    # Invariant: len(init_list)
        node_list.append(Node())
        node_list[i].node = init_list[i]
        node_list[i].adj = list(G.adj[i])

    index = 0
    found, set = is_cycle(node_list, index)
    not_visited, index = all_visited(node_list)
    while not_visited and not found:
    # Invariat: not_visited, found
        found, set = is_cycle(node_list, index)
        not_visited, index = all_visited(node_list)
    return found, set


def is_cycle(node_list, index):
    """
    Sig: Node node_list[0..n], int index  ==> boolean, int[0..j-1]
    Pre: node_list is list of nodes, index is within range of list
    Post: True and list of set of cycle first cycle found, or False and empty list
    Example:
        is_cycle(g1) ==> False, []
        is_cycle(g2) ==>  True, [3,7,8,6,3]
    """
    current = node_list[index]
    # Initialize stack intended to track current sub tree of nodes
    # Type: Node[]
    stack = [current]
    # Iterate over tree. As long as stack contain at least 1 node, there are unexplored nodes in the tree
    while stack:
    # Invariant: stack
        current.visited = True
        # If no adjacent node, no ring is possible
        if len(current.adj) == 0:
            return False, []
        # Iterate over current node's adjecent nodes
        for j in range(len(current.adj)):
        # Variant: len(current.adj)-j
        # Invariant: len(current.adj)

            # Set node's parent only if not root node
            if len(stack) > 1:
                node_list[current.node].parent = stack[-2].node

            is_parent = node_list[current.adj[j]].node == current.parent
            is_visited = node_list[current.adj[j]].visited
            is_in_current_stack = is_in_stack(stack, node_list[current.adj[j]])
            # Following conditions means cycle has been found
            if not is_parent and is_visited and is_in_current_stack:
                # Initialize list intended to keep set of nodes making up cycle
                # Type: int[]
                set = []
                key_node = node_list[current.adj[j]].node
                # Add node number to set until root of cycle is reached
                while current.node != key_node:
                # Variant current.node
                # Invariant: key_node
                    set.append(stack.pop().node)
                    current = stack[-1]
                set.append(stack.pop().node)
                set.append(set[0])
                return True, set

            # Ignore parents and visited nodes
            if is_parent or is_visited:
                # If all of adjacency list has been exhausted, track back one node and continue
                if j == len(current.adj)-1:
                    stack.pop()
                    break

            # Continue up the tree
            else:
                current = node_list[current.adj[j]]
                stack.append(current)
                break
        if stack:
            current = stack[-1]
    return False, []


def is_in_stack(stack, node):
    """
    Sig: list stack[0..n], Node node  ==> Boolean
    Pre: Stack is list of nodes, node is class Node
    Post: True if node exists in list, False if node does not
    Example:
        is_in_stack(stack1, node1) ==> True
        is_in_stack(stack1, node1) ==> False
    """
    for i in range(len(stack)):
    # Variant: len(stack)-i
    # Invariant: len(stack)
        if stack[i] == node:
            return True
    return False


def all_visited(node_list):
    """
    Sig: list node_list[0..n], Node node ==> Boolean
    Pre: node_list is list of Node
    Post: True and index of unvisited node if unvisited node exists, False and 0 if not
    Example:
        all_visited(node_list1) ==> True, 4
        all_visited(node_list2) ==> False, 0
    """
    for i in range(len(node_list)):
    # Variant: len(node_list)-i
    # Invariant len(node_list)
        if not node_list[i].visited:
            return True, i
    return False, 0


def draw_graph(G,r):
    """Draw graph and the detected ring
    """
    if not HAVE_PLT:
        return
    pos = nx.spring_layout(G)
    plt.axis('off')
    nx.draw_networkx_nodes(G,pos)
    nx.draw_networkx_edges(G,pos,style='dotted') # graph edges drawn with dotted lines
    nx.draw_networkx_labels(G,pos)

    # add solid edges for the detected ring
    if len(r) > 0:
        T = nx.Graph()
        T.add_path(r)
        for (a,b) in T.edges():
            if G.has_edge(a,b):
                T.edge[a][b]['color']='g' # green edges appear in both ring and graph
            else:
                T.edge[a][b]['color']='r' # red edges are in the ring, but not in the graph
        nx.draw_networkx_edges(
            T,pos,
            edge_color=[edata['color'] for (a,b,edata) in T.edges(data=True)],
            width=4)
    plt.show()

class RingTest(unittest.TestCase):
    """Test Suite for ring detection problem

    Any method named "test_something" will be run when this file is
    executed. Use the sanity check as a template for adding your own test
    cases if you wish.
    (You may delete this class from your submitted solution.)
    """
    def is_ring(self, graph, path):
        """Asserts that the nodes in path from a ring in graph"""
        traversed = nx.Graph()
        for v in range(len(path) - 1):
            self.assertTrue(
                path[v + 1] in graph.neighbors(path[v]),
                "({},{}) is not an edge in the graph\ngraph: {}".format(
                    path[v],
                    path[v+1],
                    graph.edges())
                    )
            self.assertFalse(
                traversed.has_edge(path[v],path[v+1]),
                "duplicated edge: ({},{})".format(path[v],path[v+1]))
            traversed.add_edge(path[v],path[v+1])
        self.assertEqual(
            path[0], path[-1],
            "start and end not equal: {} != {}".format(path[0],path[-1]))


    def est_sanity(self):
        """Sanity Test

        This is a simple sanity check for your function;
        passing is not a guarantee of correctness.
        """

        testgraph = nx.Graph([(0,1),(0,2),(0,3),(2,4),(2,5),(3,6),(3,7),(7,8)])
        self.assertFalse(ring(testgraph))
        testgraph.add_edge(6,8)
        self.assertTrue(ring(testgraph))

    def test_timeout(self):
        G = nx.Graph();
        G.add_node(0);
        G.add_node(1);
        G.add_node(2);
        G.add_node(3);
        G.add_node(4);
        G.add_node(5);
        G.add_node(6);
        G.add_node(7);
        G.add_node(8);
        G.add_edge(0, 1);
        G.add_edge(0, 4);
        G.add_edge(4, 5);
        G.add_edge(1, 2);
        G.add_edge(5, 7);
        G.add_edge(1, 2);
        G.add_edge(6, 8);
        G.add_edge(2, 8);
        G.add_edge(1, 8);
        G.add_edge(0, 6);
        G.add_edge(0, 6);
        G.add_edge(4, 6);
        G.add_edge(1, 2);
        G.add_edge(4, 8);
        G.add_edge(3, 8);
        G.add_edge(3, 8);
        G.add_edge(3, 5);
        G.add_edge(3, 8);
        G.add_edge(2, 4);
        G.add_edge(0, 7);
        G.add_edge(1, 4);
        G.add_edge(2, 8);
        G.add_edge(0, 4);
        G.add_edge(0, 2);
        G.add_edge(1, 3);
        G.add_edge(2, 3);
        G.add_edge(1, 2);
        G.add_edge(4, 6);
        G.add_edge(1, 4);
        testgraph = G
        self.assertTrue(ring(testgraph))

    def test_timeout2(self):
        G = nx.Graph();
        G.add_node(0);
        G.add_node(1);
        G.add_node(2);
        G.add_node(3);
        G.add_node(4);
        G.add_node(5);
        G.add_edge(1, 2);
        G.add_edge(2, 3);
        G.add_edge(2, 4);
        G.add_edge(0, 5);
        G.add_edge(0, 4);
        G.add_edge(1, 2);
        testgraph = G
        self.assertFalse(ring(testgraph))

    def test_timeout2(self):
        G = nx.Graph();
        G.add_node(0);
        G.add_node(1);
        G.add_node(2);
        G.add_node(3);
        G.add_node(4);
        G.add_node(5);
        G.add_node(6);
        testgraph = G
        self.assertFalse(ring(testgraph))

    '''
    def test_simple(self):
        testgraph = nx.Graph()
        self.assertFalse(ring(testgraph))

    def est_noedge(self): #FIX!!!
        testgraph = nx.Graph()
        testgraph.add_node(1)
        testgraph.add_node(2)
        self.assertFalse(ring(testgraph))

    def test_simple(self):
        testgraph = nx.Graph([(0,1), (0,2),(1,2)])
        self.assertTrue(ring(testgraph))

    def test_edge0(self):
        testgraph = nx.Graph([(0,1)])
        self.assertFalse(ring(testgraph))

    def test_multi(self):
        testgraph = nx.Graph([(0,1), (2,3), (2,4), (3,4)])
        self.assertTrue(ring(testgraph))

    def test_mega_multi(self):
        testgraph = nx.Graph([(0,1), (2,3), (3,4), (5,6), (5,7), (6,7)])
        self.assertTrue(ring(testgraph))

    def test_trap_multi(self):
        testgraph = nx.Graph([(0,1), (2,3), (2,4), (3,4), (5,6), (6,7)])
        self.assertTrue(ring(testgraph))

    def test_extended_sanity(self):
        """sanity test for returned ring"""
        testgraph = nx.Graph([(0,1),(0,2),(0,3),(2,4),(2,5),(3,6),(3,7),(7,8),(6,8)])
        found, thering = ring_extended(testgraph)
        self.assertTrue(found)
        self.is_ring(testgraph, thering)
        # Uncomment to visualize the graph and returned ring:
        #draw_graph(testgraph,thering)

    def test_e_multi(self):
        testgraph = nx.Graph([(0,1), (2,3), (2,4), (3,4)])
        found, thering = ring_extended(testgraph)
        self.assertTrue(ring(testgraph))
        self.is_ring(testgraph, thering)

    def test_e_trap_multi(self):
        testgraph = nx.Graph([(0,1), (2,3), (2,4), (3,4), (5,6), (6,7)])
        found, thering = ring_extended(testgraph)
        self.assertTrue(ring(testgraph))
        self.is_ring(testgraph, thering)

    def est_e_edge0(self): # is_ring fails?
        testgraph = nx.Graph([(0,1)])
        found, thering = ring_extended(testgraph)
        self.assertFalse(ring(testgraph))
        self.is_ring(testgraph, thering)
    '''
    @classmethod
    def tearDownClass(cls):
        if HAVE_PLT:
            plt.show()
if __name__ == '__main__':
    unittest.main()
