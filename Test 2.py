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
        #print(shapes[:][:,:,:])
        i=0

import pandas as pd

pd.DataFrame(range(10**1), dtype=np.int64)==''  # OK, just a FutureWarning
pd.DataFrame(range(10**2), dtype=np.int64)==''  # OK, just a FutureWarning
pd.DataFrame(range(10**3), dtype=np.int64)==''  # OK, just a FutureWarning
pd.DataFrame(range(10**4), dtype=np.int64)==''  # OK, just a FutureWarning
pd.DataFrame(range(10**5), dtype=np.int64)==''  # ValueError: unknown type str32
pd.DataFrame(range(10**5), dtype=np.int64)=='  '  # ValueError: unknown type str64
pd.DataFrame(range(10**5), dtype=np.int64)=='    '  # ValueError: unknown type str128