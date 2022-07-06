#!/usr/bin/python
#source: random 
from msilib import Feature
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

def getEveScreen():
    return gEveScreen

def getEveScreenNumpy():
   return gEveScreenNumpy

def getEveScreenWidth():
  return gScreenWidth

def boardToDebugRender(binaryList):
  finalImage=[]
  for binarycolor in binaryList:
    finalColor = binarycolor[GREEN]#(binarycolor[RED] <<3)+ (binarycolor[GREEN] << 2) + (binarycolor[BLUE] <<1)
  return finalImg

def colorize(listoflist):
  a = []
  for index in range(395*395):
    count =1 
    found = False
    for x in listoflist:
      if index in x["clusterIndexes"]:
        found = True
        a.append(count)
        break
      count +=1
    if found == False:
      a.append(0)

  return a

PRINT_LEVEL = 0 
def myprint(str, level=0):
  if level >= PRINT_LEVEL:
     print(str)
    
def testClicks():
  sleeptime = 0.5
  moveMouse(*BUTTON_CORD["Continue"])
  sleep(sleeptime)
  moveMouse(*BUTTON_CORD["Nucleus01"])
  sleep(sleeptime)
  moveMouse(*BUTTON_CORD["Nucleus02"])
  sleep(sleeptime)
  moveMouse(*BUTTON_CORD["Nucleus03"])
  sleep(sleeptime)
  moveMouse(*BUTTON_CORD["Nucleus04"])
  sleep(sleeptime)
  moveMouse(*BUTTON_CORD["Nucleus05"])
  sleep(sleeptime)
  moveMouse(*BUTTON_CORD["Nucleus06"])
  sleep(sleeptime)
  moveMouse(*BUTTON_CORD["Nucleus07"])
  sleep(sleeptime)
  moveMouse(*BUTTON_CORD["Nucleus08"])
  sleep(sleeptime)
  moveMouse(*BUTTON_CORD["Nucleus09"])
  sleep(sleeptime)
  moveMouse(*BUTTON_CORD["Cytoplasm01"])
  sleep(sleeptime)
  moveMouse(*BUTTON_CORD["Cytoplasm02"])
  sleep(sleeptime)
  moveMouse(*BUTTON_CORD["Cytoplasm03"])
  sleep(sleeptime)
  moveMouse(*BUTTON_CORD["Cytoplasm04"])
  sleep(sleeptime)
  moveMouse(*BUTTON_CORD["Cytoplasm05"])
  sleep(sleeptime)
  moveMouse(*BUTTON_CORD["Cytoplasm06"])
  sleep(sleeptime)
  moveMouse(*BUTTON_CORD["Cytoplasm07"])
  sleep(sleeptime)
  moveMouse(*BUTTON_CORD["Cytoplasm08"])
  sleep(sleeptime)
  moveMouse(*BUTTON_CORD["Cytoplasm09"])
  sleep(sleeptime)
  moveMouse(*BUTTON_CORD["Cytoplasm10"])
  sleep(sleeptime)
  moveMouse(*BUTTON_CORD["Cytoplasm11"])
  sleep(sleeptime)
  moveMouse(*BUTTON_CORD["Cytoplasm12"])
  sleep(sleeptime)
  moveMouse(*BUTTON_CORD["Cytoplasm13"])
  sleep(sleeptime)
  moveMouse(*BUTTON_CORD["Cytoplasm14"])
  sleep(sleeptime)
  moveMouse(*BUTTON_CORD["Periphery01"])
  sleep(sleeptime)
  moveMouse(*BUTTON_CORD["Periphery02"])
  sleep(sleeptime)
  moveMouse(*BUTTON_CORD["Periphery03"])
  sleep(sleeptime)
  moveMouse(*BUTTON_CORD["Misc"])
  sleep(sleeptime)
  moveMouse(*BUTTON_CORD["Not01"])
  sleep(sleeptime)
  moveMouse(*BUTTON_CORD["Not02"])
  sleep(sleeptime)

def findColor(r,g,b):
  pixelIndex = 0 
  for pix in gEveScreen:
    if pix[0] == r and pix[1] ==g and pix[2] ==b:
      break
    pixelIndex +=1

  y=int(pixelIndex/gScreenWidth)
  x=int(((pixelIndex / gScreenWidth) - y) * gScreenWidth)
  x += gScreenOffsetL
  y += gScreenOffsetT
  #myprint("pixindex : " + str(pixelIndex) + ",Coord(" +str(x) + "," + str(y) + ") with window size(" + str(gScreenWidth) + "," + str(gScreenHeight)
  return (x,y)

RED = 0
GREEN = 1 
BLUE = 2
SVM_MACHINE ={}
SCALER = None
MACHINE_ALL = None
NUM_PROC = 6
ERROR_FILE="errors.json"
RUN_START_TIME=""

SPECIAL_BUTTON_DATA = {
    "Continue": "ref\\ContinueBtn2.png",
    "Submit": "ref\\SubmitBtn.png"
}

