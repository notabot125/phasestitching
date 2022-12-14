import numpy as np
from PIL import Image
import os
from os import listdir
from os.path import isfile, join
import glob
import re
import cv2

if __name__ == '__main__':
    dir_name = 'E:/phase images/'
    save_loc = "E:/stitched images"
    save_name = "testFullRes"
    dimension = [4, 4]
    for picture_index in range(16):
        if picture_index < dimension[0]:  # if on first row
            print(str(picture_index) + " first row")
        elif picture_index % dimension[0] == 0:  # if on first column of each row
            print(str(picture_index) + " first of each column")
        else:  # if on >1 column on >1 row
            print(str(picture_index) + " on >1 column on >1 row")


def get_image_dirs(path_to_file):
    # Get list of all files in a given directory sorted by name
    # list_of_files = sorted(filter(os.path.isfile, glob.glob(path_to_file + 'tile_*')))
    list_of_files = glob.glob(path_to_file + 'tile_*.tif')
    # sort them using 'human sorting/natural sorting'
    def atoi(text):
        return int(text) if text.isdigit() else text

    def natural_keys(text):
        '''
        alist.sort(key=natural_keys) sorts in human order
        http://nedbatchelder.com/blog/200712/human_sorting.html
        (See Toothy's implementation in the comments)
        '''
        return [atoi(c) for c in re.split(r'(\d+)', text)]

    list_of_files.sort(key=natural_keys)
    return list_of_files


def get_images(list_of_files):
    """"make a list of images to store images
    loads list with images using address from list_of_files"""
    images = []

    for i in range(0, len(list_of_files)):
        with Image.open(list_of_files[i]) as im:
            images.append(im.copy())
    return images

def get_images_opencv(list_of_files):
    """"make a list of images to store images
    loads list with images using address from list_of_files"""
    images = []

    for i in range(0, len(list_of_files)):
        images.append(cv2.imread(list_of_files[i], 0))
    return images

# Iterate over sorted list of files and print the file paths
# one by one.
"""
for file_path in list_of_files:
    print(file_path)
"""


def stitch_tile(path_to_file, xx, yy):
    images = get_image_dirs(path_to_file)

    if len(images) >= xx * yy:
        pass
    else:
        raise ValueError('not enough images in path_to_file !!!!!!!!!!!')

    # stitching by just pasting side by side, does not account for overlap
    """
    sq_x = xx
    sq_y = yy
    img_x = (Image.open(images[0]).size[0])
    img_y = (Image.open(images[0]).size[1])
    img_mode = (Image.open(images[0]).mode)

    new_image = Image.new(img_mode, (img_x * sq_x, img_y * sq_y))

    # stitching using no overlap
    x = 0
    y = 0
    cnt = 0
    for i in range(0, len(images)):
        with Image.open(images[i]) as img:
            new_image.paste(img, (x, y))
            cnt += 1
            x += img_x
            if cnt == sq_x:
                x = 0
                y += img_y
                cnt = 0
            else:
                pass
    """
    # stitching using overlap coordinate list
    # reads the .txt file there and gets the estimated overlap generated by
    # micromanager when the images are taken

    offsetList = [[0] * 2 for _ in range(xx * yy)]
    with open(path_to_file + '/' + "TileConfiguration.registered.txt") as f:
        contents = f.readlines()
        for i in range(4, len(contents)):
            # lstrip, rstrip, and split isolates the line string in to a pair
            for j, coord in enumerate(contents[i].lstrip("tile_.tif;0123456789 ").lstrip("(").rstrip(")\n").split(",")):
                # float converts the string with a decimal in to a float and round rounds in to a int
                offsetList[i - 4][j] = round(float(coord))

    print(offsetList)
    img_x = (Image.open(images[0]).size[0])
    img_y = (Image.open(images[0]).size[1])
    img_mode = Image.open(images[0]).mode

    new_image = Image.new(img_mode, (img_x + offsetList[xx - 1][0], img_y + offsetList[xx * yy - 1][1]))

    """print("new_image shape: ", end="")
    print(new_image.size)"""

    for i in range(0, len(offsetList)):
        with Image.open(images[i]) as img:
            new_image.paste(img, (offsetList[i][0], offsetList[i][1]))

    return new_image


# save by converting to jpeg first (doesn't work)
"""
out = stich_tile(dir_name, 4, 4).convert("RGB")
out.save("test.JPEG", quality=90)
"""


# saves to desktop by default, default name is image
def save_image(path_to_file=os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), file_name="image"):
    filesinfolder = [f for f in listdir(path_to_file) if isfile(join(path_to_file, f))]
    highestindex = 0
    for i, file in enumerate(filesinfolder):
        if (file.lstrip(file_name).rstrip(".tiff") != '') and ((file.rstrip("0123456789.tiff") == file_name)):
            highestindex = int(file.lstrip(file_name).rstrip(".tiff"))
    if highestindex == 0:
        stitch_tile(dir_name, 4, 4).save(path_to_file + "/" + file_name + ".tiff", "TIFF")
    else:
        stitch_tile(dir_name, 4, 4).save(path_to_file + "/" + file_name + str(highestindex + 1) + ".tiff", "TIFF")

    save_image(path_to_file=save_loc, file_name=save_name)
