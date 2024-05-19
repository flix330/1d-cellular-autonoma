# fohalloran24 5.16.24
# initial creation 5.1.24

"""
Felix O'Halloran's 1D Cellular Automata

This is a program which allows the user to explore a wide range of visuals produced by a one
dimentional cellular automata based off the principles of Wolframs studies. When the program
is started, the user is promted to pick a 'graph size' and 'number'. The graph size determines
how many initial cells can be placed, as well as how many generations can be displayed when
the program runs. The rule set determines which set of rules will apply to each cell when it
evolves between generations. (Will be explained later)

Once the user is satisfied with their inital conditions, they can press launch which will
bring them into the main UI. Looking at the graph, the user can select with their mouse which
cells they desire to turn on in the first generation. Once they have turned on the cells they
wish to they can push Next Gen, which starts the automation process.

This cellular autonoma program works using a three cell neighborhood principle. In each 
generation, every cell is indiviually looked at with the cell directly to its left and right.
These three cells each get a 1 (if they are on) or 0 (if they are off). There states combined
give us a binary number from 0 to 7. We then turn this value into an integer from 0 to 7 which
I refer to as the neighborhood value.

Now lets dive into the 255 differnt rules. Once the user selects a rule, that number is turned
into an 8 digit binary number. We then compare our neighborhood value to this 8 digit converted
rule value. The neighboorhood value acts as the index of the rule value which we will compare
our number to. If the value is true, we turn on that cell, and if it is false, we turn that
cell off. This process is then continued until the maxium graph size is reached
"""
#imports
import sys
sys.path.append("../util")
from DEgraphics import *

# dictionarys for grid and circles
grid = {}
circles = {}

# creates the grid based on the size determined by user
def newGrid(size, win):
    step = 20 / size
    current = -10
    for n in range(size + 1):
        lineA = Line(Point(current, -10),Point(current, 10))
        lineB = Line(Point(-10, current),Point(10, current))
        lineA.draw(win)
        lineB.draw(win)
        current += step
    for i in range(size):
        for j in range(size):
            grid[(i, j)] = Rectangle(Point(i * step - 10, j * step - 10),Point((i + 1) * step - 10, (j + 1) * step - 10))
            grid[(i, j)].setOutline('#58748a')
            grid[(i, j)].draw(win)
            circles[(i, j)] = None

