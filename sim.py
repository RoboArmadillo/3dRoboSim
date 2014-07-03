from visual import *
import Image, time, thread, collisiondetection
from math import *

im = Image.open('libkoki.png')  
im2 = Image.open('floor.png') 

tex = materials.texture(data=im, mapping='sign')
tex2 = materials.texture(data=im2, mapping='sign')

lamp = local_light(pos=(200,300,200), color=color.white)

color.brown = (0.38,0.26,0.078)
color.orange = (0.85,0.54,0.18)

#width and height
#0-400

marker_list = []
player_position = vector(1,2,3)

LENGTH = 400
WIDTH = 400
HEIGHT = 50
RATE = 50

#creates arena
arenafloor = box(pos=(0,0,0), size=(4,WIDTH,LENGTH), color=color.orange, material = tex2, axis=(0,1,0))
arenawall1 = box(pos=(-WIDTH/2,HEIGHT/2,0), size=(4,HEIGHT,LENGTH), color=color.orange)
arenawall2 = box(pos=(WIDTH/2,HEIGHT/2,0), size=(4,HEIGHT,LENGTH), color=color.orange)
arenawall3 = box(pos=(0,HEIGHT/2,-LENGTH/2), size=(WIDTH,HEIGHT,4), color=color.orange)
arenawall4 = box(pos=(0,HEIGHT/2,LENGTH/2), size=(WIDTH,HEIGHT,4), color=color.orange)
walllist = [arenawall1,arenawall2,arenawall3,arenawall4]
scene.forward=(0,-1,0)

#the marker object creates one "Marker" that represents one paper marker that we stick on the side of a "token".
#For the Boxes look at the "Token" Object
class Marker(object):
    def __init__(self,code,x,y,z,axis_decider,marker_type):
        global player_position
        self.x = x
        self.y = y
        self.z = z
        self.pos = vector(self.x,self.y,self.z)

        self.axis = vector(int(axis_decider[0]),int(axis_decider[1]),int(axis_decider[2]))

        self.marker_type = marker_type
        if self.marker_type == "token marker":
            self.size = 9
        elif self.marker_type == "token arena":
            self.size = 40
        self.marker = box(pos=self.pos, size=(0.01,self.size,self.size), color=color.white,material=tex,axis = self.axis)



        self.angle = 0
        self.angle_rad = math.radians(self.angle)
        self.distance = math.sqrt((self.pos.x -player_position.x)**2 + (self.pos.y -player_position.y)**2 + (self.pos.z -player_position.z)**2)
        self.code = code



class Token(object):
    def __init__(self,code):
        global player_position
        self.x = random.randint((-WIDTH/2)+11,WIDTH/2-11)
        self.z = random.randint((-LENGTH/2)+11,LENGTH/2-11)
        self.pos = vector(self.x,7,self.z)
        self.size = 10
        self.box = self.marker = box(pos=self.pos, size=(self.size,self.size,self.size), color=color.brown)

        self.markers = [Marker(code,self.x-5,7,self.z,(-1,0,0),"token marker"),
                        Marker(code,self.x+5,7,self.z,(1,0,0),"token marker"),
                        Marker(code,self.x,7,self.z-5,(0,0,-1),"token marker"),
                        Marker(code,self.x,7,self.z+5,(0,0,1),"token marker"),
                        Marker(code,self.x,2,self.z,(0,-1,0),"token marker"),
                        Marker(code,self.x,12,self.z,(0,1,0),"token marker")]



        self.angle = 0
        self.angle_rad = math.radians(self.angle)
        self.pos = vector(self.x,7,self.z)
        #self.token.rotate(angle = self.angle_rad,axis=(0,1,0),origin = self.pos)
        self.code = code

class Motor(object):
    def __init__(self, which_motor, speed = 0):
        self._speed = speed;
        self._motor_no = which_motor
        
    @property
    def speed(self):
        return self._speed
        
    @speed.setter
    def speed(self, value):
        global speed
        self._speed = value
    
    @speed.deleter
    def speed(self):
        del self._speed

