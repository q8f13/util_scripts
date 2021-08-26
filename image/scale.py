# -*- coding: utf-8 -*- 
# scale image file
# based on PIL
# params:
#   1:filename(jpg)
#   2:target width
#   3:target height
# output:
#   width_filename.jpg

from PIL import Image
import os,sys

Image.MAX_IMAGE_PIXELS = 9999999999
# basewidth = 300
w = int(sys.argv[2])
h = int(sys.argv[3])
filename = sys.argv[1]
img = Image.open(filename)
img = img.resize((w,h), Image.ANTIALIAS)
img.save('%d_%s.jpg' % (w,filename)) 
