# script for large image resize

from PIL import Image
import os,sys

Image.MAX_IMAGE_PIXELS = 9999999999
# basewidth = 300
h = int(sys.argv[2])
filename = sys.argv[1]
img = Image.open(filename)
# wpercent = (basewidth/float(img.size[0]))
# hsize = int((float(img.size[1])*float(wpercent)))
img_w,img_h = img.size
ratio = img_w / img_h
# img_new_side = max(h*ratio, h)
img = img.resize((int(h*ratio),h), Image.ANTIALIAS)

def make_square(im, min_size=256, fill_color=(0,0,0)):
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGB', (size, size), 128.0)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    return new_im

new_img = make_square(img, min_size=h, fill_color=(255.0,255.0,255.0))
# img.save('%d_%s.jpg' % (w,filename)) 
new_img.save('%d_%s.jpg' % (h,filename), quality=100, subsampling=0) 
