"""
File Description: this file contains two functions for drawing any basic scatterplot graph.
"""





#draws the x and y axis of a graph, as well as create the title and enumerations on the axes with number labeling
#x1, y1, x2, y2 is the location for the graph (x1, y1 is top left; x2, y2, is bottom right)
#startX, startY are the starting values for the graph
#maxX, maxY are the bigget values for the graph axes
#xIntervals, yIntervals are the enumerations between each dash on the axes for x and y axes
#title is the title of the graph(duh)
def drawBaseGraph(canvas, x1, y1, x2, y2, startX, startY, maxX, maxY, xIntervals, yIntervals, title):
    canvas.create_text((x1+x2)//2, y1, text = title, font = "Arial 25 bold", anchor = "s")
    canvas.create_text(x1, y2 + 5, text = startX, anchor = "n")
    canvas.create_text(x1 - 5, y2, text = startY, anchor = "e")
    canvas.create_line(x1, y1, x1, y2)
    canvas.create_line(x1, y2, x2, y2)
    numXIntervals = int((maxX-startX)//xIntervals + 1)
    lenXIntervals = int((x2-x1)//numXIntervals)
    for i in range(1, numXIntervals + 1):
        canvas.create_line(x1 + i*lenXIntervals, y2 - 5, x1 + i*lenXIntervals, y2 + 5)
        canvas.create_text(x1 + i*lenXIntervals, y2 + 5, text = startX + i*xIntervals, anchor = "n")
    numYIntervals = int((maxY-startY)//yIntervals + 1)
    lenYIntervals = int((y2-y1)//numYIntervals)
    for i in range(1, numYIntervals + 1):
        canvas.create_line(x1 - 5, y2 - i*lenYIntervals, x1 + 5, y2 - i*lenYIntervals)
        canvas.create_text(x1 - 5, y2 - i*lenYIntervals, text = startX + i*yIntervals, anchor = "e")


#draws points on the given graph values
#points: list of (x, y, bool) tuples to graph
#bool value determines whether or not the point is green(True) or red(False)
#all other values are exactly the same as the drawBaseGraph function
def drawPoints(canvas, x1, y1, x2, y2, startX, startY, maxX, maxY, xIntervals, yIntervals, points):
    numXIntervals = int((maxX-startX)//xIntervals + 1)
    lenXIntervals = int((x2-x1)//numXIntervals)
    numYIntervals = int((maxY-startY)//yIntervals + 1)
    lenYIntervals = int((y2-y1)//numYIntervals)
    for x, y, value in points:
        cx = x1 + int(((x-startX)/xIntervals)*lenXIntervals)
        cy = y2 - int(((y-startY)/yIntervals)*lenYIntervals)
        if(value == True):
            color = "green"
        else:
            color = "red"
        canvas.create_oval(cx-5, cy-5, cx+5, cy+5, fill = color)