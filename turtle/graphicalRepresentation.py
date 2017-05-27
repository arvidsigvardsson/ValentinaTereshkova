import turtle as turtle
import time
import math as math
import urllib2
import json
import requests

turtle.screensize(1920,1080)
turtle.setworldcoordinates(0, 0, 500, 400)

'''
retrieves the robots coordinates from the server
return: p1, p2
p1: a tuple with coordinates for the LED 1 on the robot
p2: a tuple with coordinates for the LED 2 on the robot
'''
def getCoordinates():
    content = urllib2.urlopen("http://192.168.20.133:5000/srv/coordinate/getlatest").read()
    j = json.loads(content)
    x1 = int(j['coordinate']['x1'])
    y1 = int(j['coordinate']['y1'])
    x2 = int(j['coordinate']['x2'])
    y2 = int(j['coordinate']['y2'])
    return ((x1, y1), (x2,y2))

'''
retrieves the coordinates for the objects
return: socka, kub, glas
socka: a tuple with the coordinates for the sock
kub: a tuple with the coordinates for the cube
glas: a tuple with the coordinates for the glass
'''
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

'''
Returns the center of the robot
param: p1, p2
p1: a tuple with the coordinates for LED 1
p2: a tuple with the coordinates for LED 2
return: p
p: a tuple with the coordinates for the center of the robot
'''
def getCenter(p1, p2):
    diameter_x = abs(p1[0] - p2[0])
    diameter_y = abs(p1[1] - p2[1])

    middle_x = min(p1[0], p2[0]) + diameter_x / 2
    middle_y = min(p1[1], p2[1]) + diameter_y / 2
    return (middle_x, middle_y)

'''
Moves the turtle to the center of the given points
param: p1, p2
p1: a tuple with the coordinates for LED 1
p2: a tuple with the coordinated for LED 2
'''
def turtleMove(p1, p2):
    turtle.goto(getCenter(p1, p2))

'''
Moves the turtle
param: p1
p1: a tuple with the coordinates of where to move
'''
def turtleMoveOneCoordinate(p1):
    turtle.goto(p1)

'''
Places an object on the map
param: obj, text, color
obj: a tuple with the coordinates for the object
text: a string with the name of the object
color: a string with the color of which the object shall be represented
'''
def placeobject(obj, text, color):
    turtle.color(color)
    turtle.penup()
    turtle.goto(obj[0], obj[1])
    turtle.pendown()
    turtle.dot(image)
    turtle.penup()
    turtle.goto(obj[0], obj[1] + 10)
    turtle.pendown()
    turtle.write(text, False, 'left', font=('Arial', 12, 'normal'))
    turtle.penup()
    turtle.home()
    turtle.pendown()

'''
Initializes the program by drawing the map, placing the objects, setting the shape and setting the speed
'''
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

'''
Resets the drawing by removing everything and redrawing it
param: x, y
x: Unused
y: Unused
'''
def restartTurtle(x, y):
    turtle.reset()
    turtle.speed(0)
    init()
    turtle.speed(5)

turtle.onscreenclick(restartTurtle) #when the user clicks the screen, reset the program
init()
while(True):
    p1, p2 = getCoordinates()
    #turtleMove(p1, p2)
    turtleMoveOneCoordinate(p1)
    
    
