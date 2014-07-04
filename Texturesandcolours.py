import Image
from visual import *

'''
##################
Colours and Images
##################
'''
#imports two images we need to use 
im2 = Image.open('floor.png') 
im = Image.open('libkoki.png')
im3 =  Image.open('end.png')
im4 = Image.open('side.png')
im5 = Image.open('top.png')

#converts images to usable textures
tex = materials.texture(data=im, mapping='sign')
tex2 = materials.texture(data=im2, mapping='sign')
tex3 = materials.texture(data=im3, mapping='sign')
tex4 = materials.texture(data=im4, mapping='sign')
tex5 = materials.texture(data=im5, mapping='sign')

#defines any useful colours we need, RGB scale between 0-1, user colour_mapper function to convert from 0-255 to 0-1
color.brown = (0.38,0.26,0.078)
color.orange = (0.85,0.54,0.18)