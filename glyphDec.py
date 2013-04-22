#!/usr/bin/python
import cv #Import functions from OpenCV
import math

#functions

def mean(img, x, y, dx, dy):
        print type(img)
        roi = cv.SetImageROI(img, cv.Rectangle(x,y,dx,dy))
        
        return cv.cvAvg(img)


storage = cv.CreateMemStorage(0);

cv.NamedWindow('window', 0)
cv.NamedWindow('edges', 0)
cv.NamedWindow('source', 0)

image=cv.LoadImage('glyph5', cv.CV_LOAD_IMAGE_COLOR) #Load the image

blue=cv.CreateImage(cv.GetSize(image),8,1)
green=cv.CreateImage(cv.GetSize(image),8,1)
red=cv.CreateImage(cv.GetSize(image),8,1)
grey=cv.CreateImage(cv.GetSize(image),8,1)
canny = cv.CreateImage(cv.GetSize(grey), cv.IPL_DEPTH_8U, 1)
src = cv.CreateImage(cv.GetSize(image),8,3)
src = image

cv.CvtColor(image,grey,cv.CV_BGR2GRAY)
cv.Split(image, blue, green, red, None)


#cv.Threshold(grey, canny, 10, 255, cv.CV_THRESH_BINARY)

#cv.Laplace(grey, canny)
cv.Canny(grey, canny, 20,60)

#cv.Threshold(canny, canny, 30, 255, cv.CV_THRESH_BINARY)

color_dst = cv.CreateImage(cv.GetSize(grey), 8, 3)
#color_dst = canny

lines = cv.HoughLines2(canny, storage, cv.CV_HOUGH_PROBABILISTIC, 1, math.pi/180, 100, 50, 40)

ends = []
corners = []
quads = []
for line in lines:
        
        cv.Line(color_dst, line[0], line[1], cv.CV_RGB(255,0,0), 3, 8)

        ends.append([line[0][0], line[0][1]])
        ends.append([line[1][0], line[1][1]])
#print 'corners'
for end in ends:
        for test in ends[ends.index(end)+1:]:
                
                if abs(end[0] - test[0]) + abs(end[1] - test[1]) < 25:
                        corners.append([(end[0] + test[0])/2, (end[1] + test[1])/2])
                        break
        
#remove duplicates
for c in corners:
        for c2 in corners[corners.index(c)+1:]:
                if abs(c[0] - c2[0]) < 10 and abs(c[1] - c2[1]) < 10:
                        #print 'removed'
                        corners.remove(c2)
                        #print c
                        #print c2

#corners = [[900,260], [910,640], [550,290], [540,640]]

for a in corners:
        cv.Circle(color_dst, (a[0], a[1]), 20,  cv.CV_RGB(100,255,0))
        for b in corners[corners.index(a)+1:]:
                for c in corners[corners.index(b)+1:]:
                        for d in corners[corners.index(c)+1:]:
                                sa = a[0] + a[1]
                                sb = b[0] + b[1]
                                sc = c[0] + c[1]
                                sd = d[0] + d[1]
                                smax = max(sa, sb, sc, sd)
                                smin = min(sa, sb, sc, sd)
                                #c1 is top left corner, c3 is bottom right
                                if sa == smax:
                                        c3 = a
                                        if sb == smin:
                                                c1 = b
                                                c2 = c
                                                c4 = d
                                        elif sc == smin:
                                                c1 = c
                                                c2 = b
                                                c4 = d
                                        else:
                                                c1 = d
                                                c2 = b
                                                c4 = c
                                elif sb == smax:
                                        c3 = b
                                        if sa == smin:
                                                c1 = a
                                                c2 = c
                                                c4 = d
                                        elif sc == smin:
                                                c1 = c
                                                c2 = a
                                                c4 = d
                                        else:
                                                c1 = d
                                                c2 = a
                                                c4 = c
                                elif sc == smax:
                                        c3 = c
                                        if sa == smin:
                                                c1 = a
                                                c2 = b
                                                c4 = d
                                        elif sb == smin:
                                                c1 = b
                                                c2 = a
                                                c4 = d
                                        else:
                                                c1 = d
                                                c2 = a
                                                c4 = b
                                else:
                                        c3 = d
                                        if sa == smin:
                                                c1 = a
                                                c2 = b
                                                c4 = c
                                        elif sb == smin:
                                                c1 = b
                                                c2 = a
                                                c4 = d
                                        else:
                                                c1 = c
                                                c2 = a
                                                c4 = b                
                                
                                midx = (c1[0] + c3[0]) / 2
                                midy = (c1[1] + c3[1]) / 2
                                x4 = midx + (midx - c2[0])
                                y4 = midy + (midy - c2[1])
                                #cv.Circle(color_dst, (midx, midy), 30,  cv.CV_RGB(0,255,255))
                                #cv.Circle(color_dst, (x4, y4), 30,  cv.CV_RGB(255,255,0))
                                if abs(c4[0] - x4) < 30 and abs(c4[1] - y4) < 30:
                                        quads.append([c1, c2, c3, c4])
                                        cv.Circle(color_dst, (c1[0], c1[1]), 30,  cv.CV_RGB(0,200,100))
                                        cv.Circle(color_dst, (c2[0], c2[1]), 30,  cv.CV_RGB(0,150,150))
                                        cv.Circle(color_dst, (c3[0], c3[1]), 30,  cv.CV_RGB(0,100,200))
                                        cv.Circle(color_dst, (c4[0], c4[1]), 30,  cv.CV_RGB(0,50,250))
                                        cv.Line(src, (c1[0], c1[1]), (c2[0], c2[1]), cv.CV_RGB(255,255,0),3,4)
                                        cv.Line(src, (c2[0], c2[1]), (c3[0], c3[1]), cv.CV_RGB(255,255,0),3,4)
                                        cv.Line(src, (c3[0], c3[1]), (c4[0], c4[1]), cv.CV_RGB(255,255,0),3,4)
                                        cv.Line(src, (c4[0], c4[1]), (c1[0], c1[1]), cv.CV_RGB(255,255,0),3,4)
                                        
                                        #print mean(src, c3[0], c3[1], 5, 5)
                                        break

cv.ResizeWindow('window', color_dst.height, color_dst.width)
cv.ShowImage('window', color_dst) #Show the image
cv.ShowImage('edges', canny) #Show the image
cv.ShowImage('source', src) #Show the image
cv.WaitKey(0)