# creates a black box and cell where the user clicks
def newBox(point, win, size, currentGen):
    # converting screen coords into grid coords
    grid_x, grid_y = win.toWorld(point.x, point.y)
    step = 20 / size
    x, y = int((grid_x + 10) // step),int((grid_y + 10) // step)
    
    # make sure x and y are in bounds
    if 0 <= x < size and 0 <= y < size:
        if circles[(x, y)] is None:
            circ = Circle(Point((x + 0.5) * step - 10,(y + 0.5) * step - 10),step * 0.45)
            circ.setFill('#58748a')
            circ.draw(win)
            circles[(x, y)] = circ
            currentGen[x] = 1
        else:
            circles[(x, y)].undraw()
            circles[(x, y)] = None
            currentGen[x] = 0

# converts the rule to its binary number
def ruleToBinary(ruleNum):
    binaryStr = f"{ruleNum:08b}"
    binaryList = [int(bit) for bit in binaryStr]
    binaryList.reverse()
    return binaryList

# applies the rule to every cells neighborhood
def applyRule(currentGen,rules,size,nextGen):
    for i in range(1,size - 1):
        left = currentGen[i - 1]
        center = currentGen[i]
        right = currentGen[i + 1]
        neighborhoodList = [left, center, right]
        if neighborhoodList == [0,0,0]:
            index = 0
        elif neighborhoodList == [0,0,1]:
            index = 1
        elif neighborhoodList == [0,1,0]:
            index = 2
        elif neighborhoodList == [0,1,1]:
            index = 3
        elif neighborhoodList == [1,0,0]:
            index = 4
        elif neighborhoodList == [1,0,1]:
            index = 5
        elif neighborhoodList == [1,1,0]:
            index = 6
        elif neighborhoodList == [1,1,1]:
            index = 7
        nextGen[i] = rules[index]
    return nextGen

# run the simulation on the current generation, and output the resulting next generation
def runSim(ruleNum,currentGen,size,nextGen):
    rules = ruleToBinary(ruleNum)
    nextGen = applyRule(currentGen,rules,size,nextGen)
    return nextGen

# update the next row (generation) of the graph with black dots denoting cells
def updateGrid(win, rowNum, nextGen, size):
    step = 20 / size
    y = 10 - (step * (rowNum + 1)) - (step / 2)
    for i in range(size):
        if nextGen[i] == 1:
            x = (step * i) + (step / 2) - 10
            dot = Circle(Point(x, y),step * 0.45)
            dot.setFill('#58748a')
            dot.draw(win)
    return nextGen[:]

def oneDCA(size,ruleNum):
    # arrays for the generation
    # current generation
    currentGen = [0] * size
    nextGen = [0] * size

    #####################-Windows-############################  
    # list of windows for easy closing
    winList = []

    # using another window as the border so border doesnt cut off edges of graph
    winBorder = DEGraphWin(width=708,height=708,hasTitlebar=False,defCoords=[-10,-10,10,10],
                      offsets=[396,46],hBGColor=("#58748a"),hThickness=4,axisType=1)
    winList.append(winBorder)

    # autonoma window
    winFirstGen = DEGraphWin(width=700,height=700,hasTitlebar=False,defCoords=[-10,-10,10,10],
                      offsets=[400,50],hBGColor=("#58748a"),hThickness=0,axisType=0,axisColor=('#58748a'))
    winList.append(winFirstGen)

    # control panel window
    winCP = DEGraphWin(title="CP",width=150, height=75, hasTitlebar=True,defCoords=[-1,-1,1,1],
                       offsets=[246,50],hBGColor=("#58748a"),hThickness=4)
    winList.append(winCP)

    #####################-Buttons-############################ 
    # list of buttons
    btnList = []
    
    # button to close
    btnExit = Button(winCP, topLeft=Point(-0.9,0.85), width=1.8, height=0.8,
                     edgeWidth=1, label='x',
                     buttonColors=['#58748a', '#58748a', '#fffbf7'],
                     clickedColors=['#58748a', '#58748a', '#58748a'],
                     font=('courier', 22), timeDelay=0.25)
    btnExit.activate()
    btnList.append(btnExit)

    # button to advance
    btnNxtGen = Button(winCP, topLeft=Point(-0.9,-0.05), width=1.8, height=0.8,
                       edgeWidth=1, label='Next Gen',
                       buttonColors=['#58748a', '#58748a', '#fffbf7'],
                       clickedColors=['#58748a', '#58748a', '#58748a'],
                       font=('courier', 22), timeDelay=0.25)
    btnNxtGen.activate()
    btnList.append(btnNxtGen)

    # initializing the grid and generation arrays
    newGrid(size,winFirstGen)
    currentGen = [0] * size
    nextGen = [0] * size
    winFirstGen.setMouseHandler(lambda point: newBox(point, winFirstGen,size,currentGen))

    #####################-ButtonActions-############################
    # creating the click point
    clickPoint = Point(-1, 1)
    # button actions
    while not btnExit.clicked(clickPoint):
        clickPoint = winCP.getMouse()
        # create the next generation
        if btnNxtGen.clicked(clickPoint):
            gen = 0
            while gen < size:
                nextGen = runSim(ruleNum,currentGen,size,nextGen)
                currentGen = updateGrid(winFirstGen,gen,nextGen,size)
                gen += 1
    # closing all the windows
    for w in winList:
        w.close()

# run main method
if __name__ == "__main__":
        #####################-windows-############################ 
        # splash screen
        winSplash = DEGraphWin(width = 400, height = 400, hasTitlebar=False, defCoords=[-2,-2,2,2],
                      offsets=[500,200],hBGColor=("#58748a"),hThickness=6)
        winSplash.setBackground("#fffbf7")

        #####################-Text-############################
        # top text
        introText = Text(Point(0,1), "Felix's Cellular Automata")
        introText.setTextColor('#58748a')
        introText.setSize(25)
        introText.setFace('courier')
        introText.draw(winSplash)
    
        #####################-Sliders-############################
        # slider for number of iterations
        sizeSlider = Slider(Point(0.7,-0.3), length=150,height=20,min=3,max=200,label="Graph Size",orient="H")
        sizeSlider.setTextColor('#58748a')
        sizeSlider.draw(winSplash)

        # slider for number of julia set iterations
        ruleSlider = Slider(Point(0.7,-1.1), length=150,height=20,min=0,max=255,label="Rule Select",orient="H")
        ruleSlider.setTextColor('#58748a')
        ruleSlider.draw(winSplash) 
        
        #####################-Buttons-############################        
        # button to exit
        btnExitSplash = Button(winSplash, topLeft = Point(-1.3,-0.8), width = 1, height = 0.8,
                 edgeWidth = 5, label = 'x',
                 buttonColors = ['#58748a', '#58748a', '#fffbf7'],
                 clickedColors = ['#58748a', '#58748a', '#58748a'],
                 font=('courier',22), timeDelay = 0.25)
        btnExitSplash.activate()
        
        # button to launch graph
        btnLaunch = Button(winSplash, topLeft = Point(-1.3,0.2), width = 1, height = 0.4,
                 edgeWidth = 5, label = 'Launch',
                 buttonColors = ['#58748a', '#58748a', '#fffbf7'],
                 clickedColors = ['#58748a', '#58748a', '#58748a'],
                 font=('courier',22), timeDelay = 0.25)
        btnLaunch.activate()

        # button to open info panel
        btnOpenInfo = Button(winSplash, topLeft = Point(-1.3,-0.3), width = 1, height = 0.4,
                 edgeWidth = 5, label = 'Info',
                 buttonColors = ['#58748a', '#58748a', '#fffbf7'],
                 clickedColors = ['#58748a', '#58748a', '#58748a'],
                 font=('courier',22), timeDelay = 0.25)
        btnOpenInfo.activate()

        #####################-ButtonActions-############################
        # creating the click point
        clickPointSplash = Point(-1,1)

        while not btnExitSplash.clicked(clickPointSplash):
            # launch the program
            if btnLaunch.clicked(clickPointSplash):
                size = sizeSlider.getValue()
                ruleNum = ruleSlider.getValue()
                oneDCA(size,ruleNum)
            # info panel
            if btnOpenInfo.clicked(clickPointSplash):
                #####################-windows-############################
                winInfo = DEGraphWin(width = 400, height = 600, hasTitlebar=False, defCoords=[0,0,4,6],
                      offsets=[500,100],hBGColor=("#58748a"),hThickness=6)
                winInfo.setBackground("#fffbf7")

                #####################-buttons-############################
                # button to exit
                btnExitInfo = Button(winInfo, topLeft = Point(0.1,0.6), width = 3.8, height = 0.5,
                        edgeWidth = 5, label = 'x',
                        buttonColors = ['#58748a', '#58748a', '#fffbf7'],
                        clickedColors = ['#58748a', '#58748a', '#58748a'],
                        font=('courier',22), timeDelay = 0.25)
                btnExitInfo.activate()

                # top text
                infoText = Text(Point(2,5.7), "Celular Automata")
                infoText.setTextColor('#58748a')
                infoText.setSize(25)
                infoText.setFace('courier')
                infoText.draw(winInfo)

                # main text
                mainText = Text(Point(2,4.3), "This is a program which allows the\n user to explore a wide range of\n visuals produced by a one dimentional\n cellular automata based off the\n principles of Wolframs studies. When\n the program is started, the user is\n promted to pick a 'graph size' and\n 'number'. The graph size determines\n how many initial cells can be placed,\n as well as how many generations can\n be displayed when the program runs.\n The rule set determines which set\n of rules will apply to each cell\n when it evolves between generations.")
                mainText.setTextColor('#58748a')
                mainText.setSize(16)
                mainText.setFace('courier')
                mainText.draw(winInfo)                

                #####################-buttonActions-############################
                # button actions for cp window
                clickPointInfo = Point(-1,1)
                while not btnExitInfo.clicked(clickPointInfo):
                    clickPointInfo = winInfo.getMouse()
                winInfo.close()
            clickPointSplash = winSplash.getMouse()
        winSplash.close()

# the end...