# used to change filepaths
import os

import matplotlib as mpl
import matplotlib.pyplot as plt
from IPython.display import display
#matplotlib inline

import pandas as pd
import numpy as np

# import Image from PIL
# ... YOUR CODE FOR TASK 1 ...

from skimage.feature import hog
from skimage.color import rgb2gray

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA