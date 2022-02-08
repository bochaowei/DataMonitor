from threading import Thread
from shutil import copyfile
from PIL import ImageTk, Image
import json
import datetime
import statistics
import io
from PIL import Image, ImageEnhance, ImageOps, ImageFilter, ImageChops,ImageGrab,ImageMath
import PIL
import upload 
from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import numpy as np
import cv2
import time
import numpy
from scipy.stats import mode

def video():
    cv2.namedWindow("preview")
    vc = cv2.VideoCapture(0)
    if vc.isOpened(): # try to get the first frame
        rval, frame = vc.read()
    else:
        rval = False

    while rval:
        cv2.imshow("preview", frame)
        rval, frame = vc.read()
        key = cv2.waitKey(177)
        #cv2.imwrite('test.jpg',frame)
        #copyfile('test.jpg','test2.jpg')
        if key == 27: # exit on ESC
            break
    vc.release()
    cv2.destroyWindow("preview")
def recognition(decimal,bright,filename):
    def takefirst(elem):
        return elem[0]
    print('wait for 7 seconds')
    time.sleep(7)  
    condition=1
    contournumber=30
    wholelist=[]
    while condition:
        im=Image.open('tem.jpg')
        im=Image.open('test2.jpg')
        sizex=im.size[0]
        sizey=im.size[1]
        im_copy=numpy.array(im)
        im = im.convert('L')
        threshold=im_copy.max()/2
        if bright=='y':
            im = im.point(lambda x: 0 if x < threshold else 255)
        if bright=='n':
            im = im.point(lambda x: 0 if x > threshold else 255)
        #im.show()

        grayim=im.copy()
        grayim=numpy.array(grayim) #######here saved the grayim to be used later
        
        im = im.filter(ImageFilter.CONTOUR)
        #im.save('contour.jpg')
        #print(im.format, im.size, im.mode)
        img=numpy.array(im)



        #roi=cv2.imread("pressure.png")


        #roi_copy = roi.copy()
        #roi_hsv = cv2.cvtColor(roi, cv2.COLOR_RGB2HSV)
        #    # filter black color
        #mask1 = cv2.inRange(roi_hsv, np.array([0, 0, 0]), np.array([180, 255, 125]))
        #mask1 = cv2.morphologyEx(mask1, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
        #mask1 = cv2.Canny(mask1, 100, 300)
        #mask1 = cv2.GaussianBlur(mask1, (1, 1), 0)
        #mask1 = cv2.Canny(mask1, 100, 300)

            # mask1 = cv2.morphologyEx(mask1, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)))

        # Find contours for detected portion of the image
        cnts, hierarchy = cv2.findContours(img.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[0:contournumber] # get largest contour area
        rects = []
        minx=5000000
        maxx=-10
        ########draw rectangle around the contours
        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
            if h >= sizey/28 and w<=sizex/8 and h<sizey/2:
                    # if height is enough
                    # create rectangle for bounding
                rect = (x, y, w, h)
                rects.append(rect)
                #aa=cv2.rectangle(im_copy, (x, y), (x+w, y+h), (0, 255, 0), 1)       

        ######################### Get some basic statistics before reducing the rectangles
        ylist=[]
        xlist=[]
        wlist=[]
        hlist=[]

        for shape in rects:
            xlist.append(shape[0])
            ylist.append(shape[1])
            wlist.append(shape[2])
            hlist.append(shape[3])
        
        if wlist==[]:
            wlist.append(1)
            hlist.append(1)
            #condition=0
        meanw=statistics.mean(wlist)
        meanh=statistics.mean(hlist)
        ############the digits should have similar y (the devices are always horizontal)
        y_round=[]
        for shape in rects:
            y_round.append(10*round(shape[1]/10))

        modey=mode(y_round)[0]
        ###########delete the rectangles that far away from mode y or x direction not too close to side.
        newrects=rects.copy()
        for shape in rects:
            if (shape[1]-modey)**2>(meanh/2)**2 or (shape[0]-sizex)**2<(meanh)**2 or (shape[0]-sizex)**2<(meanh)**2:
                newrects.remove(shape)
            
                
        #########remove the smaller rectangles inside digits, and the list is sorted by x
        newrects.sort(key=takefirst)
        cleanrects=newrects.copy()
        for i in range(0,len(newrects)-1):
            if newrects[i+1][0]<newrects[i][0]+newrects[i][2]-2:
                cleanrects.remove(newrects[i+1])
        ################### update the statistics in rects
        ylist=[]
        xlist=[]
        wlist=[]
        hlist=[]
        for shape in cleanrects:
            xlist.append(shape[0])
            ylist.append(shape[1])
            wlist.append(shape[2])
            hlist.append(shape[3])
        if wlist==[]:
            wlist.append(1)
            hlist.append(1)
            #condition=0
        meanw=statistics.mean(wlist)
        meanh=statistics.mean(hlist)
        ############left some space for improving rectangles:reshape the rectangles only cover half of the zero
        finalrects=list(cleanrects.copy())
        if len(finalrects)>1:
            for i in range(1,len(cleanrects)):
                if cleanrects[i][3]< meanh*0.7:
                    
                    finalrects[i]=((cleanrects[i][0],cleanrects[i][1],cleanrects[i][2],cleanrects[i-1][3]))
                    
            for i in range(0,len(cleanrects)):   
                if cleanrects[i][2]<meanw*0.7:
                    if i>0:
                        finalrects[i]=((cleanrects[i][0]-round(cleanrects[i-1][2]*0.7),cleanrects[i-1][1],cleanrects[i-1][2],cleanrects[i-1][3]))                   
                    else:
                        finalrects[i]=((cleanrects[i][0]-round(cleanrects[i+1][2]*0.7),cleanrects[i+1][1],cleanrects[i+1][2],cleanrects[i+1][3]))
        ################################## here is to avoid 1 in the first line and avoid bright stuff before digits
    #    if len(finalrects)>1:
    #        if finalrects[0][2]<finalrects[1][3]/1.2 or finalrects[0][2]>finalrects[1][3]*1.1:
    #            del finalrects[0]
        ############################# here is to include possible 1 in the front or end, add a proper rectangle to it
    #    finalrects.append((finalrects[len(finalrects)-1][0]+round(finalrects[len(finalrects)-1][2]*1.2),finalrects[len(finalrects)-1][1],finalrects[len(finalrects)-1][2],finalrects[len(finalrects)-1][3]))
        #finalrects.append((finalrects[0][0]-round(finalrects[0][2]*1.15),finalrects[0][1],finalrects[0][2],finalrects[0][3]))
        finalrects.sort(key=takefirst)
        ###########here is to see the final rectangles
        for shape in finalrects:
            (x,y,w,h)=shape
            bb=cv2.rectangle(im_copy, (x, y), (x+w, y+h), (0, 255, 0), 1)
            
        #cv2.imwrite('box.png',bb)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        ##########start to look for digits
        DIGITS_LOOKUP = {
            (1, 1, 1, 0, 1, 1, 1): 0,
            (0, 0, 1, 0, 0, 1, 0): 1,
            (1, 0, 1, 1, 1, 0, 1): 2,
            (1, 0, 1, 1, 0, 1, 1): 3,
            (0, 1, 1, 1, 0, 1, 0): 4,
            (1, 1, 0, 1, 0, 1, 1): 5,
            (1, 1, 0, 1, 1, 1, 1): 6,
            (1, 0, 1, 0, 0, 1, 0): 7,
            (1, 1, 1, 1, 1, 1, 1): 8,
            (1, 1, 1, 1, 0, 1, 1): 9,
            (1, 1, 1, 1, 0, 1, 0): 9
        }

        #for shape in finalrects:
        #    (x,y,w,h)=shape
        #    for x in range(x,x+w):
        #        for y in range
        
        digits = [] 
        for shape in finalrects:
            (x,y,w,h)=shape
            roi = grayim[y:y + h, x:x + w]
            dH=round(w*6/8)
            dW=w//6
            
            dHC=h//15
            margin=w//7
             
            segments = [
                    ((margin, 0), (w-margin, dW)),  # top
                    ((0, margin), (dW, dH)), # top-left
                    ((w - dW, margin), (w, dH)), # top-right
                    ((margin, (h // 2) -dW//2) , (w-margin, (h // 2)+dW//2 )), # center
                    ((0, h //2+dW//2), (dW, h-margin)), # bottom-left
                    ((w - dW, h //2+dW//2), (w, h-margin)), # bottom-right
                    ((margin, h - dW), (w-margin, h))   # bottom
                ]
            on = [0] * len(segments)    

            for (i, ((xA, yA), (xB, yB))) in enumerate(segments):
                segROI = roi[yA:yB, xA:xB]
                total = cv2.countNonZero(segROI)
                area = (xB - xA) * (yB - yA)
                if total / float(area+1) > 0.15:
                    on[i]= 1
                    
            if tuple(on) in DIGITS_LOOKUP:
                digit = DIGITS_LOOKUP[tuple(on)]
                digits.append(digit)
            else:
                #print(tuple(on))
                digit=' '
            
            #cv2.rectangle(im_copy, (x, y), (x + w, y + h), (0, 255, 0), 1)
            #cv2.putText(im_copy, str(digit), (x - 10, y - 10),cv2.FONT_HERSHEY_SIMPLEX, 1.7, (0, 255, 0), 2)

        if digits==[]:
            print('Can not recognize digits')
            #condition=0
            
        # display the digits
        print(digits)
        #cv2.imshow("Output", im_copy)
        #cv2.imwrite('result.jpg',im_copy)
        #cv2.waitKey(0)
        #####################################################begin analysis

        tens=10**(len(digits)-decimal-1)
        final_digits=0
        for i in range(0,len(digits)):
            final_digits=final_digits+digits[i]*tens
            tens=tens/10
        currenttime = datetime.datetime.now()
        #formattime = currenttime.strftime("%Y-%m-%d %H:%M:%S")
        output=[final_digits,str(currenttime)]
        wholelist.append(output)
        with open(filename,'w') as f:
              json.dump(wholelist,f)
        upload.upload_to_bucket('data.txt', filename, 'dataset111')
        time.sleep(0.417)
decimal=int(input("how many decimal do you have?"))
bright=input("Is your digits bright?(y/n)")
filename=input("Name your local data file")
filename=filename+".txt"
Thread(target = video).start()
Thread(target = recognition(decimal,bright,filename)).start()

print('done')



