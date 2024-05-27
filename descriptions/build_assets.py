from PIL import Image
from PIL.Image import Palette

from draw_text import *
import os
import pandas as pd


def __getRecordPlayerData():
    SHEET_ID = '134iAr6fepLq1cBAhyAyNkX3RCvbDwclhHsMx_tVtgtY'
    SHEET_NAME = 'DATA'
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
    df = pd.read_csv(url)

    data = []
    id_ = 0
    stack = 0
    for i in range(len(df)):
        location = df.at[i, 'Location'].split(':')
        map_ = location[0].strip()
        sub_area = location[1].strip() if len(location) > 1 else ''

        track_file = df.at[i, 'track file']

        slot_id = df.at[i, 'slot id']
        file_suffix_int = 1000000
        if slot_id == slot_id:  # checks if slot_id is not NaN
            id_ = int(slot_id)
            stack = 0
        else:
            stack += 1

        file_suffix_int += (100 * id_) + stack
        file_suffix = str(file_suffix_int)[1::]

        data.append([map_, sub_area, track_file, file_suffix])

    return data


__frame = (320, 240)
__size = (320, 240)


def __export(img, name, dest):
    # force indexed for debug purposes. Remove later.
    converted = img.convert('P', palette=Palette.ADAPTIVE, colors=2)
    converted.putpalette([
        255, 0, 255,  # index 0 is magenta background
        255, 255, 255,  # index 1 is white
    ])

    converted.save(os.path.join(dest, name))


# def __preview(img):
#     img = img.resize((54, 70), Image.BICUBIC)
#     return img
#
# def __arrange(frame0, frame1, frame2):
#     sheet = Image.new("RGBA", __size, (0, 0, 0, 0))
#
#     sheet.paste(frame0, (0, 0))
#     sheet.paste(frame1, (0, __frame[1]))
#     sheet.paste(frame2, (0, __frame[1] * 2))
#     return sheet
#
# def __shear(img, size, left, wscale, rise, slope):
#     return img.transform(size, Image.Transform.AFFINE,
#                          (1 / wscale, 0, (-left + slope) / wscale, slope, 1, -left * slope + rise))
#
# def __composite(cover, shadeIndex):
#     comp = ImageChops.add(cover, __light[shadeIndex])
#     comp = ImageChops.multiply(comp, __dark[shadeIndex])
#
#     cover.close()
#     return comp

def makeDesc(destinationFolder):
    data = __getRecordPlayerData()

    desc_imgsize = (320, 240)
    map_name_anchor = (7, 194)
    sub_area_anchor = (21, 207)
    track_anchor = (45, 221)
    text_color = (255, 255, 255)  # white
    for entry in data:
        desc_image = Image.new('RGBA', desc_imgsize)
        drawTextSize16(desc_image, map_name_anchor, entry[0], text_color)
        drawTextSize12(desc_image, sub_area_anchor, entry[1], text_color)
        drawTextSize14(desc_image, track_anchor, entry[2], text_color)
        
        filename = "record_player_description_" + entry[3] + ".png"
        __export(desc_image, filename, destinationFolder)
        print(filename)


#path = input('Please enter the destination path (can be relative) :')
#makeDesc(path)
makeDesc('out')
#desc_image = Image.new('RGBA', (320, 240))
#drawTextSize12(desc_image, (21, 210), 'test0123456789!"#$%&\'()*+,-./:;<=>?@\\^_`{|.', (255, 255, 255))
#__export(desc_image, "test.png", path)
