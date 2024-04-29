import sys
import os
import cv2
import numpy as np
import math
import random
#from scipy import ndimage
#from imageio import imread
from PIL import Image
from matplotlib import pyplot as plt
import warnings
warnings.filterwarnings("ignore")

#PARAM
template_path = "template.png"
accessory1 = "Head/Head_MiniDucker_Test.png"
head_pixel = [0, 0] # xy value of the top left hat area (Already set to head from ProCreate Drawing)
col_list = [[1,3,255]] #Preset colour list
###


def isColour(pix, col): #Col as an array of RGB
    if pix[0] == col[0] and pix[1] == col[1] and pix[2] == col[2]:
        return True
    else:
        return False
            

def avg_pixel(img): #Find avg pixel of an accessory img with white/black background
    pixel_count = 0
    x_total = 0
    y_total = 0
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            if not isColour(img[x][y], [255, 255, 255]):
                pixel_count += 1
                x_total += x
                y_total += y
    return [(x_total/pixel_count), (y_total/pixel_count)]
    
def addAccessory(img, acc, x, y):
    for x1 in range(acc.shape[0] - 1):
        for y1 in range(acc.shape[1] - 1):
            if x1+x < acc.shape[0] and y1 + y < acc.shape[1]:
                if not isColour(acc[x1][y1], [255, 255, 255]):
                    img[x1 + x][y1 + y][0] = acc[x1][y1][0]
                    img[x1 + x][y1 + y][1] = acc[x1][y1][1]
                    img[x1 + x][y1 + y][2] = acc[x1][y1][2]
    return img

def changeColour(img, col, new_col): #Colour as an array of RGB
    new_img = img
    for x in range(new_img.shape[0]):
        for y in range(new_img.shape[1]):
            if isColour(new_img[x][y], col):
                new_img[x][y][0] = new_col[0]
                new_img[x][y][1] = new_col[1]
                new_img[x][y][2] = new_col[2]
    return new_img

def create_colour_list(increment):
    r_col = 0
    g_col = 0
    b_col = 0
    col_list = []
    while r_col < 255:
        g_col = 0
        if r_col + increment < 255:
            r_col += increment
        else:
            break
        while g_col < 255:
            b_col = 0
            if g_col + increment < 255:
                g_col += increment
            else:
                break
            while b_col < 255:
                col_list.append([r_col, g_col, b_col])
                b_col += increment
    return col_list

try:
    img = cv2.imread(template_path)
except AttributeError:
    print("Template not found.")
    exit()

try:
    acc_img = cv2.imread(accessory1)
except AttributeError:
    print("Template not found.")
    exit()

print("Adding Accessory...")
addAccessory(img, acc_img, head_pixel[0], head_pixel[1])
print("Added Accessory!")
#col_list = create_colour_list(50)

cv2.imwrite("output.png", img)

img_counter = 0
for col in col_list:
    img = cv2.imread("output.png")
    print("Converting Colour...")
    new_img = changeColour(img, [253,253,253], [150, 50, 250])
    print("Converting Colour!")
    cv2.imwrite("Output/testOutput%d.png" % img_counter, new_img)
    img_counter += 1
print("COMPLETE!")