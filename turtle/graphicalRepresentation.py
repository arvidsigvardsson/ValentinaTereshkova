import turtle as turtle
import time
import math as math
import urllib2
import json
import requests

turtle.screensize(1920,1080)
turtle.setworldcoordinates(0, 0, 500, 400)

#hamtar robotens koordinater fran servern
def getCoordinates():
    content = urllib2.urlopen("http://192.168.20.133:5000/srv/coordinate/getlatest").read()
    j = json.loads(content)
    x1 = int(j['coordinate']['x1'])
    y1 = int(j['coordinate']['y1'])
    x2 = int(j['coordinate']['x2'])
    y2 = int(j['coordinate']['y2'])
    return ((x1, y1), (x2,y2))

#hamtar objektens koordinater fran servern
def getObjects():
    content = urllib2.urlopen("http://192.168.20.133:5000/srv/objectlist").read()
    j = json.loads(content)
    socka_x = int(j['sock'][0]['x'])
    socka_y = int(j['sock'][0]['y'])
    kub_x = int(j['cube'][0]['x'])
    kub_y = int(j['cube'][0]['y'])
    glas_x = int(j['glas'][0]['x'])
    glas_y = int(j['glas'][0]['y'])
    return ((socka_x, socka_y),(kub_x, kub_y),(glas_x, glas_y))

#bestammer robotens center baserat pa dess koordinater
def getCenter(p1, p2):
    diameter_x = abs(p1[0] - p2[0])
    diameter_y = abs(p1[1] - p2[1])

    middle_x = min(p1[0], p2[0]) + diameter_x / 2
    middle_y = min(p1[1], p2[1]) + diameter_y / 2
    #print "position: ", middle_x, ", ", middle_y
    return (middle_x, middle_y)

#flytta skoldpaddan
def turtleMove(p1, p2):
    turtle.goto(getCenter(p1, p2))

def turtleMoveOneCoordinate(p1):
    turtle.goto(p1)

#placera ett objekt pa kartan
def placeobject(obj1, text, color):
    turtle.color(color)
    turtle.penup()
    turtle.goto(obj1[0], obj1[1])
    turtle.pendown()
    turtle.dot(image)
    turtle.penup()
    #turtle.goto(obj1[0], obj1[1] - 100)
    #turtle.pendown()
    #turtle.circle(100)
    #turtle.penup()
    turtle.goto(obj1[0], obj1[1] + 10)
    turtle.pendown()
    turtle.write(text, False, 'left', font=('Arial', 12, 'normal'))
    turtle.penup()
    turtle.home()
    turtle.pendown()

#gor skoldpaddan fin och placerar objekten
def init():
    turtle.speed(0)
    turtle.home()
    turtleMoveOneCoordinate((0, 400))
    turtleMoveOneCoordinate((500, 400))
    turtleMoveOneCoordinate((500, 0))
    turtle.home()
    turtle.shape('circle')
    socka, kub, glas = getObjects()
    placeobject(socka, 'strumpa', 'green')
    placeobject(kub, 'kub', 'red')
    placeobject(glas, 'glas', 'blue')
    turtle.color('magenta', 'magenta')

    #Mange
    #turtle.Screen().addshape("mangus.gif")
    #turtle.shape("mangus.gif")

    #Gion
    turtle.Screen().addshape("gion.gif")
    turtle.shape("gion.gif")
    
    turtle.speed(5)

def erasableWrite(tortoise, name, font, align, reuse=None):
    eraser = turtle.Turtle() if reuse is None else reuse
    eraser.hideturtle()
    eraser.penup()
    eraser.setposition(tortoise.position())
    eraser.pendown()
    eraser.write(name, font=font, align=align)
    eraser.penup()
    return eraser

def restartTurtle(x, y):
    turtle.reset()
    turtle.speed(0)
    init()
    turtle.speed(5)

def printCoordinate(erasable, p1):
    turtle.hideturtle()
    turtle.penup()
    turtleMoveOneCoordinate((600, 400))
    erasable.clear()
    erasable = erasableWrite(turtle, (p1[0], ", ", p1[1]), font=("Arial", 12, "normal"), align="center", reuse=erasable)
    turtle.showturtle()
    turtle.pendown()
    
    return erasable

turtle.onscreenclick(restartTurtle)
init()
while(True):
    p1, p2 = getCoordinates()
    #turtleMove(p1, p2)
    turtleMoveOneCoordinate(p1)
    #erasable = printCoordinate(erasable, p1)
    
    
