#!/usr/bin/python
import sys       #system
import os        #os interaction
import glob      #regex files
from time import strftime
from time import sleep
import win32gui  #windows gui
import win32ui   #windows ui
import win32api  
import numpy 
import json
import scipy.ndimage
import multiprocessing
from sklearn.externals import joblib
from PIL import Image
from sklearn import svm #SKLEARN, the machine learning library for newbies
from sklearn import cross_validation
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import label_ranking_average_precission_score
