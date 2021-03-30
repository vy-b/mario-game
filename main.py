# My_Mario_Game.py
# Description: A maze for a character "♞" to navigate through and reach an exit gate to win! (Crash free :D)
# Author: AL + Vy Bui
# Date: July 28 2019

# -------------------------------------------------------------------
  
def readDataFileAndSetVariables( filename ):
    # Make the following variables accessible in this function by making them "global"
    global mazeWidth
    global mazeHeight
    global aNumOfTreasures
    global aNumOfBombs
    global emptyCell
    global treasure
    global bomb
    global mario
    global exitGate
    global boundary
    global boundarySide
    global marioLocationList
    global rList
    global eList
    global bombScoreRatio

    # Open file for reading
    dataFileRead = open(filename, "r")

    # Read file content into a list - to be completed - Part 1
    intList = []
    for line in range(4):
     intList.append(int(dataFileRead.readline().strip("\n")))
    mazeWidth, mazeHeight, aNumOfTreasures, aNumOfBombs = intList
    
    strList = []
    for line in range(7):
      strList.append(dataFileRead.readline().strip("\n"))
    emptyCell, treasure, bomb, mario, exitGate, boundary, boundarySide = strList

    marioLocationList.append( list( dataFileRead.readline().replace(" ","").strip("\n")) )
    marioLocationList[0][0] = int(marioLocationList[0][0])
    marioLocationList[0][1] = int(marioLocationList[0][1])

    for i in range(15):
      rList.append( list(dataFileRead.readline().replace(" ","").strip("\n")) )
      rList[i][0] = int(rList[i][0])
      rList[i][1] = int(rList[i][1])

    
    for i in range(30):
      eList.append(list(dataFileRead.readline().replace(" ","").strip("\n")))
      eList[i][0] = int(eList[i][0])
      eList[i][1] = int(eList[i][1])

    bombScoreRatio = int(dataFileRead.readline().strip("\n"))



# For debugging purposes
    print("mazeWidth = ", mazeWidth)
    print("mazeHeight = ", mazeHeight)
    print("aNumOfTreasures = ", aNumOfTreasures)
    print("aNumOfBombs = ", aNumOfBombs)
    print("emptyCell = '{}'".format(emptyCell))
    print("treasure = '{}'".format(treasure))
    print("bomb = '{}'".format(bomb))  
    print("mario = '{}'".format(mario))    
    print("exitGate = '{}'".format(exitGate))
    print("boundary = '{}'".format(boundary))    
    print("boundarySide = '{}'".format(boundarySide))
    print("marioLocationList = ", marioLocationList)
    print("rList = ", rList)
    print("eList = ", eList)
    print("bombScoreRatio = ", bombScoreRatio)

    # Close the file
    dataFileRead.close( )
    return

# -------------------------------------------------------------------

def createMaze(aMaze, aWidth, aHeight, aCell):
    ''' Create and return "aMaze" of "aWidth" by "aHeight".
        Each cell of the maze is a string set to "cell".      
    '''
    aMaze = [ [ (aCell) for i in range(aWidth) ] for j in range(aHeight) ]   
    # printMaze(maze, aHeight)  #for debugging purposes - Print maze as a list of list
    return aMaze

# -------------------------------------------------------------------

# Print Maze - for debugging purposes
def printMaze(aMaze, aHeight):
    ''' Print "aMaze" of "aHeight" - for debug purposes.
    ''' 
    for row in range(aHeight):
        print(aMaze[row])  
    return
		
# -------------------------------------------------------------------

def createBoundary(aWidth, bH):
    ''' Create and return a list that contains 2 lists: the top boundary of the maze
        and the bottom boundary of the maze. Each element of these 2 lists is a string set to "bH".
    '''
    return list([[(bH) for number in range(aWidth)],[(bH) for number in range(aWidth)]])                

# -------------------------------------------------------------------

def displayMaze(aMaze, aWidth, aHeight, hBoundary, bS ):
    ''' Display 'aMaze' with column numbers at the top and row numbers to the left of each row
        along with the top and the bottom boundaries "hBoundary" that surround the maze.

        Other parameters:
         "aWidth" is the width of the maze.
         "aHeight" is the height of the maze.
         "bS" is the symbol used for the vertical border.

        No returned value
    '''
    topIndex = 0  # Index of proper boundary in hBoundary
    bottomIndex = 1
    offset = 3
    aString = (offset+1) * " "

    print()  
    # Display a row of numbers from 1 to aWidth
    for column in range(aWidth):
        aString = aString + str(column+1) + ""
        if len(str(column+1)) == 1 :
            aString += " "           
    print(aString)

    # Display the top boundary of maze
    print(offset * " " + "".join(hBoundary[topIndex]))
    
    # Display a column of numbers from 1 to aHeight + left and right boundaries of the maze
    for row in range(aHeight):
        pre = str(row+1) + " " + bS
        if row >= 9: # i.e., displayed row number is >= 10 - adjusting for extra digit
           pre = str(row+1) + bS
        post = bS
        aRow = pre + ''.join(aMaze[row]) + post
        print(aRow)

    # Display the bottom boundary of maze
    print(offset * " " + "".join(hBoundary[bottomIndex]))
    return