BUTTON_DATA = {
  #"test": "tests:\\test.png"
  "Continue": "ref\\ContinueBtn2.png",
  "Submit": "ref\\SubmitBtn.png",
  "Cytoplasm01": "ref\\CytoplasmBtn01.png",
  "Cytoplasm02": "ref\\CytoplasmBtn02.png",
  "Cytoplasm03": "ref\\CytoplasmBtn03.png",
  "Cytoplasm04": "ref\\CytoplasmBtn04.png",
  "Cytoplasm05": "ref\\CytoplasmBtn05.png",
  "Cytoplasm06": "ref\\CytoplasmBtn06.png",
  "Cytoplasm07": "ref\\CytoplasmBtn07.png",
  "Cytoplasm08": "ref\\CytoplasmBtn08.png",
  "Cytoplasm09": "ref\\CytoplasmBtn09.png",
  "Cytoplasm10": "ref\\CytoplasmBtn10.png",
  "Cytoplasm11": "ref\\CytoplasmBtn11.png",
  "Cytoplasm12": "ref\\CytoplasmBtn12.png",
  "Cytoplasm13": "ref\\CytoplasmBtn13.png",
  "Cytoplasm14": "ref\\CytoplasmBtn14.png",
  "Nucleus01": "ref\\NucleusBtn01.png",
  "Nucleus02": "ref\\NucleusBtn02.png",
  "Nucleus03": "ref\\NucleusBtn03.png",
  "Nucleus04": "ref\\NucleusBtn04.png",
  "Nucleus05": "ref\\NucleusBtn05.png",
  "Nucleus06": "ref\\NucleusBtn06.png",
  "Nucleus07": "ref\\NucleusBtn07.png",
  "Nucleus08": "ref\\NucleusBtn08.png",
  "Nucleus09": "ref\\NucleusBtn09.png",
  "Periphery01": "ref\\Periphery01.png",
  "Periphery02": "ref\\Periphery02.png",
  "Periphery03": "ref\\Periphery03.png",
  "Misc": "ref\\MiscBtn01.png",
  "Not01": "ref\\NotBtn01.png",
  "Not02": "ref\\NotBtn02.png"
}

BUTTON_CORD={}
TRAINING_PATH="training"
TRAINING_DATA_NAME="Cytoplasm01"

gEveScreen =[]
gEveScreenAlpha=[]
gEveScreenNumpy=[]
gEveScreenAlphaNumpy =[]
gScreenOffsetT = 0 
gScreenOffsetL = 0 
gScreenWidth = 0 
gScreenHeight=0
BOARD_NUCLEUS_OFFSET = [414,466] #found that in paint in a screenshot ( should be exact as long as minimize the discovery window as much as possible)
BOARD_SIZE=[395,395] #The exact area is I think 400x400, but I'd rather miss a few pixel than get the border by mistake in my calculations.
MIN_FROM_AVERAGE=0.7

class TrainingData:
    def __init__(self):
      self.y=[]
      self.X=[]
      self.files=[]

class ProcessData:
    def __init__(self):
      self.colorAverage    = [0,0,0]
      self.totalGreenBlack = 0 
      self.totalGreenBlue  = 0 
      self.totalGreenRed   = 0 
      self.totalRed        = 0 
      self.totalBlue       = 0 
      self.totalBlack      = 0 
      self.totalGreenPixel = 0 
      self.averageRoundnessGreen = 0 
      self.per_of_red_with_green = 0 
      self.per_of_blue_with_green=0
      self.per_of_black_with_green=0
      self.averageSizeGreenFeatures=0
      self.binaryList=[]
      self.green=[]
      self.red =[]
      self.redn =[]
      self.greenn =[]
      self.bluen =[]
      self.resultButtons=[]
      self.cytoplasm=[]
      self.nucli = [] #list of already found nuclie so we don't count them twice
      self.greenFeatures=[]
      self.greenFeaturesRoundness=[]
    
    def __repr__(self):
      a = "color average (" + str(self.colorAverage) + \
        "),\r\nG/N " + str(self.totalBlack) + ", G/B " + str(self.totalGreenBlue) + ", G/R " + str(self.totalGreenRed) + \
        ")\r\ntotal RGBN(" + str(self.totalRed) + "," + str(self.totalGreenPixel) + "," + str(self.totalBlue) + "," + str(self.totalGreenBlack) + ")" \
        "\r\n avg round " + str(self.averageRoundnessGreen) +", average size green " + str(self.averageSizeGreenFeatures) + \
        "\r\n per Green + RBN(" + str(self.per_of_red_with_green) + "," + str(self.per_of_blue_with_green) + "," + str(self.per_of_black_with_green)
      return a

  # ===================================
  # INITIALIZATION AND UPDATE

  def getWindowByTitle(title_text,exact=False):
    pass


#machine learning alogrithim
#source: scikit-learn.org
def gen_machine_all():
  global MACHINE_ALL
  global SCALER
  SCALER = StandardScaler()
  featurejson=""
  with open("ref\\features.json",'r') as jsonfile:
     featurejson = json.load(jsonfile)

  #Load Training Data from json
  trainingSet = TrainingData()
  loadJSONTrainingData(trainingSet, featurejson["ALL"]["features"], featurejson["ALL"]["exlusion"])
  cats = getActiveCats(featurejson)
  loadAnswersCombined(trainingSet,cats)

  #missing text in code. 
  MACHINE_ALL = MLPClassifier(solver='lbgfs', alpha=10.0 hidden_layer_sizes=(150,29), random_state=1000, activation="relu", max_iter=4000, batch_size=10)

  SCALER.fit(trainingSet.X)
  trainingSet.X = Scaler.transform(trainingSet.X)
  MACHINE_ALL.fit(trainingSet.X,trainingSet.y)
  save_machine()

