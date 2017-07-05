import cv2
import numpy as np

def destroyAndShowMaximized(title, img):
    cv2.destroyAllWindows() 
    cv2.namedWindow(title, cv2.WND_PROP_FULLSCREEN)          
    cv2.setWindowProperty(title, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow(title,img)

def updateWindow(windowTitle, img):
    cv2.imshow(windowTitle, img)

def showImsInSequence(title, imgs, startAt = 0):
    print 'Press right arrow and left arrow to index through, and esc to exit.'
    i = startAt
    imgsLenL1 = len(imgs)-1
    cv2.namedWindow(title, cv2.WND_PROP_FULLSCREEN)          
    cv2.setWindowProperty(title, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow(title, imgs[i])
    while(True):
        key = cv2.waitKey(0)
        
        if key == 46 and i<imgsLenL1: #period 46
            i = i + 1
            updateWindow(title, imgs[i])
        elif key == 44 and i > 0:            #comma 44
            i = i - 1
            updateWindow(title, imgs[i])
        elif key == 27:
            cv2.destroyAllWindows()
            return

def showImsInSeqCustomWindow(windowTitle, imgs, startAt = 0, destroyOnExit = True):
    print 'Press right arrow and left arrow to index through, and esc to exit.'
    i = startAt
    imgsLenL1 = len(imgs)-1
    cv2.imshow(title, imgs[i])
    while(True):
        key = cv2.waitKey(0)
        
        if key == 46 and i<imgsLenL1: #period 46
            i = i + 1
            updateWindow(title, imgs[i])
        elif key == 44 and i > 0:            #comma 44
            i = i - 1
            updateWindow(title, imgs[i])
        elif key == 27:
            if destroyOnExit: cv2.destroyAllWindows()
            return

def showImsSameWindow(imgs, imgTypes, pictureBoxHeight, pictureBoxWidth, rowCount, columnCount):
    
    numImages = len(imgs)
    largestImgWidth = 0
    largestImgHeight = 0
    
    #get largest image width
    for img in imgs:
        rows,cols = img.shape[:2]
        if cols > largestImgWidth:
            largestImgWidth = cols
        if rows > largestImgHeight:
            largestImgHeight = rows


    factor = min(float(pictureBoxWidth)/float(largestImgWidth)/columnCount,
    
                    float(pictureBoxHeight)/float(largestImgHeight)/rowCount)
    

    #scale all the original images using this factor
    
    i = 0
    j = 0
    
    combinedRows,combinedCols = pictureBoxHeight,pictureBoxWidth
    combined_image = np.zeros((combinedRows,combinedCols,3), np.uint8)
    for img in imgs:
        origRows,origCols = img.shape[:2]
        img_Resize = cv2.resize(img, (int(origCols*factor),int(origRows*factor)))

        resizedRows,resizedCols = img_Resize.shape[:2]
        firstColPx = int(i*largestImgWidth*factor)
        lastColPx = firstColPx + resizedCols
        firstRowPx = int(j*largestImgHeight*factor)
        lastRowPx = firstRowPx + resizedRows 

        imgToAdd = img_Resize

        if (imgTypes[j*columnCount+i] == 'gray' or imgTypes[j*columnCount+i] == 'binary'):
            imgToAdd = cv2.cvtColor(img_Resize, cv2.COLOR_GRAY2BGR)
        #get the image depth
        #if len(img.shape) == 2: #if the image has a depth of 1
            #imgDepth = img.shape[2]
            #imgToAdd = 
        
        combined_image[firstRowPx:lastRowPx,firstColPx:lastColPx] = imgToAdd
        i = i+1
        if i == columnCount:
            i = 0
            j = j + 1

    cv2.imshow('combined_image', combined_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return