from PIL import Image
from numpy import asarray
import matplotlib.pyplot as plt
import numpy as np
import itertools

edges = [[3,18],[5,22],[7.78]]
shapes = [[43,8,9],[5,22,6]]

print(shapes[:])
for xy in edges:
    if xy not in shapes[:][0:1]:
        print(shapes[:][:,:,:])