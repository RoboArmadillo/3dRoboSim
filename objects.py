from visual import *
import Image
import random
from variables import *
from Texturesandcolours import *
import collisiondetection
import collections



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
            marker_list.append(box)
        counter +=1

    while counter <=Tokens_per_wallx+Tokens_per_wallz:
        zposnew = zpos - ((counter-Tokens_per_wallx) * spacingz)
        if counter > Tokens_per_wallx:
            box = Marker(2,xpos+2,ypos,zposnew,(1,0,0),"token arena")
            marker_list.append(box)
        counter +=1

    while counter <=((Tokens_per_wallx*2)+Tokens_per_wallz):
        xposnew = xpos + ((counter-Tokens_per_wallx-Tokens_per_wallz) * spacingz)
        if counter > Tokens_per_wallx+Tokens_per_wallz:
            box = Marker(2,xposnew+2,ypos,zpos-LENGTH,(0,0,1),"token arena")
            marker_list.append(box)
        counter +=1

    while counter <=(Tokens_per_wallx+Tokens_per_wallz)*2:
        zposnew = zpos - ((counter-Tokens_per_wallx-Tokens_per_wallz-Tokens_per_wallx) * spacingz)
        if counter > Tokens_per_wallx+Tokens_per_wallz+Tokens_per_wallx:
            box = Marker(2,xpos+WIDTH-2,ypos,zposnew,(-1,0,0),"token arena")
            marker_list.append(box)
        counter +=1





'''
##############
Arena Creation
##############
'''
arenafloor = box(pos=(0,0,0), size=(4,WIDTH,LENGTH), color=color.orange, material = tex2, axis=(0,1,0))
arenawall1 = box(pos=(-WIDTH/2,HEIGHT/2,0), size=(4,HEIGHT,LENGTH), color=color.orange)
arenawall2 = box(pos=(WIDTH/2,HEIGHT/2,0), size=(4,HEIGHT,LENGTH), color=color.orange)
arenawall3 = box(pos=(0,HEIGHT/2,-LENGTH/2), size=(WIDTH,HEIGHT,4), color=color.orange)
arenawall4 = box(pos=(0,HEIGHT/2,LENGTH/2), size=(WIDTH,HEIGHT,4), color=color.orange)
walllist = [arenawall1,arenawall2,arenawall3,arenawall4]

#floor decorations

area1 = box(pos=(0,2,LENGTH/2-50), size=(WIDTH,0.01,4), color=color.white)
area2 = box(pos=(WIDTH/2-50,2,0), size=(4,0.01,LENGTH), color=color.white)
area3 = box(pos=((-WIDTH/2 +50),2,0), size=(4,0.01,LENGTH), color=color.white)
area4 = box(pos=(0,2,(-LENGTH/2 +50)), size=(WIDTH,0.01,4), color=color.white)



scene.forward=(0,-1,0)
lamp = local_light(pos=(200,300,200), color=color.white)






class Marker(object):
    def __init__(self,code,x,y,z,axis_decider,marker_type):
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
        self.code = code






class Token(object):
    def __init__(self,code):
        global player_position
        self.x = -190#random.randint((-WIDTH/2)+60,WIDTH/2-60)
        self.z = 0#random.randint((-LENGTH/2)+60,LENGTH/2-60)
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
        self.code = code




class Robot(object):
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        self.velocity = vector(0,0,0)
        self.pos = vector(self.x,self.y,self.z)
        self.box = box(pos=self.pos, size=(50,30,30), color=color.blue)
        self.motors = [self.Motor(0),self.Motor(1),self.Motor(2)]
        self.servos = [self.Servo(0),self.Servo(1),self.Servo(2)]
        self.Rotationtuple = collections.namedtuple('Rotationtuple', 'x y z')
        self.Markertuple = collections.namedtuple('Markertuple', 'distance code marker_type rotation')
        self.totalmoment=0
        '''
        self.coverings = [self.Covering(self.x-25,17,self.z,(-1,0,0),"front"),
                        self.Covering(self.x+25,17,self.z,(1,0,0),"back"),
                        self.Covering(self.x,30,self.z-15,(0,0,-1),"leftside"),
                        self.Covering(self.x,17,self.z+15,(0,0,1),"rightside"),
                        self.Covering(self.x,2,self.z,(0,-1,0),"top"),
                        self.Covering(self.x,32,self.z,(0,1,0),"top")]
        '''

    def angle_diff(self,v1x,v1z,v2x,v2z):
        angle=atan2(v2z,v2x)-atan2(v1z,v1x)
        return angle
        
    def see(self):
        newlist = []
        personal_marker_list = []
