from visual import *
import Image, time, thread, collisiondetection
from math import *
from objects import *
#from usercode import usercode
from arena import *



'''
#################
Usercode Function
#################
'''    

def usercode():
    while True:
        R.motors[0].speed = 50.0
        R.motors[1].speed = 50.0
        time.sleep(2)
        R.motors[0].speed = 50.0
        R.motors[1].speed = -50.0
        time.sleep(0.5)
        R.motors[0].speed = 50.0
        R.motors[1].speed = 50.0
        time.sleep(2)

   

     
'''
#############################
Movement update and collision
#############################
'''

if __name__ == "__main__":
    
    for x in xrange(41,60):
        token_list.append(Token(x))
        for thing in Token(x).markers:
            marker_list.append(thing)
    populate_walls(5,5)
    
    global R
    #R = Robot(0,15,0)
    thread.start_new_thread(usercode,())
    while True:
        rate(RATE)
        #Calculates turning effect of each motor and uses them to make a turn
        averagespeed = (R.motors[0].speed + R.motors[1].speed)/2
        velocity = norm(R.box.axis)*averagespeed/RATE
        moment0 = R.motors[0].speed
        moment1 = -R.motors[1].speed
        totalmoment = (moment0 + moment1)/RATE
        #Check for collisions with walls
        for wall in walllist:
            if collisiondetection.collisiondetect(wall,R.box):
                if wall == walllist[0]:
                    print "wall 1"
                    R.box.pos += (0.2,0,0)
                elif wall == walllist[1]:
                    print "wall 2"
                    R.box.pos += (-0.2,0,0)
                elif wall == walllist[2]:
                    print "wall 3"
                    R.box.pos += (0,0,0.2)
                elif wall == walllist[3]:
                    print "wall 4"
                    R.box.pos += (0,0,-0.2)
                velocity=(0,0,0)
                totalmoment=0     
        #check for collisions with 
        for token in token_list:
            if collisiondetection.collisiondetect(R.box,token.box):
                print "True"
                #check if markers are touching walls
                for wall in walllist:
                    if collisiondetection.collisiondetect(wall,token.box):
                        if wall == walllist[0]:
                            print "wall 1"
                            token.box.pos += (0.1,0,0)
                            R.box.pos += (0.2,0,0)
                            for things in token.markers:
                                things.marker.pos += (0.1,0,0)
                        elif wall == walllist[1]:
                            print "wall 2"
                            token.box.pos += (-0.1,0,0)
                            R.box.pos += (-0.2,0,0)
                            for things in token.markers:
                                things.marker.pos += (-0.1,0,0)
                        elif wall == walllist[2]:
                            print "wall 3"
                            token.box.pos += (0,0,0.1)
                            R.box.pos += (0,0,0.2)
                            for things in token.markers:
                                things.marker.pos += (0,0,0.1)
                        elif wall == walllist[3]:
                            print "wall 4"
                            token.box.pos += (0,0,-0.1)
                            R.box.pos += (0,0,-0.2)
                            for things in token.markers:
                                things.marker.pos += (0,0,-0.1)
                        velocity=(0,0,0)
                        totalmoment=0  
                if velocity != (0,0,0):
                    token.box.pos += velocity*1.1
                    for things in token.markers:
                        things.marker.pos += velocity*1.1
        R.box.pos += velocity
        R.box.rotate(angle=totalmoment/RATE, axis = (0,1,0), origin = R.box.pos)
        

    


