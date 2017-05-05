#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import numpy as np
import cv2

class Mapper:
    def __init__(self, p1, p2, p3, p4, xdim, ydim, camerapos):
        self.xdim = xdim
        self.ydim = ydim
        self.calibrate(p1, p2, p3, p4, camerapos)

    def calibrate(self, p1, p2, p3, p4, camerapos):
        # gör om punkterna från tuples till nparrayer
        a = np.array([[p1[0]], [p1[1]], [1.0]])
        b = np.array([[p2[0]], [p2[1]], [1.0]])
        c = np.array([[p3[0]], [p3[1]], [1.0]])
        d = np.array([[p4[0]], [p4[1]], [1.0]])

        # sparar kamerapositionen, som även har en z-komponent
        self.campos = np.array([[camerapos[0]], [camerapos[1]], [camerapos[2]], [1]])
        # print 'camerapos:'
        # print self.campos

        # matris för att sätta a till origo och vända på yaxeln, som växer positivt nedåt i bildkoordinater. Vi vill ha att den växer positivt uppåt
        flip_y_origo = np.array([[1,  0, -p1[0]],
                                 [0, -1,  p1[1]],
                                 [0,  0,      1]])

        # mappa om hörnen med flip_y_origo
        A = np.matmul(flip_y_origo, a)
        B = np.matmul(flip_y_origo, b)
        C = np.matmul(flip_y_origo, c)
        D = np.matmul(flip_y_origo, d)

        # lista med bildkoordinater
        image_corners = np.array([A[:-1], B[:-1], C[:-1], D[:-1]])

        # lista över de fyra hörnen i världskoordinater
        # world_corners = np.array([
        #     np.array([[0],         [0],         [1.0]]),
        #     np.array([[self.xdim], [0],         [1.0]]),
        #     np.array([[self.xdim], [self.ydim], [1.0]]),
        #     np.array([[0],         [self.ydim], [1.0]]) ])

        world_corners = np.array([
            np.array([[0],         [0.0]]),
            np.array([[self.xdim], [0]]),
            np.array([[self.xdim], [self.ydim] ]),
            np.array([[0],         [self.ydim]]) ])

        # print 'image'
        # print image_corners
        # print 'world'
        # print world_corners

        # räkna ut homographymatrisen
        h, status = cv2.findHomography(image_corners, world_corners)

        # print A[:-1]

        self.mapmtx = np.matmul(h, flip_y_origo)
        # print h

    def get_mapped(self, p):
        point = np.array([[p[0]], [p[1]], [1]])
        result = np.matmul(self.mapmtx, point)
        return (result.item(0), result.item(1))

    def get_mapped_with_height(self, p, height):
        # mappar om p
        pm = self.get_mapped(p)
        # print 'pm:', pm

        # lägger till z-komponent till p och döper om den
        P = np.array([[pm[0]], [pm[1]], [0], [1]])

        # vektor mellan leds position och kamerans postition
        v = P - self.campos

        # på linjen mellan leds position och kamerans postition vill vi hitta x,y-koordinater där z-koordinaten är lika med height, genom att bestämma parametern t i linjens ekvation
        t = (height - self.campos[2][0]) / v[2][0]
        x = self.campos[0][0] + t * v[0][0]
        y = self.campos[1][0] + t * v[1][0]

        # print 't:', t

        return (x, y)

# bilateration med två kända punkter, en i origo och den andra på y-axeln med avstånd dist till origo. r1 är okända punktens avstånd till origo, r2 avstånd till andra punkten. Returnerarpositivt x-värde, även -x är giltig lösning
def bilat(dist, r1, r2):
    y = (r1**2 - r2**2 + dist**2) / (2 * dist)
    x = math.sqrt(r1**2 - y**2)
    return (x, y)


def main():
    # dist = 300
    # print bilat(dist, 66.4, 261.1)
    # mp = Mapper((561, 2722), (3426, 2524), (3228, 379), (429, 610), 400, 300)
    # E = (2942, 627)
    # # mp = Mapper((3,6), (10,2),(7,-3.5),(0,0), 4, 3.4)
    # newpoint = mp.get_mapped((4,4))
    # newpoint = mp.get_mapped(E)
    # print 'Mappad punkt:', newpoint

    # mp = Mapper((335, 3432), (2480, 3239), (2238, 434), (143, 555), 300.0, 400.0, (-1, -1, -1))
    # H = (480, 882)
    # newpoint = mp.get_mapped(H)
    # print 'Mappad punkt:', newpoint

    # F = (1388, 1740)
    # fp = mp.get_mapped(F)
    # print 'F:', fp

    # ppp = mp.get_mapped_with_height(F, 0.5)
    # print 'med höjd:', ppp

    mp = Mapper((0,0), (10, 0), (10, 10), (0, 10), 10, 10, (0,0, 5))
    print '\nmappad punkt:'
    print mp.get_mapped_with_height((0,10), 0.5)

if __name__ == '__main__':
    main()


