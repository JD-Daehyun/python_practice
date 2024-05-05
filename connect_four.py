import random

print("Welcome to Connect Four!")
print('------------------------')

possibleLetters = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
gameBoard = [['' for _ in range(7)] for _ in range(6)]
rows = 6
cols = 7

def printGameBoard():
    print("\n     A    B    C    D    E    F    G")
    for x in range(rows):
      print("\n   +----+----+----+----+----+----+----+")
      print(x," |", end = "")
      for y in range(cols):
        if gameBoard[x][y] == "🔵":
          print("", gameBoard[x][y], end=" |")
        elif gameBoard[x][y] == "🔴":
          print("", gameBoard[x][y], end=" |")
        else: 
          print(" ", gameBoard[x][y], end="  |")
    print("\n   +----+----+----+----+----+----+----+")

def dropChip(column, chip):
    for row in range(rows - 1, -1, -1):  # Start from the bottom row and move up
        if gameBoard[row][column] == '':
            gameBoard[row][column] = chip
            return True  # Chip successfully dropped
    return False  # Column is full

def columnParser(inputLetter):
    if inputLetter.upper() in possibleLetters:
        return possibleLetters.index(inputLetter.upper())
    else:
        print("Invalid Column!!")
        return None
def checkForWinner(chip):
  ### Check horizontal spaces
  for row in range(rows):
    for col in range(cols - 3):
      if gameBoard[row][col] == chip and gameBoard[row][col+1] == chip and gameBoard[row][col+2] == chip and gameBoard[row][col+3] == chip:
        print("\nGame over", chip, " wins! Thank you for playing :)")
        return True

  ### Check vertical spaces
  for col in range(cols):
    for row in range(rows - 3):
      if gameBoard[row][col] == chip and gameBoard[row+1][col] == chip and gameBoard[row+2][col] == chip and gameBoard[row+3][col] == chip:
        print("\nGame over", chip, " wins! Thank you for playing :)")
        return True

  ### Check upper right to bottom left diagonal spaces
  for row in range(rows - 3):
    for col in range(3, cols):
      if gameBoard[row][col] == chip and gameBoard[row+1][col-1] == chip and gameBoard[row+2][col-2] == chip and gameBoard[row+3][col-3] == chip:
        print("\nGame over", chip, " wins! Thank you for playing :)")
        return True

  ### Check upper left to bottom right diagonal spaces
  for row in range(rows - 3):
    for col in range(cols - 3):
      if gameBoard[row][col] == chip and gameBoard[row+1][col+1] == chip and gameBoard[row+2][col+2] == chip and gameBoard[row+3][col+3] == chip:
        print("\nGame over", chip, " wins! Thank you for playing :)")
        return True
  return False

def isTie():
  for row in gameBoard:
    if '' in row:  # Checks if there is an empty space in the row
      return False  # Game is not tied as there are moves left
  return True  # No empty spaces left, game is a tie

##############Advanced Heuristic Function ###############
def findBestMove(chip):
    # Priority 1: Check for a winning move
    for col in range(cols):
        if canPlayColumn(col) and isWinningMove(col, chip):
            return col

    # Priority 2: Block opponent's winning move
    opponent_chip = '🔵' if chip == '🔴' else '🔴'
    for col in range(cols):
        if canPlayColumn(col) and isWinningMove(col, opponent_chip):
            return col

    # Priority 3: Prefer center columns
    center_preferences = [3, 2, 4, 1, 5, 0, 6]
    for col in center_preferences:
        if canPlayColumn(col):
            return col

    # Fallback: Random move (should not be reached if center preferences cover all columns)
    return random.randint(0, cols - 1)

def canPlayColumn(column):
    # Check if the top row for the column is empty (indicating the column is not full)
    return gameBoard[0][column] == ''

def isWinningMove(column, chip):
    # Temporarily place the chip in the column to check for a win
    for row in range(rows - 1, -1, -1):
        if gameBoard[row][column] == '':
            gameBoard[row][column] = chip
            if checkForWinner(chip):
                gameBoard[row][column] = ''  # Undo the move
                return True
            gameBoard[row][column] = ''  # Undo the move
            break
    return False

def play_game():
    turnCounter = 0
    winner = False
    while not winner and not isTie():
        printGameBoard()
        currentChip = '🔵' if turnCounter % 2 == 0 else '🔴'  # Determine current chip based on turn

        if turnCounter % 2 == 0:  # Player's turn
            while True:
                userColumn = input("\nChoose a column (A-G): ")
                columnIndex = columnParser(userColumn)
                if columnIndex is not None and dropChip(columnIndex, currentChip):
                    break
                else:
                    print("Try again or choose a different column.")
        else:  # Computer's turn
            computerColumn = findBestMove('🔴')  # Assuming the computer uses red chips
            dropChip(computerColumn, '🔴')
            print(f"Computer chooses column: {possibleLetters[computerColumn]}")

        winner = checkForWinner(currentChip)
        if winner:
            printGameBoard()
            print(f"\nGame over. {'Player' if turnCounter % 2 == 0 else 'Computer'} wins! Thank you for playing :)")
            return  # Exit after announcing the winner

        turnCounter += 1  # Increment turn counter after checking for winner

    if isTie():
        printGameBoard()
        print("\nThe game is a tie. Thank you for playing :)")
        
play_game()