class Robot(object):
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        self.velocity = vector(0,0,0)
        self.pos = vector(self.x,self.y,self.z)
        self.box = box(pos=self.pos, size=(50,30,30), color=color.blue)
        self.motors=[Motor(0),Motor(1),Motor(2)]

    def see(self):
        for m in marker_list:
            a = m.axis
            b = R.box.axis
            if diff_angle(a,b)<pi/2:
                del (m)
        return marker_list
		
def populate_walls(Tokens_per_wallx,Tokens_per_wallz):
    spacingx = WIDTH/(Tokens_per_wallx+1)
    spacingz = LENGTH/(Tokens_per_wallz+1)
    #xwall1
    counter = 0
    xpos = -WIDTH/2
    ypos = HEIGHT/2
    zpos = LENGTH/2+4
    while counter <=Tokens_per_wallx:
        xposnew = xpos + (counter * spacingx)
        if counter > 0:
            box = Marker(2,xposnew,ypos,zpos-6,(0,0,-1),"token arena")
        counter +=1

    while counter <=Tokens_per_wallx+Tokens_per_wallz:
        zposnew = zpos - ((counter-Tokens_per_wallx) * spacingz)
        if counter > Tokens_per_wallx:
            box = Marker(2,xpos+2,ypos,zposnew,(1,0,0),"token arena")
        counter +=1

    while counter <=((Tokens_per_wallx*2)+Tokens_per_wallz):
        xposnew = xpos + ((counter-Tokens_per_wallx-Tokens_per_wallz) * spacingz)
        if counter > Tokens_per_wallx+Tokens_per_wallz:
            box = Marker(2,xposnew+2,ypos,zpos-LENGTH,(0,0,1),"token arena")
        counter +=1

    while counter <=(Tokens_per_wallx+Tokens_per_wallz)*2:
        zposnew = zpos - ((counter-Tokens_per_wallx-Tokens_per_wallz-Tokens_per_wallx) * spacingz)
        if counter > Tokens_per_wallx+Tokens_per_wallz+Tokens_per_wallx:
            box = Marker(2,xpos+WIDTH-2,ypos,zposnew,(-1,0,0),"token arena")
        counter +=1

'''
New version calculates moment caused by each motor
'''
   
    
#function contains usercode as it appears visual must run in main thread 
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
     
#sim code is here
if __name__ == "__main__":
    for x in xrange(41,60):
        marker_list.append(Token(x))
        populate_walls(5,5)
    global R
    R = Robot(0,15,0)
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
        #check for collisions with markers
        for marker in marker_list:
            if collisiondetection.collisiondetect(R.box,marker.box):
                #check if markers are touching walls
                for wall in walllist:
                    if collisiondetection.collisiondetect(wall,marker.box):
                        if wall == walllist[0]:
                            print "wall 1"
                            marker.box.pos += (0.1,0,0)
                            R.box.pos += (0.2,0,0)
                            for things in marker.markers:
                                things.marker.pos += (0.1,0,0)
                        elif wall == walllist[1]:
                            print "wall 2"
                            marker.box.pos += (-0.1,0,0)
                            R.box.pos += (-0.2,0,0)
                            for things in marker.markers:
                                things.marker.pos += (-0.1,0,0)
                        elif wall == walllist[2]:
                            print "wall 3"
                            marker.box.pos += (0,0,0.1)
                            R.box.pos += (0,0,0.2)
                            for things in marker.markers:
                                things.marker.pos += (0,0,0.1)
                        elif wall == walllist[3]:
                            print "wall 4"
                            marker.box.pos += (0,0,-0.1)
                            R.box.pos += (0,0,-0.2)
                            for things in marker.markers:
                                things.marker.pos += (0,0,-0.1)
                        velocity=(0,0,0)
                        totalmoment=0  
                if velocity != (0,0,0):
                    marker.box.pos += velocity*1.1
                    for things in marker.markers:
                        things.marker.pos += velocity*1.1
        R.box.pos += velocity
        R.box.rotate(angle=totalmoment/RATE, axis = (0,1,0), origin = R.box.pos)
        

    


