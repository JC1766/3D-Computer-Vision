import numpy as np
import sys
import cv2
from PIL import Image
import pickle
import time
from scipy.signal import medfilt
from scipy.ndimage.filters import maximum_filter as maxfilt

c0 = Image.open("cam00_00023_0000008550.png")
c1 = Image.open("cam01_00023_0000008550.png")
c2 = Image.open("cam02_00023_0000008550.png")
c3 = Image.open("cam03_00023_0000008550.png")
c4 = Image.open("cam04_00023_0000008550.png")
c5 = Image.open("cam05_00023_0000008550.png")
c6 = Image.open("cam06_00023_0000008550.png")
c7 = Image.open("cam07_00023_0000008550.png")