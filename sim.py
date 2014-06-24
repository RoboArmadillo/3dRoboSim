from visual import *
import math
import Image


im = Image.open('libkoki.png')  
im2 = Image.open('floor.png') 

tex = materials.texture(data=im, mapping='sign')

lamp = local_light(pos=(200,1000,200), color=color.white)

color.brown = (0.38,0.26,0.078)












#width and height
#0-400

marker_list = []
player_position = vector(1,2,3)

LENGTH = 400
WIDTH = 400
HEIGHT = 50

#creates arena
arenafloor = box(pos=(0,0,0), size=(WIDTH,4,LENGTH), color=color.green), #material = tex2)
areawall1 = box(pos=(-WIDTH/2,HEIGHT/2,0), size=(4,HEIGHT,LENGTH), color=color.green)
areawall2 = box(pos=(WIDTH/2,HEIGHT/2,0), size=(4,HEIGHT,LENGTH), color=color.green)
areawall3 = box(pos=(0,HEIGHT/2,-LENGTH/2), size=(WIDTH,HEIGHT,4), color=color.green)
areawall4 = box(pos=(0,HEIGHT/2,LENGTH/2), size=(WIDTH,HEIGHT,4), color=color.green)




#the marker object creates one "Marker" that represents one paper marker that we stick on the side of a "token".
#For the Boxes look at the "Token" Object
class Marker(object):
	def __init__(self,code,x,y,z,orientation,marker_type):
		global player_position
		self.x = x
		self.y = y
		self.z = z
		self.pos = vector(self.x,self.y,self.z)
		self.orientation = orientation

		self.marker_type = marker_type
		if self.marker_type == "token marker":
			self.size = 9
		elif self.marker_type == "token arena":
			self.size = 40

		
		if self.orientation == "end":
			self.marker = box(pos=self.pos, size=(self.size,0.01,self.size), color=color.white,material=tex)

		elif self.orientation == "side":
			self.marker = box(pos=self.pos, size=(self.size,self.size,0.01), color=color.white,material = tex)

		elif self.orientation == "other_side":
			self.marker = box(pos=self.pos, size=(0.01,self.size,self.size), color=color.white, material = tex)


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


		self.markers = [Marker(code,self.x-5,7,self.z,"other_side","token marker"),
						Marker(code,self.x+5,7,self.z,"other_side","token marker"),
						Marker(code,self.x,7,self.z-5,"side","token marker"),
						Marker(code,self.x,7,self.z+5,"side","token marker"),
						Marker(code,self.x,2,self.z,"end","token marker"),
						Marker(code,self.x,12,self.z,"end","token marker")]



		self.angle = 0
		self.angle_rad = math.radians(self.angle)
		self.pos = vector(self.x,7,self.z)
		#self.token.rotate(angle = self.angle_rad,axis=(0,1,0),origin = self.pos)
		self.code = code



class Robot(object):
	def __init__(self,x,y,z):
		self.x = x
		self.y = y
		self.z = z
		#self.velocity = vector(0,0,0)
		self.pos = vector(self.x,self.y,self.z)
		robot = box(pos=self.pos, size=(5,5,5), color=color.blue)


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
			box = Marker(2,xposnew,ypos,zpos-6,"side","token arena")
		counter +=1

	while counter <=Tokens_per_wallx+Tokens_per_wallz:
		zposnew = zpos - ((counter-Tokens_per_wallx) * spacingz)
		if counter > Tokens_per_wallx:
			box = Marker(2,xpos+4,ypos,zposnew,"other_side","token arena")
		counter +=1

	while counter <=Tokens_per_wallx+Tokens_per_wallz:
		zposnew = zpos - ((counter-Tokens_per_wallx) * spacingz)
		if counter > Tokens_per_wallx:
			box = Marker(2,xpos+4,ypos,zposnew,"other_side","token arena")
		counter +=1

	





	







for x in xrange(41,50):
	marker_list.append(Token(x))

populate_walls(5,5)



#for m in marker_list:
#	print m.distance

#player = Robot(12)
