# -*- coding: utf-8 -*- 
import image_slicer
import os, sys

# print('slice %s pieces' % sys.argv[2])
image_slicer.Image.MAX_IMAGE_PIXELS = 9999999999
tiles = image_slicer.slice(sys.argv[1], int(sys.argv[2]), save=False)
image_slicer.save_tiles(tiles, prefix='slice', format='jpeg', directory='./sliced/')
# image_slicer.save_tiles(tiles, prefix='slice', format='jpeg', directory='./sliced/')
