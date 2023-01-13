"""
Tic Tac Toe Player
"""

import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    # Counts the amount of X's and O's on the board
    xCount = 0
    oCount = 0

    # Iterates over the board
    for row in board:
        for col in row:
            # Increments the X counter if the item in the slot is a X
            if col == X:
                xCount += 1
            # Increments the O counter if the item in the slot is a O
            elif col == O:
                oCount += 1

    # Checks if the amount of X's and O's are equal
    # If it is, then itll return X, otherwise itll return O
    if xCount == oCount:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Initializes the actions array
    actions = []

    # Loops over the board, and checks if the slot is empty
    # If it is empty, it'll append the coordinates to the actions list
    for rowCount, row in enumerate(board):
        for colCount, col in enumerate(row):
            if col == EMPTY:
                actions.append((rowCount, colCount))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    if type(action) != tuple:
        raise TypeError("Action must be a tuple (i, j)")

    # Initializes the action to be in the format, in which the board dictionary can be accessed
    actionRow = action[0]
    actionCol = action[1]

    # Creates a copy of the board
    boardCopy = copy.deepcopy(board)

    # Sets the action to the player who has the right to play
    boardCopy[actionRow][actionCol] = player(board)

    return boardCopy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Intializes the 3 lists of streaks
    verticalAlign = ["", "", ""]
    horizontalAlign = ["", "", ""]
    diagonalAlign = ["", ""]

    # Loops over the board and assigns the values at the possible streak locations to a list of strings
    for rowCount, row in enumerate(board):
        for colCount, col in enumerate(row):
            verticalAlign[colCount] = f"{verticalAlign[colCount]}{col}"
            horizontalAlign[rowCount] = f"{horizontalAlign[rowCount]}{col}"

    # Creates the diagonal streak strings
    diagonalAlign[0] = f"{board[0][0]}{board[1][1]}{board[2][2]}"
    diagonalAlign[1] = f"{board[0][2]}{board[1][1]}{board[2][0]}"

    # Checks if there has been any horizontal streaks for both X and O
    for streak in horizontalAlign:
        if streak == "XXX":
            return X
        elif streak == "OOO":
            return O

    # Checks if there has been any vertical streaks for both X and O
    for streak in verticalAlign:
        if streak == "XXX":
            return X
        elif streak == "OOO":
            return O

    # Checks if there has been any diagonal streaks for both X and O
    for streak in diagonalAlign:
        if streak == "XXX":
            return X
        elif streak == "OOO":
            return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # Checks if theres any winners
    winnerInt = winner(board)

    # If its not none, it means that it has returned a winner already, so the game has ended
    if winnerInt is not None:
        return True

    # Initializes the variable
    slotsFree = False

    # Iterates over the entries on the board, and checks which are empty
    for row in board:
        for col in row:
            # PERFORMANCE CHECK,
            # if an empty slot is already found,
            # then it means that the game can't have ended already
            if slotsFree:
                break
            # Checks if the slot is empty
            if col == EMPTY:
                slotsFree = True
        # PERFORMANCE CHECK,
        # if an empty slot is already found,
        # then it means that the game can't have ended already
        if slotsFree:
            break

    # There arent any slots left, so the game is over
    if not slotsFree:
        return True

    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # Gets the winnerChar
    winnerChar = winner(board)

    # Remaps the chars to the right letter
    if winnerChar == X:
        return 1
    elif winnerChar == O:
        return -1

    return 0


class Node():
    def __init__(self, action: tuple, eval: int):
        self.action = action
        self.eval = eval


def minimax(board,
            alphaNode=Node(action="alpha", eval=-10000),
            betaNode=Node(action="beta", eval=10000),
            depth=0):
    """ 
    Returns the most optimal action for the given board.\n
    Returns coordinates (i, j)
    """

    # Handling of returning the action responding to the optimal eval
    if depth == 0:
        optimalNode = minimax(board, alphaNode, betaNode, depth + 1)
        return optimalNode.action

    # Checks if the action has a terminal consequence
    if terminal(board):
        return Node(action=None, eval=utility(board))

    # Checks if the maximizing player is at turn
    if player(board) == X:
        # Initializes the maxEval variable
        maxEvalNode = Node(action=None, eval=-10000)

        # Loops over all of the possible actions
        for action in actions(board):
            # Initializes a Node with the action and corresponding eval
            evalNode = Node(action=action,
                            eval=minimax(result(board, action),
                                         alphaNode,
                                         betaNode,
                                         depth + 1).eval)

            # Checks if the new action corresponds to a higher eval score
            if maxEvalNode.eval < evalNode.eval:
                maxEvalNode = evalNode
            # Checks if the alpha node is less than the new action
            if alphaNode.eval < evalNode.eval:
                alphaNode = evalNode
            # Compares the alpha and beta nodes for alpha beta pruning
            if betaNode.eval <= alphaNode.eval:
                break
        return maxEvalNode
    else:
        # Initializes the maxEval variable
        minEvalNode = Node(action=None, eval=10000)

        # Loops over all of the possible actions
        for action in actions(board):
            # Initializes a Node with the action and corresponding eval
            evalNode = Node(action=action,
                            eval=minimax(result(board, action),
                                         alphaNode,
                                         betaNode,
                                         depth + 1).eval)

            # Checks if the new action corresponds to a lower eval score
            if minEvalNode.eval > evalNode.eval:
                minEvalNode = evalNode
            # Checks if the beta node is more than the new action
            if betaNode.eval > evalNode.eval:
                betaNode = evalNode

            # Compares the alpha and beta nodes for alpha beta pruning
            if betaNode.eval <= alphaNode.eval:
                break
        return minEvalNode
