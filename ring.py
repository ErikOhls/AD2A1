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
    Pre:
    Post:
    Example:
        ring(g1) ==> False
        ring(g2) ==> True
    """

    init_list = list(G)
    node_list = []

    for i in range(len(init_list)):
        node_list.append(Node())
        node_list[i].node = init_list[i]
        node_list[i].adj = list(G.adj[i])

    found_switch = False

    is_class_cycle(node_list, node_list[0].node, -1, found_switch)

    for i in range(len(node_list)):
        print_node(node_list[i])
        print ""

    '''
    node_list = list(G)

    super_list = []
    for i in range(len(node_list)):
        tmp_list = list(G.adj[i])
        #                 [Node        , adj list, visited, parent]
        super_list.append([node_list[i], tmp_list, False, -1])

    print "\n\n"

    #draw_graph(G, len(G))

    found = False

    if is_cycle(super_list, super_list[0][0], -1, found):
        print "Found cycle"

    print super_list

    return is_cycle(super_list, super_list[0][0], -1, found)
    '''

def print_node(N):
    print "Node:", N.node, "Adjecency:"
    for i in N.adj:
        print i
    print "Visited:", N.visited,"Parent:", N.parent

def ring_extended(G):
    """
    Sig: graph G(node,edge) ==> boolean, int[0..j-1]
    Pre:
    Post:
    Example:
        ring(g1) ==> False, []
        ring(g2) ==>  True, [3,7,8,6,3]
    """

def is_class_cycle(node_list, node, parent, found_switch):
    if node_list[node].visited:
        print "Return from visited node:", node
        return
    node_list[node].visited = True
    node_list[node].parent = parent
    # Only continue if node is within range
    if node < len(node_list):
        # Iterate over adjecency list
        for i in range(len(node_list[node].adj)):
            # If neighbor is visited and node.adj != parent
            if node_list[node_list[node].adj[i]].visited and node_list[node_list[node].adj[i]].node != parent:
                print "Ring found at:", node, node_list[node_list[node].adj[i]].node
                found_switch = True
                return found_switch
            print "Recurring from node:", node_list[node].adj[i]
            is_class_cycle(node_list, node_list[node].adj[i], node, found_switch)
    print "Bottom return from node:", node
    return found_switch

def is_cycle(super_list, node, parent, found):
    if super_list[node][2]:
        print "Return from node:", node, "case visited"
        return
    # Set visited True
    super_list[node][2] = True
    super_list[node][3] = parent
    if node+1 < len(super_list):
        # Iterate over adjecency list
        for i in range(len(super_list[node][1])):
            # if neighbor is visited and not parent
            if super_list[super_list[node][1][i]][2] and super_list[super_list[node][1][i]][0] != parent:
                print node, super_list[super_list[node][1][i]][0]
                print "found ring"
                found = True
                return True
            is_cycle(super_list, super_list[node][1][i], super_list[node][0], found)
    print "Return from node:", node
    return found


def draw_graph(G,r):
    """Draw graph and the detected ring
    """
    if not HAVE_PLT:
        print "dont have plt"
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
        """
        testgraph = nx.Graph([(0,1),(0,2),(0,3),(2,4),(2,5),(3,6),(3,7),(7,8)])
        self.assertFalse(ring(testgraph))
        testgraph.add_edge(6,8)
        self.assertTrue(ring(testgraph))
        """
        testgraph = nx.Graph([(0,1), (0,2),(1,2)])
        self.assertTrue(ring(testgraph))
        '''
   def test_extended_sanity(self):
        """sanity test for returned ring"""
        testgraph = nx.Graph([(0,1),(0,2),(0,3),(2,4),(2,5),(3,6),(3,7),(7,8),(6,8)])
        found, thering = ring_extended(testgraph)
        self.assertTrue(found)
        self.is_ring(testgraph, thering)
        # Uncomment to visualize the graph and returned ring:
        #draw_graph(testgraph,thering)
        '''
    @classmethod
    def tearDownClass(cls):
        if HAVE_PLT:
            plt.show()
if __name__ == '__main__':
    unittest.main()
