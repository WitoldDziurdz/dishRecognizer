import os
import imghdr
from PIL import Image

def to_jpeg(dir):
    dir = dir + '/'
    files = os.listdir(dir)
    for file in files:
        filename = os.path.splitext(dir + file)[0]
        if imghdr.what(dir + file) == 'jpeg':
            os.rename(dir + file, filename + '.jpg')
        else:
            try:
                im = Image.open(dir + file)
                rgb_im = im.convert('RGB')
                rgb_im.save(filename + '.jpg')
                os.remove(dir + file)
            except:
                pass
