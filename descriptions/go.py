from PIL import Image
from PIL import ImageChops
import os

charac = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!"#$%&\'()*+,-./:;<=>?@\\^_`{|}~'
def char(img, iteration):
    arr = []
    for row in range(16):
        val = 0
        for col in range(16):
            px = img.getpixel((col + (iteration * 16), row))
            if px[3] > 0:
                val += pow(2, col)
        arr.append(val)
    return arr


def img2dict(sourceFolder):
    dict_ = {}
    for file in os.listdir(sourceFolder):
        if file.endswith(".png"):
            img = Image.open(os.path.join(sourceFolder, file))
            for i in range(len(charac)):
                data = char(img, i)
                dict_[str(ord(charac[i]))] = data
    with open('out.txt', 'w') as f:
        print(dict_, file=f)


img2dict("in")