#angle of 2 relative to 1= atan2(v2.y,v2.x) - atan2(v1.y,v1.x)

        for m in marker_list:
            a = m.axis
            b = self.box.axis
            if m.axis.y == 0:
                if (self.angle_diff(a.x,a.z,b.x,b.z)<=1.6) and (self.angle_diff(a.x,a.z,b.x,b.z) >= -1.6):
                    newlist.append(m)





        for n in newlist:
            a = self.box.pos-vector(m.pos.x,self.box.pos.y,m.pos.z)
            b = self.box.axis
            a = math.degrees(self.angle_diff(a.x,a.z,b.x,b.z))
            distance = round(math.hypot((self.box.pos.x-n.marker.pos.x),(self.box.pos.y-n.marker.pos.y))/100,2)
            marker = self.Markertuple(distance,n.code,n.marker_type,self.Rotationtuple(2,a,2))
            personal_marker_list.append(marker)

        return personal_marker_list


    def wall_token_collision(self,token):
            for wall in walllist:
                if collisiondetection.collisiondetect(wall,token.box):
                    if wall == walllist[0]:
                        token.box.pos += (0.1,0,0)
                        self.box.pos += (0.2,0,0)
                        for things in token.markers:
                            things.marker.pos += (0.1,0,0)
                    elif wall == walllist[1]:
                        token.box.pos += (-0.1,0,0)
                        self.box.pos += (-0.2,0,0)
                        for things in token.markers:
                            things.marker.pos += (-0.1,0,0)
                        token.box.pos += (0,0,0.1)
                        self.box.pos += (0,0,0.2)
                        for things in token.markers:
                            things.marker.pos += (0,0,0.1)
                    elif wall == walllist[3]:
                        token.box.pos += (0,0,-0.1)
                        self.box.pos += (0,0,-0.2)
                        for things in token.markers:
                            things.marker.pos += (0,0,-0.1)
                    self.velocity=(0,0,0)
                    self.totalmoment=0  

    def token_token_collision(self,token):
        temp_token_list = token_list[:]
        temp_token_list.remove(token)
        for othertoken in temp_token_list:
            if self.velocity != (0,0,0):
                if collisiondetection.collisiondetect(token.box,othertoken.box):
                    self.wall_token_collision(othertoken)
                    if self.velocity!=(0,0,0):
                        othertoken.box.pos += self.velocity*1.5
                        for things in othertoken.markers:
                            things.marker.pos += self.velocity*1.5
                if self.totalmoment != 0:
                    othertoken.box.rotate(angle=(self.totalmoment/RATE), axis = (0,1,0), origin=self.box.pos)
                    othertoken.box.pos -= 0.03*vector(self.box.axis.z,0,-self.box.axis.x)
                    for things in othertoken.markers:
                        things.marker.rotate(angle=(self.totalmoment/RATE), axis = (0,1,0), origin=self.box.pos)
                        things.marker.pos -= 0.03*vector(self.box.axis.z,0,-self.box.axis.x)
                    self.wall_token_collision(othertoken)
    
    def update(self):
        #Calculates turning effect of each motor and uses them to make a turn
        averagespeed = float((self.motors[0].speed + self.motors[1].speed))/2
        self.velocity = norm(self.box.axis)*averagespeed/RATE
        moment0 = float(self.motors[0].speed)
        moment1 = float(-self.motors[1].speed)
        self.totalmoment = (moment0 + moment1)/RATE
        #Check for collisions with walls
        for wall in walllist:
            if collisiondetection.collisiondetect(wall,self.box):
                if wall == walllist[0]:
                    self.box.pos += (0.2,0,0)
                elif wall == walllist[1]:
                    self.box.pos += (-0.2,0,0)
                elif wall == walllist[2]:  
                    self.box.pos += (0,0,0.2)
                elif wall == walllist[3]:
                    self.box.pos += (0,0,-0.2)
                self.velocity=(0,0,0)
                self.totalmoment=0     
        #check for collisions with tokens
        for token in token_list:
            if collisiondetection.collisiondetect(self.box,token.box):
                #check if tokens are touching walls
                self.wall_token_collision(token) 
                #check if tokens are touching other tokens
                self.token_token_collision(token)
                if self.velocity != (0,0,0):
                    token.box.pos += self.velocity*1.5
                    for things in token.markers:
                        things.marker.pos += self.velocity*1.5
                if self.totalmoment != 0:
                    token.box.rotate(angle=(self.totalmoment/RATE), axis = (0,1,0), origin=self.box.pos)
                    token.box.pos -= 0.03*vector(self.box.axis.z,0,-self.box.axis.x)
                    for things in token.markers:
                        things.marker.rotate(angle=(self.totalmoment/RATE), axis = (0,1,0), origin=self.box.pos)
                        things.marker.pos -= 0.03*vector(self.box.axis.z,0,-self.box.axis.x)
                        things.marker.pos += self.velocity*1.5
                if self.totalmoment != 0:
                    token.box.rotate(angle=(self.totalmoment/RATE), axis = (0,1,0), origin=self.box.pos)
                    token.box.pos -= 0.1*vector(self.box.axis.z,0,-self.box.axis.x)
                    for things in token.markers:
                        things.marker.rotate(angle=(self.totalmoment/RATE), axis = (0,1,0), origin=self.box.pos)
                        things.marker.pos -= 0.1*vector(self.box.axis.z,0,-self.box.axis.x)                        
        self.box.pos += self.velocity
        self.box.rotate(angle=self.totalmoment/RATE, axis = (0,1,0), origin = self.box.pos)

        #this section needs to be fixed to allow the cover to stick to the robot even while turning
        #for m in self.coverings:
            #m.box.rotate(angle=self.totalmoment/RATE, axis = (0,1,0), origin = self.box.pos)
        
        



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

    class Servo(object):
        def __init__(self, which_servo, angle = 90):
            self._angle = angle
            self._servo_no = which_servo
            
        @property
        def angle(self):
            return self._angle
            
        @angle.setter
        def angle(self, value):
            global angle
            self._angle = value
        
        @angle.deleter
        def angle(self):
            del self._angle

    class Covering(object):
        def __init__(self,x,y,z,axis_decider,marker_type):
            self.x = x
            self.y = y
            self.z = z
            self.pos = vector(self.x,self.y,self.z)

            self.axis = vector(int(axis_decider[0]),int(axis_decider[1]),int(axis_decider[2]))

            self.marker_type = marker_type
            if self.marker_type == "back":
                self.sizey = 30
                self.sizez = 30
                self.box = box(pos=self.pos, size=(0.01,self.sizey,self.sizez), color=color.white,material=tex3,axis = self.axis)

            elif self.marker_type == "leftside":
                self.sizey = 30
                self.sizez = 50
                self.box = box(pos=self.pos, size=(0.01,self.sizey,self.sizez), color=color.white,material=tex4,axis = self.axis)

            elif self.marker_type == "top":
                self.sizey = 50
                self.sizez = 30
                self.box = box(pos=self.pos, size=(0.01,self.sizey,self.sizez), color=color.white,material=tex5,axis = self.axis)

            elif self.marker_type == "front":
                self.sizey = 30
                self.sizez = 30
                self.box = box(pos=self.pos, size=(0.01,self.sizey,self.sizez), color=color.white,material=tex6,axis = self.axis)

            elif self.marker_type == "rightside":
                self.sizey = 30
                self.sizez = 50
                self.box = box(pos=self.pos, size=(0.01,self.sizey,self.sizez), color=color.white,material=tex7,axis = self.axis)

