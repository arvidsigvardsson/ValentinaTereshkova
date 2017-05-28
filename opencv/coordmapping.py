#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import numpy as np
import cv2

# from calibration import camera_matrix, dist_coeffs
import calibration

class Mapper:
    def __init__(self, p1, p2, p3, p4, xdim, ydim, camerapos):
        self.xdim = xdim
        self.ydim = ydim
        self.camera_matrix = calibration.camera_matrix
        self.dist_coeffs = calibration.dist_coeffs
        self.calibrate(p1, p2, p3, p4, camerapos)

    def remove_distortion(self, p):
        # gör om p till homografiskt nparray
        pos = np.array([[p[0]], [p[1]], [1]])
        #print 'pos'
        #print pos

        # mappar om koordinaten med camera_matrix, sätter origo i optiska centret
        # pos = np.matmul(self.camera_matrix, pos)
        # print 'nya pos'
        # print pos

        # beräknar radien r
        # r = (pos[0] **2 + pos[1] ** 2) ** .5
        # print 'r:', r

        # test
        optmtx, roi = cv2.getOptimalNewCameraMatrix(self.camera_matrix, self.dist_coeffs, (800, 600), 1)
        #print 'optmtx'
        #print optmtx

        newpos = cv2.undistortPoints(np.array(
             [[[p[0], p[1]]],
              [[p[0], p[1]]]]), self.camera_matrix, self.dist_coeffs, None, optmtx)
        # newpos = cv2.undistortPoints(np.array(
        #      [[[450, 350]],
        #       [[400, 300.0]]]), self.camera_matrix, self.dist_coeffs, None, optmtx)
        #print 'mappar om punkten:'
        #print pos
        #print 'till nya postitionen:'
        #print newpos

        rp = (newpos[0][0][0], newpos[0][0][1])
        #print 'rp'
        #print rp
        return rp

    def calibrate(self, p1, p2, p3, p4, camerapos):
        # tar bort distortion
        p1 = self.remove_distortion(p1)
        p2 = self.remove_distortion(p2)
        p3 = self.remove_distortion(p3)
        p4 = self.remove_distortion(p4)
        # camerapos = self.remove_distortion(camerapos)

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
        # tar bort distortion
        p = self.remove_distortion(p)
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

    def get_mapped_with_height_compensated(self, p, height):
        return compensate_for_measured_error(self.get_mapped_with_height(p, height))

# bilateration med två kända punkter, en i origo och den andra på y-axeln med avstånd dist till origo. r1 är okända punktens avstånd till origo, r2 avstånd till andra punkten. Returnerarpositivt x-värde, även -x är giltig lösning
def bilat(dist, r1, r2):
    y = (r1**2 - r2**2 + dist**2) / (2 * dist)
    x = math.sqrt(r1**2 - y**2)
    return (x, y)


#Nya x,y koordinaterna blir kalibrerade enligt uppmätt fel

def compensate_for_measured_error((x, y)):
    textdata = ""
    x_compensation = 0.0
    y_compensation = 0.0

    with open('kompensation_koefficienter.txt') as f:
        textdata = f.readlines()
    lines = []
    for line in textdata:
        lines.append(line.replace('\n', ''))
    data = []
    for line in lines:
        data.append(line.split(','))
    for curve in data:
        if curve[1] == "linear":
            if curve[0] == "xx":
                x_compensation += float(curve[2]) * x + float(curve[3])
            elif curve[0] == "xy":
                x_compensation += float(curve[2]) * y + float(curve[3])
            elif curve[0] == "yx":
                y_compensation += float(curve[2]) * x + float(curve[3])
            elif curve[0] == "yy":
                y_compensation += float(curve[2]) * y + float(curve[3])
        elif curve[1] == "squared":
            if curve[0] == "xx":
                x_compensation += float(curve[2]) * x**2 + float(curve[3]) * x + float(curve[4])
            elif curve[0] == "xy":
                x_compensation += float(curve[2]) * y**2 + float(curve[3]) * y + float(curve[4])
            elif curve[0] == "yx":
                y_compensation += float(curve[2]) * x**2 + float(curve[3]) * x + float(curve[4])
            elif curve[0] == "yy":
                y_compensation += float(curve[2]) * y**2 + float(curve[3]) * y + float(curve[4])


        # print 'xkomp:', x_compensation
        # print 'ykomp:', y_compensation

    x -= x_compensation
    y -= y_compensation
    return (x, y)