# -------------------------------------------------------------------

def placeInMaze(aMaze, aRow, aColumn, aContent):
    ''' Place something represented by "aContent" at the location ["aRow", "aColumn"] into "aMaze"

        Returned value:
         "aMaze" updated.
    '''
    aMaze[aRow][aColumn] = aContent
    return aMaze

# -------------------------------------------------------------------

def placeExitGate(aWidth, aHeight, rowMario, columnMario, hBoundary, exitGate):
    ''' Place the exit gate, represented by "exitGate", at the opposite corner of Mario's location.
		This means:
		Place the exit gate either in the top boundary or the bottom boundary 
		which ever is at the opposite corner of Mario's location, represented by [rowMario, columnMario].

        Other parameters:
         "aWidth" is the width of the maze.
         "aHeight" is the height of the maze.

        Returned value:
         "hBoundary" updated.
         "hBoundary" is a list of 2 lists: the first list is the top boundary and the second list is the bottom boundary.
         "exitGateLocationList" updated.
    '''
    topIndex = 0 # Index of proper boundary in hBoundary
    bottomIndex = 1
    exitGateRight = False
    exitGateBottom = False
    row = 0
    column = 1
    exitGateLocationList.insert(row, 0)   # Assume exit gate at the top left
    exitGateLocationList.insert(column, 0)
        
    # Where is Mario?
    # If Mario is top left then exit gate is bottom right
    if columnMario <= ((aWidth) // 2) : # Mario on the left?
        exitGateLocationList[column] = aWidth - 1  # Yes, then exit gate on the right
        exitGateRight = True
    # No, then assuption holds -> exit gate on the left
    if rowMario <= ((aHeight) // 2) :   # Mario at the top?
        exitGateLocationList[row] = aHeight - 1    # Yes, then exit gate at the bottom
        exitGateBottom = True
        # No, then assuption holds -> exit gate at the top

    # Place exit gate in appropriate top/bottom boundary
    if exitGateBottom :
        del hBoundary[bottomIndex][exitGateLocationList[column]]
        hBoundary[bottomIndex].insert(exitGateLocationList[column], exitGate)
    else:
        del hBoundary[topIndex][exitGateLocationList[column]]
        hBoundary[topIndex].insert(exitGateLocationList[column], exitGate)       

    
    return hBoundary, exitGateLocationList  # Can return a tuple -> elements sepatared by a coma

# -------------------------------------------------------------------

def setMarioScore(numOfBombs, divideBy):
    ''' Set and return Mario's score to be numOfBombs // divideBy
    '''    
    return numOfBombs // divideBy


# -------------------------------------------------------------------


# Main part of the program

# Welcome the user and identify the game
print("""Welcome.\n""")

# Ask user for filename
filename = "data.txt";

# Initialize the game variables ...
mazeWidth = 0
mazeHeight = 0
aNumOfTreasures = 0
aNumOfBombs = 0
emptyCell = ""
treasure = "" 
bomb = ""
mario = ""  
exitGate = ""  
boundary = ""  
boundarySide = ""
marioLocationList = list()
rList = list()
eList = list()
bombScoreRatio = 0

# ... and assign them values coming form the input data file (filename)
readDataFileAndSetVariables(filename)

# Create a maze
theMaze = list()
theMaze = createMaze(theMaze, mazeWidth, mazeHeight, emptyCell)

# Create the boundary around the maze (not part of the maze)
hBoundary = list()
hBoundary = createBoundary(mazeWidth, boundary)

# Place treasures in the maze
rowIndex = 0
columnIndex = 1  
for obstacle in range(aNumOfTreasures):
    theMaze = placeInMaze(theMaze, int(rList[obstacle][rowIndex]), int(rList[obstacle][columnIndex]), treasure)

# Place bombs in the maze
for obstacle in range(aNumOfBombs):
    theMaze = placeInMaze(theMaze, int(eList[obstacle][rowIndex]), int(eList[obstacle][columnIndex]), bomb)

# Place Mario in the maze
theMaze = placeInMaze(theMaze, int(marioLocationList[0][0]), int(marioLocationList[0][1]), mario)
          
# Create exit gate and place it in the maze
# Place the exit gate at the opposite corner of Mario's location
exitGateLocationList = list()
hBoundary, exitGateLocationList = placeExitGate(mazeWidth, mazeHeight, int(marioLocationList[0][0]), int(marioLocationList[0][1]), hBoundary, exitGate)

# Set Mario's score
marioScore = setMarioScore(aNumOfBombs, bombScoreRatio)




# Part 2 - To be completed
# Here is the 'high-level' algorithm:

playing = True
marioCurrentRow = int(marioLocationList[0][0])
marioCurrentColumn = int(marioLocationList[0][1])



# As long as the player is playing ...
while playing:

	# Display the maze
	# Once you have completed Part 1, uncomment the following Python statement and see what is displayed on the screen!

  displayMaze(theMaze, mazeWidth, mazeHeight, hBoundary, boundarySide)
	
	# Display Mario's score (see Sample Runs)
  print("score -> {}".format(marioScore))

	# Display instructions to the player (see Sample Runs)
  playerInput = input("Move your character using w,a,s,d and x to exit\n")



	# Update the game if the player is moving Mario one cell to the right, to the left, up or down 

  # If player wants to move to the right
  if playerInput.lower() == "d":
    # Prevent crash by displaying error message if player tries to move out of maze range
    if marioCurrentColumn == 9:
      print("Cannot move out of maze! Move somewhere else.")
    else:
      # Move Mario to the right by one
      placeInMaze(theMaze, marioCurrentRow, marioCurrentColumn+1, mario)
      # Replace Mario's previous location with empty cell
      placeInMaze(theMaze, marioCurrentRow, marioCurrentColumn, emptyCell)
      # Change stored value of Mario's current location
      marioCurrentColumn += 1

  # If player wants to move to the left
  if playerInput.lower() == "a":
    # Prevent crash by displaying error message if player tries to move out of maze range
    if marioCurrentColumn == 0:
      print("Cannot move out of maze! Move somewhere else.")
    else:
      # Move Mario to the left by one
      placeInMaze(theMaze, marioCurrentRow, marioCurrentColumn-1, mario)
      # Replace Mario's previous location with empty cell
      placeInMaze(theMaze, marioCurrentRow, marioCurrentColumn, emptyCell)
      marioCurrentColumn -= 1
    
  # If player wants to move up
  if playerInput.lower() == "w":
    # Exit gate scenario if exit gate was top left
    # If Mario reaches the exit gate coordinate
    if [marioCurrentRow,marioCurrentColumn] == [exitGateLocationList[0],exitGateLocationList[1]] and (exitGateLocationList == [0,0] or [0,9]):
      print("Mario has reached the exit gate with a score of {}! You win!".format(marioScore))
      # Exit game
      playing = False
    # If Mario has not reached the exit gate coordinate, continue game
    elif marioCurrentRow == 0:
      print("Cannot move out of maze! Move somewhere else.")
    else:
      # Move Mario up by one
      placeInMaze(theMaze, marioCurrentRow-1, marioCurrentColumn, mario)
      # Replace Mario's previous location with empty cell
      placeInMaze(theMaze, marioCurrentRow, marioCurrentColumn, emptyCell)
      marioCurrentRow -= 1
    
  # If player wants to move down
  if playerInput.lower() == "s":
    # Exit gate scenario if exit gate was bottom right
    # If Mario reaches the exit gate coordinate
    if [marioCurrentRow,marioCurrentColumn] == [exitGateLocationList[0],exitGateLocationList[1]] and (exitGateLocationList == [9,9] or [0,9]):
      print("Mario has reached the exit gate with a score of {}! You win!".format(marioScore))
      # Exit game
      playing = False
    # If Mario has not reached the exit gate coordinate, continue game
    elif marioCurrentRow == 9:
      print("Cannot move out of maze! Move somewhere else.")
    else:
      # Move Mario down by one
      placeInMaze(theMaze, marioCurrentRow+1, marioCurrentColumn, mario)
      # Replace Mario's previous location with empty cell
      placeInMaze(theMaze, marioCurrentRow, marioCurrentColumn, emptyCell)
      marioCurrentRow += 1

  if playerInput.lower() not in ['w','a','s','d']:
    # If player input is not 'w','a','s','d'
    print("Invalid input!")




  # Move on to scoring system
  # If Mario moves into a bomb location, deduct 1 point
  if [marioCurrentRow,marioCurrentColumn] in eList:
    marioScore -= 1
    # Remove bomb (remove location from bomb list) to prevent further point deduction if player moves back into the same spot
    eList.remove([marioCurrentRow,marioCurrentColumn])

    # If Mario moves into a treasure location, add 1 point
  if [marioCurrentRow,marioCurrentColumn] in rList:
    marioScore += 1
    # Remove treasure (remove location from treasure list) to prevent further point addition if player moves back into the same spot
    rList.remove([marioCurrentRow,marioCurrentColumn])

  # If score reaches 0, player loses
  if marioScore == 0:
    print("Mario's score is now down to 0! You have lost!")
    playing = False

	# Stop the game if the player has entered 'x'.
  if playerInput.lower() == "x":
    playing = False
	# (Hint: There is a lot going on in this step, i.e., lotÃ¢â‚¬â„¢s of details to discover).

print("\n-------")
