#!/usr/bin/python
import cv
import math
import sys

#cartesian distance between two points
def dist(p1, p2):
        return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)


#mean pixel intensity of a region
def mean(img, x, y, size=10):
                oldRoi = cv.GetImageROI(img)

                #make sure roi is within image bounds
                x = min(x, img.width-1)
                x = max(x, 0)
                y = min(y, img.height-1)
                y = max(y, 0)
                
                cv.SetImageROI(img, (x-size/2,y-size/2,size,size))
                avg = cv.Avg(img)

                cv.SetImageROI(img, oldRoi)

                return (avg[0]+avg[1]+avg[2])/3.0


#determines if a region is white or black
def isWhite(img, x, y, thresh = -1, size = 6):
                if thresh == -1:
                        #set threshold as image average intensity
                        avg = cv.Avg(img)
                        thresh = (avg[0]+avg[1]+avg[2])/3.0
                        
                return mean(img, int(x), int(y), size) > thresh


#finds the corners in a list of lines
def getCorners(lines):
        ends = []
        corners = []

        for line in lines:
                ends.append([line[0][0], line[0][1]])
                ends.append([line[1][0], line[1][1]])

        for end in ends:
                for test in ends[ends.index(end)+1:]:
                        if abs(end[0] - test[0]) + abs(end[1] - test[1]) < 30:
                                corners.append([(end[0] + test[0])/2, (end[1] + test[1])/2])
                                break
                                
        #remove duplicates
        for c in corners:
                for c2 in corners[corners.index(c)+1:]:
                        if abs(c[0] - c2[0]) < 40 and abs(c[1] - c2[1]) < 40:
                                corners.remove(c2)
                                
        return corners


#find glyphs
def findGlpyh(image, corners):
        for a in corners:
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
                                                                        if c[0] > d[0]:
                                                                                c2 = c
                                                                                c4 = d
                                                                        else:
                                                                                c2 = d
                                                                                c4 = c
                                                                elif sc == smin:
                                                                        c1 = c
                                                                        if b[0] > d[0]:
                                                                                c2 = b
                                                                                c4 = d
                                                                        else:
                                                                                c2 = d
                                                                                c4 = b
                                                                else:
                                                                        c1 = d
                                                                        if b[0] > c[0]:
                                                                                c2 = b
                                                                                c4 = c
                                                                        else:
                                                                                c2 = c
                                                                                c4 = b                                    
                                                        elif sb == smax:
                                                                        c3 = b
                                                                        if sa == smin:
                                                                                c1 = a
                                                                                if c[0] > d[0]:
                                                                                        c2 = c
                                                                                        c4 = d
                                                                                else:
                                                                                        c2 = d
                                                                                        c4 = c                                        
                                                                        elif sc == smin:
                                                                                c1 = c
                                                                                if a[0] > d[0]:
                                                                                        c2 = a
                                                                                        c4 = d
                                                                                else:
                                                                                        c2 = d
                                                                                        c4 = a                                        
                                                                        else:
                                                                                c1 = d
                                                                                if a[0] > d[0]:
                                                                                        c2 = a
                                                                                        c4 = c
                                                                                else:
                                                                                        c2 = c
                                                                                        c4 = a                                        
                                                        elif sc == smax:
                                                                        c3 = c
                                                                        if sa == smin:
                                                                                c1 = a
                                                                                if b[0] > d[0]:
                                                                                        c2 = b
                                                                                        c4 = d
                                                                                else:
                                                                                        c2 = d
                                                                                        c4 = b
                                                                                
                                                                        elif sb == smin:
                                                                                c1 = b
                                                                                if a[0] > d[0]:
                                                                                        c2 = a
                                                                                        c4 = d
                                                                                else:
                                                                                        c2 = d
                                                                                        c4 = a
                                                                                
                                                                        else:
                                                                                c1 = d
                                                                                if a[0] > b[0]:
                                                                                        c2 = a
                                                                                        c4 = b
                                                                                else:
                                                                                        c2 = b
                                                                                        c4 = a                                        
                                                        else:
                                                                        c3 = d
                                                                        if sa == smin:
                                                                                c1 = a
                                                                                if b[0] > c[0]:
                                                                                        c2 = b
                                                                                        c4 = c
                                                                                else:
                                                                                        c2 = c
                                                                                        c4 = b
                                                                        elif sb == smin:
                                                                                c1 = b
                                                                                if a[0] > c[0]:
                                                                                        c2 = a
                                                                                        c4 = c
                                                                                else:
                                                                                        c2 = c
                                                                                        c4 = a                                        
                                                                        else:
                                                                                c1 = c
                                                                                if a[0] > b[0]:
                                                                                        c2 = a
                                                                                        c4 = b
                                                                                else:
                                                                                        c2 = b
                                                                                        c4 = a                                                       
                                                        
                                                        #diagonals should be roughly equal in length
                                                        diag1 = dist(c1,c3)
                                                        diag2 = dist(c2,c4)
                                                        q = abs(diag1-diag2) < 30
                                                        
                                                        #due to perspective, dy1 and dy2 should be equal in magnitude but opposite in sign
                                                        dx1 = c1[0]-c4[0]
                                                        dx2 = c2[0]-c3[0]
                                                        dy1 = c1[1]-c2[1]
                                                        dy2 = c4[1]-c3[1]                                               
                                                        r = abs(dy1 + dy2) < 50
                                                        
                                                        #both dx's should be minimal (since glyph is assumed at camera height)
                                                        s = abs(dx1) < 30 and abs(dx2) < 30
                                                        
                                                        #top and bottom should be similar in length
                                                        t = abs(dist(c1,c2) - dist(c3,c4)) < 50
                                                        
                                                        if q and r and s and t:
                                                        
                                                                #check for a solid white/black edge
                                                                white = (mean(image,c1[0]-20,c1[1]-20)+mean(image,c1[0]+20,c1[1]-20)+mean(image,c1[0]-20,c1[1]+20)+
                                                                        mean(image,c2[0]+20,c2[1]-20)+mean(image,c2[0]-20,c2[1]-20)+mean(image,c2[0]+20,c2[1]+20)+
                                                                        mean(image,c3[0]+20,c3[1]+20)+mean(image,c3[0]-20,c3[1]+20)+mean(image,c3[0]+20,c3[1]-20)+
                                                                        mean(image,c4[0]-20,c4[1]+20)+mean(image,c4[0]-20,c4[1]-20)+mean(image,c4[0]+20,c4[1]+20))/12
                                                                black = (mean(image,c1[0]+20,c1[1]+20)+mean(image,c2[0]-20,c2[1]+20)+mean(image,c3[0]-20,c3[1]-20)+
                                                                        mean(image,c4[0]+20,c4[1]-20))/4
                                                                
                                                                if white - black > 220:
                                                                        #we have found a glyph!
                                                                        return[c1, c2, c3, c4]