# en viktning av kompensationen som utförs i compensate_for_measured_error
def get_weighted_compensation((x, y)):
    xx_comp = xy_comp = yx_comp = yy_comp = 0
    with open('kompensation_koefficienter.txt') as f:
        textdata = f.readlines()
    lines = []
    for line in textdata:
        lines.append(line.replace('\n', ''))
    data = []
    for line in lines:
        data.append(line.split(','))
    for curve in data:
        if curve[1] == "linear":
            if curve[0] == "xx":
                xx_comp += float(curve[2]) * x + float(curve[3])
            elif curve[0] == "xy":
                xy_comp += float(curve[2]) * y + float(curve[3])
            elif curve[0] == "yx":
                yx_comp += float(curve[2]) * x + float(curve[3])
            elif curve[0] == "yy":
                yy_comp += float(curve[2]) * y + float(curve[3])
        elif curve[1] == "squared":
            if curve[0] == "xx":
                xx_comp += float(curve[2]) * x**2 + float(curve[3]) * x + float(curve[4])
            elif curve[0] == "xy":
                xy_comp += float(curve[2]) * y**2 + float(curve[3]) * y + float(curve[4])
            elif curve[0] == "yx":
                yx_comp += float(curve[2]) * x**2 + float(curve[3]) * x + float(curve[4])
            elif curve[0] == "yy":
                yy_comp += float(curve[2]) * y**2 + float(curve[3]) * y + float(curve[4])


        # print 'xkomp:', x_compensation
        # print 'ykomp:', y_compensation

    if (abs(x) + abs(y)) != 0:
        x_compensation = (xx_comp * x + xy_comp * y) / (abs(x) + abs(y))
        y_compensation = (yx_comp * x + yy_comp * y) / (abs(x) + abs(y))
    else:
        x_compensation = 0
        y_compensation = 0

    x -= x_compensation
    y -= y_compensation
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

    # mp = Mapper((0.0,0), (10, 0), (10, 10), (0, 10), 10, 10, (0,0, 5))
    # print '\nmappad punkt:'
    # print mp.get_mapped_with_height((0,10), 0.5)

    # mp.remove_distortion((1.0,1.0))
    # mp.remove_distortion((10,10))
    # mp.remove_distortion((100,100))
    # mp.remove_distortion((400, 300))


    error_compensation_list = [(-10.0, -10.0), (0, 52),(1, 101),(2, 150),(3, 198),(4, 245),(4, 292),(4, 339), (5, 384)];
    for p in error_compensation_list:
       c_x, c_y = compensate_for_measured_error(p);
       print "previous x: ", p[0], " previous y: ", p[1]
       print "compensated x: ", c_x, " compensated y: ", c_y
    return

    #error_compensation_list = [(0, 52),(1, 101),(2, 150),(3, 198),(4, 245),(4, 292),(4, 339), (5, 384)];
    #for p in error_compensation_list:
    #    c_x, c_y = compensate_for_measured_error(p);
    #    print "compensated x: ", c_x, " compensated y: ", c_y


    mp = Mapper((149.0, 483.0), (656.0, 411.0), (587.0, 24.0), (111.0, 96.0), 500, 400, (1.0, 1.0, 1.0))
    p2 = (257.0, 274.0)
    mapped_p2 = mp.get_mapped(p2)
    print 'p2:', p2, 'mappad p2:', mapped_p2

    p5 = (574.0, 49.0)
    mapped_p5 = mp.get_mapped(p5)
    print 'mappad p5:', mapped_p5

    p6 = (627.0, 396.0)
    mapped_p6 = mp.get_mapped(p6)
    print 'mappad p6:', mapped_p6

    p3 = (132.0, 107)
    mapped_p3 = mp.get_mapped(p3)
    print 'mappad p3:', mapped_p3

    print 'kompenserad p3', mp.get_mapped_with_height_compensated(p3, 0.0)

if __name__ == '__main__':
    main()
