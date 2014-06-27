from visual import *
import math
import Image
import thread

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
RATE = 100

#creates arena
arenafloor = box(pos=(0,0,0), size=(4,WIDTH,LENGTH), color=color.orange, material = tex2, axis=(0,1,0))
areawall1 = box(pos=(-WIDTH/2,HEIGHT/2,0), size=(4,HEIGHT,LENGTH), color=color.orange)
areawall2 = box(pos=(WIDTH/2,HEIGHT/2,0), size=(4,HEIGHT,LENGTH), color=color.orange)
areawall3 = box(pos=(0,HEIGHT/2,-LENGTH/2), size=(WIDTH,HEIGHT,4), color=color.orange)
areawall4 = box(pos=(0,HEIGHT/2,LENGTH/2), size=(WIDTH,HEIGHT,4), color=color.orange)


def backward_map(x,in1,in2,out1,out2):
    a=(in2-in1) #difference between inputs
    b =(out2-out1) #difference between output
    scale_factor = float(b)/float(a)
    return out2 -x*scale_factor


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
        self.velocity = vector(0,5,0)
        self.pos = vector(self.x,self.y,self.z)
        self.box = box(pos=self.pos, size=(50,30,30), color=color.blue)
        self.motors=[Motor(0),Motor(1),Motor(2)]
        self.heading = vector(0,0,1)


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
            box = Marker(counter,xposnew,ypos,zpos-6,(0,0,-1),"token arena")
            marker_list.append(box)
        counter +=1

    while counter <=Tokens_per_wallx+Tokens_per_wallz:
        zposnew = zpos - ((counter-Tokens_per_wallx) * spacingz)
        if counter > Tokens_per_wallx:
            box = Marker(counter,xpos+2,ypos,zposnew,(1,0,0),"token arena")
            marker_list.append(box)
        counter +=1

    while counter <=((Tokens_per_wallx*2)+Tokens_per_wallz):
        xposnew = xpos + ((counter-Tokens_per_wallx-Tokens_per_wallz) * spacingz)
        if counter > Tokens_per_wallx+Tokens_per_wallz:
            box = Marker(counter,xposnew+2,ypos,zpos-LENGTH,(0,0,1),"token arena")
            marker_list.append(box)
        counter +=1

    while counter <=(Tokens_per_wallx+Tokens_per_wallz)*2:
        zposnew = zpos - ((counter-Tokens_per_wallx-Tokens_per_wallz-Tokens_per_wallx) * spacingz)
        if counter > Tokens_per_wallx+Tokens_per_wallz+Tokens_per_wallx:
            box = Marker(counter,xpos+WIDTH-2,ypos,zposnew,(-1,0,0),"token arena")
            marker_list.append(box)
        counter +=1

    

time.sleep(1)
populate_walls(5,5)
R = Robot(0,17,0)

#for x in xrange(41,50):
 #   marker_list.append(Token(x))

def velocity_checker():
    
    oldspeed1 = 1.0
    oldspeed2 = 1.0
    while True:
        #Goes a bit wonky without the prints, not sure why
        print "looping"
        rate(RATE)
        #Calculates turning effect of each motor and uses them to make a turn
        averagespeed = (R.motors[0].speed + R.motors[1].speed)/2
        velocity = norm(R.box.axis)*averagespeed/RATE
        moment0 = float(R.motors[0].speed)
        moment1 = float(-R.motors[1].speed)
        totalmoment = (moment0 + moment1)/RATE
        #Check for collisions with walls
        newpos = R.box.pos+velocity
        if newpos.x > (-WIDTH/2) + 30 and newpos.x < WIDTH/2 -30 and newpos.z  < LENGTH/2 -30 and newpos.z > -LENGTH/2+30:
            R.box.pos += velocity
            R.box.rotate(angle=totalmoment/RATE, axis = (0,1,0), origin = R.box.pos)
            




thread.start_new_thread(velocity_checker,())

counter =0
left = R.motors[0]
right = R.motors[1]
while True:
    rate(24)

    left.speed = 100
    right.speed = 70

    