#draws a quadrilateral on an image
def drawQuad(image, quads):
        cv.Line(image, (quads[0][0], quads[0][1]), (quads[1][0], quads[1][1]), cv.CV_RGB(255,120,0),3,4)
        cv.Line(image, (quads[1][0], quads[1][1]), (quads[2][0], quads[2][1]), cv.CV_RGB(255,120,0),3,4)
        cv.Line(image, (quads[2][0], quads[2][1]), (quads[3][0], quads[3][1]), cv.CV_RGB(255,120,0),3,4)
        cv.Line(image, (quads[3][0], quads[3][1]), (quads[0][0], quads[0][1]), cv.CV_RGB(255,120,0),3,4)


#checks each square of a glpyh to see if it is white or black
def readGlyph(image, quads):

        dx = (quads[1][0]-quads[0][0] + quads[2][0]-quads[3][0])/(2.0*6.5)
        dy = (quads[3][1]-quads[0][1] + quads[2][1]-quads[1][1])/(2.0*6.5)

        grid = [[0,0,0,0,0] for x in xrange(5)]

        for row in xrange(0,5):
                for col in xrange(0,5):
                        grid[row][col] = isWhite(image, 1.25*dx+col*dx+quads[0][0], 1.25*dy+row*dy+quads[0][1], 160)
        return grid
         

#prints out a grid
def printGrid(grid):
        for row in xrange(5):
                for col in xrange(5):
                        if grid[row][col] == 1:
                                print '#',
                        else:
                                print '_',
                print ''


#find glyphs in image
def glyphRec(image):

        storage = cv.CreateMemStorage(0);

        contrast = cv.CreateImage(cv.GetSize(image),8,3)
        grey = cv.CreateImage(cv.GetSize(image),8,1)
        canny = cv.CreateImage(cv.GetSize(grey), cv.IPL_DEPTH_8U, 1)
        
        #increase contrast
        avg = cv.Avg(image)
        cv.AddS(image, cv.Scalar(-.5*avg[0],-.5*avg[1],-.5*avg[2]), contrast)
        cv.Scale(contrast, contrast, 3)
        
        #make grayscale
        cv.CvtColor(contrast,grey,cv.CV_BGR2GRAY)
        
        #smooth
        cv.Smooth(grey, grey, cv.CV_GAUSSIAN, 3, 3)
        
        #edge detect
        cv.Canny(grey, canny, 20,200,3)
        
        #smooth again
        cv.Smooth(canny, canny, cv.CV_GAUSSIAN, 3, 3)
        
        #find lines
        lines = cv.HoughLines2(canny, storage, cv.CV_HOUGH_PROBABILISTIC, 3, math.pi/180, 50, 150, 40)
        
        #find corners
        corners = getCorners(lines)
        
        #find quadrilaterals
        quad = findGlpyh(contrast, corners)
        
        if quad == None:
                return None
                
        drawQuad(image, quad)

        grid = readGlyph(image, quad)
        printGrid(grid)
        print ''
        toCoords(grid)
                
        return grid
        

#converts grid to a useful set of coordinates
def toCoords(grid):
        x = (grid[0][0]+grid[0][1]*2+grid[0][2]*4+grid[0][3]*8+grid[0][4]*16+grid[1][0]*32+grid[1][1]*64+grid[1][2]*128+grid[1][3]*256)*(grid[1][4]*-1)
        y = (grid[2][0]+grid[2][1]*2+grid[2][2]*4+grid[2][3]*8+grid[2][4]*16+grid[3][0]*32+grid[3][1]*64+grid[3][2]*128+grid[3][3]*256)*(grid[3][4]*-1)
        sector = grid[4][0]+grid[4][1]*2+grid[4][2]*4
        direction = grid[4][3]+grid[4][4]*2
        print 'X:', x
        print 'Y:', y
        print 'Sector:', sector
        print 'Direction:', direction

                
#loads image from a file and checks for glyphs in it
if __name__ == "__main__":

        if len(sys.argv) != 2:
                print "Please supply a file name"
                sys.exit()

        cv.NamedWindow('Glpyh Recognition', 0)
        
        image = cv.LoadImage("../images/" + sys.argv[1], cv.CV_LOAD_IMAGE_COLOR) #Load the image
        cv.ResizeWindow('source', 600, 800)
        
        grid = glyphRec(image)
        
        cv.ShowImage('Glpyh Recognition', image)
        
        while True:
                cv.WaitKey(1)
