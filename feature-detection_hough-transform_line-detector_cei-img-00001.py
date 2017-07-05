import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib as mpl
import opencv_custom_gui_functions

print "Using OpenCV version "+str(cv2.__version__)

displayWidth = 1920
displayHeight = 1080

fillFactor = 0.6
pictureBoxWidth = int(displayWidth*fillFactor)
pictureBoxHeight = int(displayHeight*fillFactor) 

resMode = 1 #use 1 to scale resolution to 1.3MP (1296x964) or 0 to use the original resolution

#img = cv2.imread("orig379.png") #image near the grass on the east side of parking lot (facing east)
#img = cv2.imread("orig2593.png") #facing west, halfway down
#img = cv2.imread("orig1234.png") #facing west, halfway down
img = cv2.imread("test60-original_image.bmp") #really dark
try:
    print "original image size: " + str(img.shape[:2])
except:
    print "Check input image file path."
    exit()


#[np.size(image, 0), np.size(image, 1)]


#match the resolution of the point grey chameleon (1.3MP)
if (resMode == 1): img = cv2.resize(img, (1296,964))
print "performing Hough Transform Line Detection on an image of size: " + str(img.shape[:2])

rows,cols = img.shape[:2]

#do not rotate
#M = cv2.getRotationMatrix2D((cols/2,rows/2),53,1)
#img = cv2.warpAffine(img,M,(cols,rows))

#perform the hough transform on the image

#gaussian blur
smooth = cv2.GaussianBlur(img,(7,7),0)

gray = cv2.cvtColor(smooth,cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(gray,50,150,apertureSize = 3)

lines = cv2.HoughLines(edges,1,np.pi/180,200)



numLines = len(lines)



numPairs = 0
for line in lines[:2]:
    for rho,theta in line:
        numPairs = numPairs + 1

linePairs = []



imgWithLines = img.copy()



i = 0
for line in lines:
    for rho,theta in line:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 10000*(-b))
        y1 = int(y0 + 10000*(a))
        x2 = int(x0 - 10000*(-b))
        y2 = int(y0 - 10000*(a))
        linePairs.append([x1,y1,x2,y2])
        i = i + 1
       # cv2.line(imgWithLines,(x1,y1),(x2,y2),(0,0,255),2)


imgsToShow = [img, smooth, gray, edges, imgWithLines] 
imgTypes = ['bgr', 'bgr', 'gray', 'binary', 'bgr']

#opencv_custom_gui_functions.showImsSameWindow(imgsToShow, imgTypes, pictureBoxHeight, pictureBoxWidth, 2,3)
opencv_custom_gui_functions.showImsInSequence('set1', imgsToShow, 4)

title = "set1"

#cv2.namedWindow(title)#, cv2.WND_PROP_FULLSCREEN)          
#cv2.setWindowProperty(title, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

n = 3

def nothing(x):
    pass

# Create a black image, a window
img = np.zeros((300,512,3), np.uint8)
cv2.namedWindow('image', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# create trackbars for color change
cv2.createTrackbar('numLines','image',3,numLines,nothing)


while(1):
    
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    # get current positions of four trackbars
    n = cv2.getTrackbarPos('numLines','image')
    if n > 0:
        for p in linePairs[:n]:
            cv2.line(imgWithLines,(p[0],p[1]),(p[2],p[3]),(0,0,255),2)

    #imgWithLines[:,:,2] = int(float(n)/float(numLines)*255.0)
    cv2.imshow('image',imgWithLines)

cv2.destroyAllWindows()

#now we need to filter the lines so we get the ones we are interested in

print "done"
