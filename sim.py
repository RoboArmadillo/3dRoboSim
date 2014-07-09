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
    for x in xrange(30):
        print "boo"
    start = True


 
c = controls() # Create controls window
# Create a button in the controls window:
b = button( pos=(0,0), width=150, height=60,
              text='Start Simulation', action=lambda: change() )


start = False


'''
#################
Usercode Function
#################
'''    

if SWARM_MODE == False:
    def usercode0():
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

    def usercode1():
        while True:
            markers = S.see()
            print len(markers)
            S.motors[0].speed = -50.0
            S.motors[1].speed = -50.0
            time.sleep(2)
            S.motors[0].speed = 50.0
            S.motors[1].speed = -50.0
            time.sleep(0.5)

    def usercode2():
        while True:
            markers = T.see()
            print len(markers)
            T.motors[0].speed = -50.0
            T.motors[1].speed = -50.0
            time.sleep(2)
            T.motors[0].speed = 50.0
            T.motors[1].speed = -50.0
            time.sleep(0.5)

    def usercode3():
        while True:
            markers = S.see()
            print len(markers)
            U.motors[0].speed = -50.0
            U.motors[1].speed = -50.0
            time.sleep(2)
            U.motors[0].speed = 50.0
            U.motors[1].speed = -50.0
            time.sleep(0.5)


if SWARM_MODE == True:
    def usercode(number):
        while True:
            robot_list[number].motors[0].speed = -50.0
            robot_list[number].motors[1].speed = 50.0
            markers = R.see()
    



   

     
'''
#############################
Movement update and collision
#############################
'''

#if __name__ == "__main__":

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

    while start == False:
        rate(RATE)
        c.interact()


    if start == True:
        while True:
            rate(RATE)
            R.update()
            c.interact()
    '''
            #S.update()
            #T.update()
            #U.update()
    if SWARM_MODE == True:
        for x in xrange(SWARM_NUMBER):
            robot_list.append(Robot(random.randint(-150,150),15,random.randint(-150,150)))

        counter = 0
        while counter < SWARM_NUMBER:
            counter2 = counter
            thread.start_new_thread(usercode,(counter,))
            counter +=1

        while True:
            rate(RATE)
            c.interact()
            for r in robot_list:
                r.update()
    '''
