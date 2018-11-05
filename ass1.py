#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
'''
Assignment 1: Birthday Present

Team Number: 44
Student Names: Erik Ohlsson, Erik Lövgren
'''
import unittest

def birthday_present(P, n, t):
    '''
    Sig: int[0..n-1], int, int --> Boolean
    Pre:
    Post:
    Example: P = [2, 32, 234, 35, 12332, 1, 7, 56]
             birthday_present(P, len(P), 299) = True
             birthday_present(P, len(P), 11) = False
    '''
    # Initialize the dynamic programming matrix, A
    # Type: Boolean[0..n][0..t]
    A = [[None for i in range(t + 1)] for j in range(n + 1)]

    #Sort P ascending
    P.sort()

    # Base case
    if (t == 0):
        print "Solve 0, return true"
        return True
    if (t != 0 and n == 0):
        print "Solve empty set, return false"
        return False

    # Sum = 0 is always true
    for i in range(n + 1):
        A[i][0] = True

    # For each row
    for i in range(n):
        # For each column
        for j in range(t + 1):
            # If current Set value is equal to current Target value
            if P[i] == j:
                A[i][j] = True;
            # If Cell above is true
            elif A[i-1][j] == True:
                A[i][j] = True;
            # Look back only if range is within target range
            elif j-P[i] > 0 and j-P[i] < t:
                # If whatever you have left after subtracting Set value from current target value
                if A[i-1][j-P[i]] == True:
                    A[i][j] = True;
                else:
                    A[i][j] = False
            else:
                A[i][j] = False;

    # Visualize Matrix
    print " "
    for row in A:
        for val in row:
            print '{:4}'.format(val),
        print

    print A[n-1][t]
    return A[n-1][t]

def birthday_present_subset(P, n, t):
    '''
    Sig: int[0..n-1], int, int --> int[0..m]
    Pre:
    Post:
    Example: P = [2, 32, 234, 35, 12332, 1, 7, 56]
             birthday_present_subset(P, len(P), 299) = [56, 7, 234, 2]
             birthday_present_subset(P, len(P), 11) = []
    '''

    A = [[None for i in range(t + 1)] for j in range(n + 1)]

    #Sort P ascending
    P.sort()

    # Base case
    if (t == 0):
        print "Solve 0, return true"
        return True
    if (t != 0 and n == 0):
        print "Solve empty set, return false"
        return False

    # Sum = 0 is always true
    for i in range(n + 1):
        A[i][0] = True

    # For each row
    for i in range(n):
        # For each column
        for j in range(t + 1):
            # If current Set value is equal to current Target value
            if P[i] == j:
                A[i][j] = True;
            # If Cell above is true
            elif A[i-1][j] == True:
                A[i][j] = True;
            # Look back only if range is within target range
            elif j-P[i] > 0 and j-P[i] < t:
                # If whatever you have left after subtracting Set value from current target value
                if A[i-1][j-P[i]] == True:
                    A[i][j] = True;
                else:
                    A[i][j] = False
            else:
                A[i][j] = False;

    # Visualize Matrix
    print " "
    for row in A:
        for val in row:
            print '{:4}'.format(val),
        print

    resultRow = 0
    for i in range(n):
        if A[i][t]:
            resultRow = i
            break

    if A[n-1][t]:
        print [P[resultRow]]
        return [P[resultRow]]
    else:
        return['NEJ']

class BirthdayPresentTest(unittest.TestCase):
    """Test Suite for birthday present problem

    Any method named "test_something" will be run when this file is
    executed. Use the sanity check as a template for adding your own
    tests if you wish.
    (You may delete this class from your submitted solution.)
    """
    '''
    def test_emptySet_sanity(self):
        P = []
        n = len(P)
        t = 10
        self.assertFalse(birthday_present(P, n, t))

    def test_edge0_sanity(self):
        P = [1,2,3,6]
        n = len(P)
        t = 0
        self.assertTrue(birthday_present(P, n, t))

    def test_easy_sanity(self):
        P = [1,2,3,6]
        n = len(P)
        t = 5
        self.assertTrue(birthday_present(P, n, t))

    def test_med_sanity(self):
        P = [2,3,5,8]
        n = len(P)
        t = 10
        self.assertTrue(birthday_present(P, n, t))

    def test_samloyd_sanity(self):
        P = [25,27,3,12,6,15,9,30,21,19]
        n = len(P)
        t = 50
        self.assertTrue(birthday_present(P, n, t))

    def test_bigaf_sanity(self):
        P = [518533,1037066,2074132,1648264,796528,1593056,686112,1372224,244448,977792,1955584,1411168,322336,644672,1289344,78688,157376,314752,629504,1259008]
        n = len(P)
        t = 2463098
        self.assertTrue(birthday_present(P, n, t))

    def test_sat_sanity(self):
        """Sanity Test for birthday_present()

        This is a simple sanity check;
        passing is not a guarantee of correctness.
        """
        P = [2, 32, 234, 35, 12332, 1, 7, 56]
        n = len(P)
        t = 11
        self.assertFalse(birthday_present(P, n, t))
'''
    def test_sol_sanity(self):
        """Sanity Test for birthday_present_subset()

        This is a simple sanity check;
        passing is not a guarantee of correctness.
        """
        P = [2, 32, 234, 35, 12332, 1, 7, 56]
        n = len(P)
        t = 299
        self.assertTrue(birthday_present(P, n, t))
        self.assertItemsEqual(birthday_present_subset(P, n, t),
                              [56, 7, 234, 2])


if __name__ == '__main__':
    unittest.main()
