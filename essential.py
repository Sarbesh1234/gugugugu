#importing the libraries
import numpy as np #for mathematical calculations
import cv2 #for face detection and other image operations
import dlib #for detection of facial landmarks ex:nose,jawline,eyes
from sklearn.cluster import KMeans #for clustering
from app import *


def calculate_shape(imagepath, sex):

    face_cascade_path = "faceshapes.xml"
    #.dat file for detecting facial landmarks
    predictor_path = "shape_predictor_68_face_landmarks.dat"

    #create the haar cascade for detecting face and smile
    faceCascade = cv2.CascadeClassifier(face_cascade_path)

    #create the landmark predictor
    predictor = dlib.shape_predictor(predictor_path)

    #read the image
    image = cv2.imread(imagepath)
    text = cv2.imread("black.jpg")

    #resizing the image to 0 cols and 500 rows
    image = cv2.resize(image, (504, 500))
    text = cv2.resize(text,(1008,300))

    #making another copy
    original = image.copy()


    #convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #apply a Gaussian blur with a 3 x 3 kernel to help remove high frequency noise
    gauss = cv2.GaussianBlur(gray,(3,3), 0)

    #Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gauss,
        scaleFactor=1.05,
        minNeighbors=5,
        minSize=(100,100),
        flags=cv2.CASCADE_SCALE_IMAGE
        )
    #More detection of faces in the image
    print("found {0} faces!".format(len(faces)) )

    for (x,y,w,h) in faces:
        #drawing a rectangle around the faces
        cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), 2)
        #converting the opencv rectangle coordinates to Dlib rectangle
        dlib_rect = dlib.rectangle(int(x), int(y), int(x+w), int(y+h))
        #detecting the landmarks
        detected_landmarks = predictor(image, dlib_rect).parts()
        #converting to np matrix
        landmarks = np.matrix([[p.x,p.y] for p in detected_landmarks])
        #landmarks array contains indices of landmarks.

    #making another copy  for showing final results
    results = original.copy()

    for (x,y,w,h) in faces:
        #draw a rectangle around the faces
        cv2.rectangle(results, (x,y), (x+w,y+h), (0,255,0), 2)
        #making temporary copy
        temp = original.copy()
        #getting area of interest from image i.e., forehead (25% of face)
        forehead = temp[y:y+int(0.25*h), x:x+w]
        rows,cols, bands = forehead.shape
        X = forehead.reshape(rows*cols,bands)

        #kmeans
        kmeans = KMeans(n_clusters=2,init='k-means++',max_iter=300,n_init=10, random_state=0)
        y_kmeans = kmeans.fit_predict(X)
        for i in range(0,rows):
            for j in range(0,cols):
                if y_kmeans[i*cols+j]==True:
                    forehead[i][j]=[255,255,255]
                if y_kmeans[i*cols+j]==False:
                    forehead[i][j]=[0,0,0]
        #Steps to get the length of forehead
        #1.get midpoint of the forehead
        #2.travel left side and right side
        #the idea here is to detect the corners of forehead which is the hair.
        #3.Consider the point which has change in pixel value (which is hair)
        forehead_mid = [int(cols/2), int(rows/2) ] #midpoint of forehead
        lef=0
        #gets the value of forehead point
        pixel_value = forehead[forehead_mid[1],forehead_mid[0] ]
        for i in range(0,cols):
            #enters if when change in pixel color is detected
            if forehead[forehead_mid[1],forehead_mid[0]-i].all()!=pixel_value.all():
                lef=forehead_mid[0]-i
                break;
        left = [lef,forehead_mid[1]]
        rig=0
        for i in range(0,cols):
            #enters if when change in pixel color is detected
            if forehead[forehead_mid[1],forehead_mid[0]+i].all()!=pixel_value.all():
                rig = forehead_mid[0]+i
                break;
        right = [rig,forehead_mid[1]]

    #drawing line1 on forehead with circles
    #specific landmarks are used.
    line1 = np.subtract(right+y,left+x)[0]


    #drawing line 2 with circles
    linepointleft = (landmarks[1,0],landmarks[1,1])
    linepointright = (landmarks[15,0],landmarks[15,1])
    line2 = np.subtract(linepointright,linepointleft)[0]
    cv2.line(results, linepointleft,linepointright,color=(0,255,0), thickness = 2)
    cv2.putText(results,' Line 1', linepointleft,fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=0.5,color=(0,255,0), thickness=2)
    cv2.circle(results, linepointleft, 5, color=(255,0,0), thickness=-0)
    cv2.circle(results, linepointright, 5, color=(255,0,0), thickness=-0)

    #drawing line 3 with circles
    linepointleft = (landmarks[3,0],landmarks[3,1])
    linepointright = (landmarks[13,0],landmarks[13,1])
    line3 = np.subtract(linepointright,linepointleft)[0]
    cv2.line(results, linepointleft,linepointright,color=(0,255,0), thickness = 2)
    cv2.putText(results,' Line 2',linepointleft,fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=0.5,color=(0,255,0), thickness=2)
    cv2.circle(results, linepointleft, 5, color=(255,0,0), thickness=-0)
    cv2.circle(results, linepointright, 5, color=(255,0,0), thickness=-0)

    #drawing line 4 with circles
    linepointbottom = (landmarks[8,0],landmarks[8,1])
    linepointtop = (landmarks[8,0],y)
    line4 = np.subtract(linepointbottom,linepointtop)[1]
    cv2.line(results,linepointtop,linepointbottom,color=(0,255,0), thickness = 2)
    cv2.putText(results,' Line 3',linepointbottom,fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=0.5,color=(0,255,0), thickness=2)
    cv2.circle(results, linepointtop, 5, color=(255,0,0), thickness=-0)
    cv2.circle(results, linepointbottom, 5, color=(255,0,0), thickness=-0)
    #print(line1,line2,line3,line4)

    similarity = np.std([line1,line2,line3])
    #print("similarity=",similarity)
    ovalsimilarity = np.std([line2,line4])
    #print('diam=',ovalsimilarity)

    #we use arcustangens for angle calculation
    ax,ay = landmarks[3,0],landmarks[3,1]
    bx,by = landmarks[4,0],landmarks[4,1]
    cx,cy = landmarks[5,0],landmarks[5,1]
    dx,dy = landmarks[6,0],landmarks[6,1]
    import math
    from math import degrees
    alpha0 = math.atan2(cy-ay,cx-ax)
    alpha1 = math.atan2(dy-by,dx-bx)
    alpha = alpha1-alpha0
    angle = abs(degrees(alpha))
    angle = 180-angle

    for i in range(1):
      if similarity<10:
        if angle<160:
          print('squared shape.Jawlines are more angular')
          if sex is "Male":
              x = 'Squared shape face: buzz, crew cut, side part'
              img1 = cv2.imread("Men/Square/Buzz.jpg")
              img2 = cv2.imread("Men/Square/CrewCut.jpg")
              img3 = cv2.imread("Men/Square/SidePart.jpg")

          else:
              img1 = cv2.imread("Women/SquareW/Bangs.jpg")
              img2 = cv2.imread("Women/SquareW/LongLen.jpg")
              img3 = cv2.imread("Women/SquareW/Ponytail.jpg")
              x = 'Squared shaped face: bangs, long length, ponytail'
          break
        else:
          print('round shape.Jawlines are not that angular')
          if sex is "Male":
              img1 = cv2.imread("Men/Round/BrushedBack.jpg")
              img2 = cv2.imread("Men/Round/Buzz.jpg")
              img3 = cv2.imread("Men/Round/SidePart.jpg")
              x = 'Round shaped face: brushed back, buzz, sidepart'

          else:
              img1 = cv2.imread("Women/RoundW/Bun.jpg")
              img2 = cv2.imread("Women/RoundW/LongLen.jpg")
              img3 = cv2.imread("Women/RoundW/ShoulderLen.jpg")
              x = 'Round shaped face: bun, long length, shoulder length'
          break
      if line3>line1:
        if angle<160:
          print('triangle shape.Forehead is more wider')
          if sex is "Male":
              x = 'Triangle shaped face: brushed back, buzz, side part'
              img1 = cv2.imread("Men/Triangle/BrushedBack.jpg")
              img2 = cv2.imread("Men/Triangle/Buzz.jpg")
              img3 = cv2.imread("Men/Triangle/SidePart.jpg")

          else:
              x = 'Triangle shaped face: bun, short length, shoulder length'
              img1 = cv2.imread("Women/TriangleW/Bun.jpg")
              img2 = cv2.imread("Women/TriangleW/ShortLen.jpg")
              img3 = cv2.imread("Women/TriangleW/ShoulderLen.jpg")

          break
      if ovalsimilarity<10:
        print('diamond shape. line2 & line4 are similar and line2 is slightly larger')
        if sex is "Male":
            x= 'Diamond shaped face: brushed back, buzz, undercut'
            img1 = cv2.imread("Men/Diamond/BrushedBack.jpg")
            img2 = cv2.imread("Men/Diamond/Buzz.jpg")
            img3 = cv2.imread("Men/Diamond/Undercut.jpg")

        else:
            x = 'Diamond shaped face: bun, ponytail, short length'
            img1 = cv2.imread("Women/DiamondW/Bun.jpg")
            img2 = cv2.imread("Women/DiamondW/Ponytail.jpg")
            img3 = cv2.imread("Women/DiamondW/ShortLen.jpg")
        break
      if line4 > line2:
        if angle<160:
          print('rectangular. face length is largest and jawline are angular ')
          if sex is "Male":
              x = 'Rectangle shaped face: fringe, sidepart, undercut'
              img1 = cv2.imread("Men/Rectangle/Fringe.jpg")
              img2 = cv2.imread("Men/Rectangle/SidePart.jpg")
              img3 = cv2.imread("Men/Rectangle/Undercut.jpg")

          else:

              x= 'Rectangle shaped face: bangs, bun, shoulder length haircut'
              img1 = cv2.imread("Women/RectangleW/Bangs.jpg")
              img2 = cv2.imread("Women/RectangleW/Bun.jpg")
              img3 = cv2.imread("Women/RectangleW/ShoulderLen.jpg")
          break;
        else:
          print('oblong. face length is largest and jawlines are not angular')
          if sex is "Male":
              x= 'Oblong shaped face: buzz, fringe, side part cut'
              img1 = cv2.imread("Men/Oblong/Buzz.jpg")
              img2 = cv2.imread("Men/Oblong/Fringe.jpg")
              img3 = cv2.imread("Men/Oblong/SidePart.jpg")

          else:
              #x = 'You have a oblong shaped face! Rock braids,a ponytail, or a shoulder length since your face length is largest and jawlines are not angular'
              x = 'Oblong shaped face: braids,ponytail,shoulder length'


              img1 = cv2.imread("Women/OblongW/Braids.jpg")
              img2 = cv2.imread("Women/OblongW/Ponytail.jpg")
              img3 = cv2.imread("Women/OblongW/ShoulderLen.jpg")
          break;
      print("Damn! Contact the developer")

    img1 = cv2.resize(img1, (336,500)) # axis zero
    img2 = cv2.resize(img2, (336,500)) # axis one
    img3 = cv2.resize(img3, (336,500))
    output = np.concatenate((original,results), axis=1)

    gu = np.concatenate((img1,img2),axis=1)
    gu = np.concatenate((gu,img3),axis=1)

    output = np.concatenate((output, gu), axis=0)
    output = np.concatenate((output,text),axis=0)
    cv2.putText(output,
                x,
                org=(0, 1100), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                color=(255, 255, 255), thickness=3)
    #output = np.concatenate((output, img2), axis=0)
    # output = np.concatenate((output, img3), axis=0)
    cv2.imshow('output',output)
    cv2.waitKey(delay=0)