from visual import *
import Image
import random
from variables import *
from Texturesandcolours import *


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
        self.code = code




class Robot(object):
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        self.velocity = vector(0,0,0)
        self.pos = vector(self.x,self.y,self.z)
        self.box = box(pos=self.pos, size=(50,30,30), color=color.blue)
        self.motors=[self.Motor(0),self.Motor(1),self.Motor(2)]

    def see(self):
        for m in marker_list:
            a = m.axis
            b = R.box.axis
            if diff_angle(a,b)<pi/2:
                del (m)
        return marker_list

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