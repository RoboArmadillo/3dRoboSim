from visual import *
import Image, time, thread, collisiondetection
from math import *
from objects import *
from variables import *
from visual.controls import *

start = False

def change(): # Called by controls when button is clicked
    global R
    global start
    start = True

def number_of_markers(obj): # called on slider drag events
    global NUMBER_OF_TOKENS
    NUMBER_OF_TOKENS = int(obj.value/6)


def togglecubecolor(): # called on toggle switch flips
    global SWARM_MODE
    if SWARM_MODE == False:
        SWARM_MODE= True
    else:
        SWARM_MODE = False

def number_of_robots(obj): # called on slider drag events
    global SWARM_NUMBER
    SWARM_NUMBER = int(obj.value)


 
c = controls(width=500, height=500) # Create controls window
# Create a button in the controls window:
b = button( pos=(0,50), width=90, height=60,
              text='Start Simulation', action=lambda: change() )

t1 = toggle(pos=(35,-25), width=10, height=10, text0='False', text1='True', action=lambda: togglecubecolor())
s3 = slider(pos=(50,-60), width=7, length=50, axis=(0,1,0),min=1,max = 11, action=lambda: number_of_robots(s3))
m4 = menu(pos=(50,5,-5), height=7, width=65, text='Swarm Mode Stuff')



s2 = slider(pos=(-60,-60), width=7, length=50, axis=(0,1,0), action=lambda: number_of_markers(s2))
m1 = menu(pos=(-60,-70,0), height=7, width=10, text='0')
m2 = menu(pos=(-60,-5,0), height=7, width=10, text='25')
m3 = menu(pos=(-55,5,0), height=7, width=65, text='Number of Tokens')


start = False


'''
#################
Usercode Function
#################
'''    

def SR_filter(listname,markertype):
    temporary_list=[]
    for l in listname:
        if l.marker_type== markertype:
            temporary_list.append(l)
    listname=temporary_list
    return listname


def distance_orderer(listname):
    listname=sorted(listname, key=lambda Marker:Marker.distance)
    return listname


def swarmcode(number):
    while True:
        robot_list[number].motors[0].speed = -50.0
        robot_list[number].motors[1].speed = 50.0

            






def usercode0():
    while True:
        markers = R.see()
        markers = SR_filter(markers,"TOKEN")
        markers = distance_orderer(markers)

            
        if len(markers)>0:
            angle = markers[0].bearing.y
            if angle >10 and angle <30:
                R.motors[0].speed = -10
                R.motors[1].speed = 10
            elif angle < -10 and angle > -30:
                R.motors[0].speed = 20
                R.motors[1].speed = -20
            elif angle <10 and angle >-10:
                R.motors[0].speed = 100
                R.motors[1].speed = 100
        else:
            R.motors[0].speed = -10
            R.motors[1].speed = 10
            time.sleep(0.2)

def usercode1():
    while True:
        markers = R.see()
        for m in markers:
            if m.marker_type != "token marker":
                markers.remove(m)

            
        if len(markers)>0:
            angle = markers[0].bearing.y
            if angle >10 and angle <30:
                R.motors[0].speed = -10
                R.motors[1].speed = 10
            elif angle < -10 and angle > -30:
                R.motors[0].speed = 20
                R.motors[1].speed = -20
            elif angle <10 and angle >-10:
                R.motors[0].speed = 30
                R.motors[1].speed = 30
        else:
            R.motors[0].speed = -10
            R.motors[1].speed = 10
            time.sleep(0.2)

def usercode2():
    while True:
        markers = R.see()
        for m in markers:
            if m.marker_type != "token marker":
                markers.remove(m)

            
        if len(markers)>0:
            angle = markers[0].bearing.y
            if angle >10 and angle <30:
                R.motors[0].speed = -10
                R.motors[1].speed = 10
            elif angle < -10 and angle > -30:
                R.motors[0].speed = 20
                R.motors[1].speed = -20
            elif angle <10 and angle >-10:
                R.motors[0].speed = 30
                R.motors[1].speed = 30
        else:
            R.motors[0].speed = -10
            R.motors[1].speed = 10
            time.sleep(0.2)

def usercode3():
    while True:
        markers = R.see()
        for m in markers:
            if m.marker_type != "token marker":
                markers.remove(m)

            
        if len(markers)>0:
            angle = markers[0].bearing.y
            if angle >10 and angle <30:
                R.motors[0].speed = -10
                R.motors[1].speed = 10
            elif angle < -10 and angle > -30:
                R.motors[0].speed = 20
                R.motors[1].speed = -20
            elif angle <10 and angle >-10:
                R.motors[0].speed = 30
                R.motors[1].speed = 30
        else:
            R.motors[0].speed = -10
            R.motors[1].speed = 10
            time.sleep(0.2)



   

     
'''
#############################
Movement update and collision
#############################
'''

#if __name__ == "__main__":

while start == False:
        rate(RATE)
        c.interact()
    
if start == True:

    for x in xrange(41,41+NUMBER_OF_TOKENS):
            token_list.append(Token(x))
            for thing in token_list[x-41].markers:
                marker_list.append(thing)


    if SWARM_MODE == False:
        R = Robot(0,15,0)
            #S = Robot(-150,15,-150)
            #T = Robot(150,15,-150)
            #U = Robot(-150,15,150)
        thread.start_new_thread(usercode0,())
        #thread.start_new_thread(control_window,())
            #thread.start_new_thread(usercode1,())
            #thread.start_new_thread(usercode2,())
            #thread.start_new_thread(usercode3,())

        while True:
            rate(RATE)
            R.update()
            c.interact()


    if SWARM_MODE == True:
        for x in xrange(SWARM_NUMBER):
            robot_list.append(Robot(random.randint(-150,150),15,random.randint(-150,150)))

        counter = 0
        while counter < SWARM_NUMBER:
            counter2 = counter
            thread.start_new_thread(swarmcode,(counter,))
            counter +=1

        while True:
            rate(RATE)
            c.interact()
            for r in robot_list:
                r.update()