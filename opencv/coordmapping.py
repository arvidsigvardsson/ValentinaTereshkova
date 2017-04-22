#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import numpy as np
class Mapper:
    def __init__(self, p1, p2, p3, p4, xdim, ydim):
        self.xdim = xdim
        self.ydim = ydim
        self.calibrate(p1, p2, p3, p4)

    def calibrate(self, p1, p2, p3, p4):
        A = np.matrix(p1 + (1,)).T
        B = np.matrix(p2 + (1,)).T
        C = np.matrix(p3 + (1,)).T
        D = np.matrix(p4 + (1,)).T

        # matris som vänder på y-axeln, så att den växer uppåt, istället för ned som vi får ut från opencv, samt sätter punkten p1 till origo
        trans = np.matrix(((1, 0, -A.item(0)), (0, -1, A.item(1)), (0, 0, 1)))

        AB = np.matmul(trans, A + 0.5*(B - A))
        BC = np.matmul(trans, B + 0.5*(C - B))
        CD = np.matmul(trans, C + 0.5*(D - C))
        AD = np.matmul(trans, A + 0.5*(D - A))
#
#        print 'AB'
#        print AB
#        print 'BC'
#        print BC
#        print 'CD'
#        print CD
#        print 'AD'
#        print AD
#
#        print trans

        # trans = np.matrix(([1, 0, -p1[0]], [0, 1, -p1[1]], [0, 0, 1]))

        # baselinevec = np.matrix(([p2[0] - p1[0]], [p2[1] - p1[1]]))
        baselinevec = BC - AD
        
        # print 'trans:'
        # print trans 
        # print 'baseline:'
        # print baselinevec # np.array_str(baselinevec)

        # xbase = np.array(([1], [0]))
        xbase = np.matrix((1, 0, 0))
        # print 'xbase:'
        # print xbase

        #dotp = np.matmul(baselinevec.T, xbase)[0,0] 
        dotp = np.matmul(xbase, baselinevec).item(0)
        alpha = math.acos(dotp /(np.linalg.norm(baselinevec) * np.linalg.norm(xbase)))

        # koll om punkterna ska roteras medsols eller motsols
        if BC.item(1) > AD.item(1):
            theta = - alpha
        else:
            theta = alpha

        rotate = np.matrix(((math.cos(theta), -math.sin(theta), 0), (math.sin(theta), math.cos(theta), 0), (0, 0, 1)))
        xscale = self.xdim / np.linalg.norm(BC - AD)
        yscale = self.ydim / np.linalg.norm(AB - CD)
        scaler = np.matrix(((xscale, 0, 0), (0, yscale, 0), (0, 0, 1)))

        self.mapmtx = np.matmul(scaler, np.matmul(rotate, trans))

    def get_mapped(self, p):
        point = np.matrix(p + (1,)).T
        result = np.matmul(self.mapmtx, point)
        return (result.item(0), result.item(1))

# bilateration med två kända punkter, en i origo och den andra på y-axeln med avstånd dist till origo. r1 är okända punktens avstånd till origo, r2 avstånd till andra punkten. Returnerarpositivt x-värde, även -x är lösning
def bilat(dist, r1, r2):
    y = (r1**2 - r2**2 + dist**2) / (2 * dist)
    x = math.sqrt(r1**2 - y**2)
    return (x, y)


def main():
    # dist = 300
    # print bilat(dist, 66.4, 261.1)
    mp = Mapper((561, 2722), (3426, 2524), (3228, 379), (429, 610), 400, 300)
    E = (2942, 627)
    # mp = Mapper((3,6), (10,2),(7,-3.5),(0,0), 4, 3.4)
    # newpoint = mp.get_mapped((4,4))
    newpoint = mp.get_mapped(E)
    print 'Mappad punkt:', newpoint

if __name__ == '__main__':
    main()


