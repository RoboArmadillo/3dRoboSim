from visual import *
import Image, time, thread, collisiondetection
from math import *
from objects import *
#from usercode import usercode






'''
#################
Usercode Function
#################
'''    

def usercode0():
    while True:
        markers = R.see()
        print len(markers)
        R.motors[0].speed = 50.0
        R.motors[1].speed = 50.0
        time.sleep(2)
        R.motors[0].speed = -50.0
        R.motors[1].speed = 50.0
        time.sleep(1)

def usercode1():
    while True:
        markers = S.see()
        print len(markers)
        S.motors[0].speed = -50.0
        S.motors[1].speed = -50.0
        time.sleep(2)
        S.motors[0].speed = 50.0
        S.motors[1].speed = -50.0
        time.sleep(1)

def usercode2():
    while True:
        markers = T.see()
        print len(markers)
        T.motors[0].speed = -50.0
        T.motors[1].speed = -50.0
        time.sleep(2)
        T.motors[0].speed = 50.0
        T.motors[1].speed = -50.0
        time.sleep(1)

def usercode3():
    while True:
        markers = S.see()
        print len(markers)
        U.motors[0].speed = -50.0
        U.motors[1].speed = -50.0
        time.sleep(2)
        U.motors[0].speed = 50.0
        U.motors[1].speed = -50.0
        time.sleep(1)



    



   

     
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
    R = Robot(150,15,150)
    S = Robot(-150,15,-150)
    T = Robot(150,15,-150)
    U = Robot(-150,15,150)
    thread.start_new_thread(usercode0,())
    thread.start_new_thread(usercode1,())
    thread.start_new_thread(usercode2,())
    thread.start_new_thread(usercode3,())
    while True:
        rate(RATE)
        R.update()
        S.update()
        T.update()
        U.update()


