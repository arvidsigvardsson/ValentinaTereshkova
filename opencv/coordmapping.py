#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import numpy as np
class Mapper:
    def __init__(self, p1, p2, p3, p4):
        self.calibrate(p1, p2, p3, p4)
        
    def calibrate(self, p1, p2, p3, p4):
        A = np.matrix(p1 + (1,)).T
        B = np.matrix(p2 + (1,)).T
        C = np.matrix(p3 + (1,)).T
        D = np.matrix(p4 + (1,)).T

        
        trans = np.matrix(([1, 0, -p1[0]], [0, 1, -p1[1]], [0, 0, 1]))
        baselinevec = np.matrix(([p2[0] - p1[0]], [p2[1] - p1[1]]))
        print 'trans:'
        print trans 
        print 'baseline:'
        print baselinevec # np.array_str(baselinevec)

        # xbase = np.array(([1], [0]))
        xbase = np.matrix((1, 0))
        print 'xbase:'
        print xbase

        dotp = np.matmul(baselinevec.T, xbase)[0,0] 
        alpha = math.acos(dotp * np.linalg.norm(baselinevec), np.linalg.norm(xbase))

    def get_mapped(self, p):
        pass

# bilateration med två kända punkter, en i origo och den andra på y-axeln med avstånd dist till origo. r1 är okända punktens avstånd till origo, r2 avstånd till andra punkten. Returnerarpositivt x-värde, även -x är lösning
def bilat(dist, r1, r2):
    y = (r1**2 - r2**2 + dist**2) / (2 * dist)
    x = math.sqrt(r1**2 - y**2)
    return (x, y)


def main():
    # dist = 300
    # print bilat(dist, 66.4, 261.1) 
    mp = Mapper((1, 1), (2, 1), (0, 0), (0,0))

if __name__ == '__main__':
    main()


