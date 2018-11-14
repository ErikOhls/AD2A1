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

    init_list = list(G)
    node_list = []

    # Variant: len(init_list)-i
    for i in range(len(init_list)):
        node_list.append(Node())
        node_list[i].node = init_list[i]
        node_list[i].adj = list(G.adj[i])

    index = 0
    found, set = is_cycle_new(node_list, index)
    not_visited, index = all_visited(node_list)
    # Invariat: not_visited, found
    while not_visited and not found:
        found, set = is_cycle_new(node_list, index)
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

    init_list = list(G)
    node_list = []

    # Variant: len(init_list)-i
    for i in range(len(init_list)):
        node_list.append(Node())
        node_list[i].node = init_list[i]
        node_list[i].adj = list(G.adj[i])

    index = 0
    found, set = is_cycle_new(node_list, index)
    not_visited, index = all_visited(node_list)
    # Invariat: not_visited, found
    while not_visited and not found:
        found, set = is_cycle_new(node_list, index)
        not_visited, index = all_visited(node_list)
    return found, set


def is_cycle_new(node_list, index):
    """
    Sig: Node node_list[0..n], int index  ==> boolean, int[0..j-1]
    Pre: node_list is list of nodes, index is within range of list
    Post: True and list of set of cycle first cycle found, or False and empty list
    Example:
        is_cycle(g1) ==> False, []
        is_cycle(g2) ==>  True, [3,7,8,6,3]
    """
    current = node_list[index]
    # Initialize stack intended to track current tree of nodes
    # Type: Node[]
    stack = [current]
    # Iterate over tree
    # Invariant: stack
    while stack:
        print "STACK:"
        print_node_list(stack)
        current.visited = True
        # Iterate over current node's adjecent nodes
        # Variant: len(current.adj)-j
        for j in range(len(current.adj)):
            print "current node:", current.node

            # Set node's parent only if not root node
            if len(stack) > 1:
                node_list[current.node].parent = stack[-2].node

            # If adjacent node is visited, not parent, and in current stack, cycle has been found
            if node_list[current.adj[j]].node != current.parent and \
                node_list[current.adj[j]].visited and \
                is_in_stack(stack, node_list[current.adj[j]]):
                print "True here"
                set = []
                key_node = node_list[current.adj[j]].node
                # Add node number to set until root of cycle is reached
                # Invariant: key_node
                while current.node != key_node:
                    print current.node, key_node
                    set.append(stack.pop().node)
                    current = stack[-1]
                set.append(stack.pop().node)
                set.append(set[0])
                return True, set

            # If adjacent node is same as parent or visited
            if node_list[current.adj[j]].node == current.parent or \
               node_list[current.adj[j]].visited:
                # And node is last in adjacency list, pop node and cuntinue one node down in tree
                if j == len(current.adj)-1:
                    stack.pop()
                    print "JA"
                print "pass"
                continue
            # Otherwise continue up tree
            else:
                print "elsing"
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
    # Variant: len(stack)-i
    for i in range(len(stack)):
        if stack[i] == node:
            return True
    return False

def print_node_list(node_list):
    for i in range(len(node_list)):
        print_node(node_list[i])
        print ""


def print_node(N):
    print "Node:", N.node, "Adjecency:"
    for i in N.adj:
        print i
    print "Visited:", N.visited, "." ,"Parent:", N.parent


def print_node_nr(N):
    print N.node


def all_visited(node_list):
    """
    Sig: list node_list[0..n], Node node ==> Boolean
    Pre: node_list is list of Node
    Post: True and index of unvisited node if unvisited node exists, False and 0 if not
    Example:
        all_visited(node_list1) ==> True, 4
        all_visited(node_list2) ==> False, 0
    """
    # Variant: len(node_list)-i
    for i in range(len(node_list)):
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


    def test_sanity(self):
        """Sanity Test

        This is a simple sanity check for your function;
        passing is not a guarantee of correctness.
        """

        testgraph = nx.Graph([(0,1),(0,2),(0,3),(2,4),(2,5),(3,6),(3,7),(7,8)])
        self.assertFalse(ring(testgraph))
        testgraph.add_edge(6,8)
        self.assertTrue(ring(testgraph))

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

    @classmethod
    def tearDownClass(cls):
        if HAVE_PLT:
            plt.show()
if __name__ == '__main__':
    unittest.main()
