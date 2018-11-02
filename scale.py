from PIL import Image
import os,sys

Image.MAX_IMAGE_PIXELS = 9999999999
# basewidth = 300
w = int(sys.argv[2])
h = int(sys.argv[3])
filename = sys.argv[1]
img = Image.open(filename)
# wpercent = (basewidth/float(img.size[0]))
# hsize = int((float(img.size[1])*float(wpercent)))
img = img.resize((w,h), Image.ANTIALIAS)
img.save('%d_%s.jpg' % (w,filename)) 