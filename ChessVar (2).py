# Author: Rajveer Singh
# GitHub username: rajsingh09021999
# Date: December 10, 2023
# Description: This file contains several classes and subclass that together represent chess game
# following several standard chess rules that determine a winner when one player captures all of
# opponent's pieces of one type. This program is mainly held by three classes and subclasses,
# a main class called ChessVar that manages the game, controls the flow of movement
# by bringing all other classes together and abstracting sequences, a Board class that
# creates the board and handles its framework, and Piece classes and its subclasses that represent
# different chess pieces with their unique rules about movement on the board and capturing with
# respect to other pieces around them.

class ChessVar:
    """
    Represents a variation of chess game involving setting up a standard chessboard
    and different parameters.
    """

    def __init__(self):
        """
        Initializes the ChessVar game with a board and private attributes that are
        set to default game setting (white is first turn, and game is not finished yet)
        """
        self.__board = Board()
        self.__current_turn = 'white'
        self.__game_state = 'UNFINISHED'

    def get_board(self):
        """
        A getter method that returns the chess board
        """
        return self.__board

    def get_current_turn(self):
        """
        A getter method that returns which player has the turn currently (white or black),
        """
        return self.__current_turn

    def set_current_turn(self, turn):
        """
        A setter method used to manually change a player's turn
        since current turn attribute is private,
        and can't be accessed directly outside of this class.
        """
        self.__current_turn = turn

    def get_game_state(self):
        """
        Returns the current game state which is either 'UNFINISHED', 'WHITE_WON', or 'BLACK_WON'
        """
        return self.__game_state

    def set_game_state(self, state):
        """
        A setter method that changes the game state, used primarily
        when game is finished to change to either 'WHITE_WON', or 'BLACK_WON'
        """
        self.__game_state = state

    def switch_turn(self):
        """
        Switches the turn to the next player.
        """
        if self.__current_turn == 'black':
            self.__current_turn = 'white'
        else:
            self.__current_turn = 'black'

    def make_move(self, from_square, to_square):
        """
        Attempts to move a piece from its current position to the desired position.
        The parameters from_square and to_square use algebraic chess notation (ex: 'e2').
        This method abstracts specific methods that are detailed in their respective classes,
        checks if the move is valid, updates the board state accordingly,
        switches the player's turn, and enables checks winning condition method,
        which returns boolean value depending on what conditions met by the move.
        Capturing is also handled here.
        """
        print(f"Attempting to move from {from_square} to {to_square}")
        if self.__game_state != 'UNFINISHED':
            return False

        if not self.__board.is_within_bounds(from_square) or not self.__board.is_within_bounds(to_square):
            return False

        current_piece = self.__board.get_piece(from_square)
        if not current_piece or current_piece.get_color() != self.__current_turn:
            return False

        if current_piece.is_valid_move(from_square, to_square, self.__board):
            opponent_piece = self.__board.get_piece(to_square)
            if opponent_piece and opponent_piece.get_color() != self.__current_turn:
                self.__board.remove_piece(to_square)

            self.__board.move_piece(from_square, to_square)

            if self.check_win_condition():
                return True

            self.switch_turn()

            return True

        return False

    def check_win_condition(self):
        """
        Checks whether win condition is met by keeping track of the number of each piece type
        using a dictionary.Mainly iterates through the chessboard, counts the number of each type of chess piece
        for both white and black, and stores the counts in the respective dictionaries
        to then see what specific pieces are still on the board and assess whether all pieces of one type have been captured
        """
        piece_types = ['Pawn', 'Knight', 'Bishop', 'Rook', 'Queen', 'King']
        # Create dictionaries for counting pieces of each type for white and black.
        white_pieces = {}  # Dictionary to count white pieces.
        black_pieces = {}  # Dictionary to count black pieces.

        # Initialize the piece count for each type to 0 for both white and black.
        for unique_piece in piece_types:
            white_pieces[unique_piece] = 0  # Initialize white piece count for the type.
            black_pieces[unique_piece] = 0  # Initialize black piece count for the type.

        for row in self.__board.get_board_array():
            for piece in row:
                if piece:
                    piece_type = piece.get_piece_type()  # Get the type of the piece directly
                    color = piece.get_color()
                    if color == 'white':
                        white_pieces[piece_type] += 1
                    else:
                        black_pieces[piece_type] += 1

        for color, pieces in [('white', white_pieces), ('black', black_pieces)]:
            for piece_count in pieces.values():
                if piece_count == 0:
                    if color == 'white':
                        self.__game_state = 'BLACK_WON'
                    else:
                        self.__game_state = 'WHITE_WON'
                    return True
        return False


class Piece:
    """
    Represents an abstract base class for all types of chess pieces
    """

    def __init__(self, color):
        """
        Initialize a new chess piece with the given color.
        """
        self.__color = color

    def get_color(self):
        """
        Returns the color of the chess piece (white or black).
        This method is crucial for determining whether it's the correct turn for a piece to move.
        """
        return self.__color

    def is_valid_move(self, initial_pos, new_pos, board):
        """
        Set up to be overridden in subclasses.
        This method allows for enforcement of the unique movement rules of each type of chess piece.
        By raising NotImplementedError, it ensures that subclasses provide their own implementation of this method.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")

    @staticmethod
    def convert_position(pos):
        """
        Converts the column from letter to number (a=0, b=1, c=2, etc.)
        and the row from 1-based to 0-based indexing.
        """
        col = ord(pos[0]) - ord('a')

        row = int(pos[1]) - 1
        return col, row

    @staticmethod
    def convert_to_algebraic(y, x):
        """
        Converts the column number back to a letter (0=a, 1=b, 2=c, etc.)
        and the row back to 1-based indexing.
        """
        col = chr(x + ord('a'))
        row = str(y + 1)
        return col + row


class Pawn(Piece):
    """
    Represents a pawn piece on chess board
    """

    def __init__(self, color):
        """
       Initializes the pawn object with the given color and sets its type.
        """
        super().__init__(color)
        self.__piece_type = 'Pawn'

    def get_piece_type(self):
        """
        Returns the type of the piece
        """
        return self.__piece_type

    def is_valid_move(self, from_square, to_square, board):
        """
        Validates the logic for basic movements and capture rules for pawns,
        ensuring movement position is first within boundaries,
        checking the diagonal capture logic for Pawns with
        abs(from_x - to_x) == 1 and to_y == from_y + direction,
        checking that the destination square is occupied by an opponent's piece, and if
        empty square then is able to move one square forward or if first move,
        then two squares forward.
        """
        if not ('a' <= to_square[0] <= 'h') or not ('1' <= to_square[1] <= '8'):
            return False

        from_x, from_y = Piece.convert_position(from_square)
        to_x, to_y = Piece.convert_position(to_square)
        if self.get_color() == 'white':
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6

        if abs(from_x - to_x) == 1 and to_y == from_y + direction:
            piece_at_destination = board.get_piece(to_square)
            return piece_at_destination is not None and piece_at_destination.get_color() != self.get_color()

        if from_x == to_x and to_y == from_y + direction:
            piece_at_destination = board.get_piece(to_square)
            return piece_at_destination is None

        if from_x == to_x and from_y == start_row and to_y == from_y + 2 * direction:
            piece_one_step_ahead = board.get_piece(Piece.convert_to_algebraic(from_y + direction, from_x))
            piece_two_steps_ahead = board.get_piece(Piece.convert_to_algebraic(from_y + 2 * direction, from_x))
            return piece_one_step_ahead is None and piece_two_steps_ahead is None

        return False


class Rook(Piece):
    """
    Represents a rook piece on chess board
    """

    def __init__(self, color):
        """
        Initializes rook object with the given color.
        """
        super().__init__(color)
        self.__piece_type = 'Rook'

    def get_piece_type(self):
        """
        Returns the type of the piece
        """
        return self.__piece_type

    def is_valid_move(self, from_square, to_square, board):
        """
        Validates the logic for basic movements and capture rules for Rook,
        ensuring the movement position is within the board boundaries.
        It checks if the rook moves either in a column or a row and
        verifies that there are no obstructions in the direction of movement.
        Additionally, it checks the final position to ensure a valid capture
        if an opponent's piece is present.
        """
        if not ('a' <= to_square[0] <= 'h') or not ('1' <= to_square[1] <= '8'):
            return False

        from_x, from_y = Piece.convert_position(from_square)
        to_x, to_y = Piece.convert_position(to_square)

        if from_x != to_x and from_y != to_y:
            return False

        if from_x == to_x:
            if to_y > from_y:
                step = 1
            else:
                step = -1

            for y in range(from_y + step, to_y, step):
                if board.get_piece(Piece.convert_to_algebraic(y, from_x)) is not None:
                    return False

            target_piece = board.get_piece(to_square)
            if target_piece and target_piece.get_color() == self.get_color():
                return False

        else:
            if to_x > from_x:
                step = 1
            else:
                step = -1

            for x in range(from_x + step, to_x, step):
                if board.get_piece(Piece.convert_to_algebraic(from_y, x)) is not None:
                    return False

            target_piece = board.get_piece(to_square)
            if target_piece and target_piece.get_color() == self.get_color():
                return False

        return True


class Knight(Piece):
    """
    Represents a knight piece on a chess board
    """

    def __init__(self, color):
        """
        Initializes the knight object with the given color and sets its type.
        """
        super().__init__(color)
        self.__piece_type = 'Knight'

    def get_piece_type(self):
        """
        Returns the type of the piece.
        """
        return self.__piece_type

    def is_valid_move(self, from_square, to_square, board):
        """
        Validates the movement logic for knights, ensuring the movement position is within
        the board boundaries. It checks if the knight moves in an L shape, either 2 squares
        in one direction and 1 in the other.
        """
        if not ('a' <= to_square[0] <= 'h') or not ('1' <= to_square[1] <= '8'):
            return False

        from_x, from_y = Piece.convert_position(from_square)
        to_x, to_y = Piece.convert_position(to_square)

        if (abs(from_x - to_x), abs(from_y - to_y)) not in [(1, 2), (2, 1)]:
            return False

        target_piece = board.get_piece(to_square)
        if target_piece and target_piece.get_color() == self.get_color():
            return False

        return True


class Bishop(Piece):
    """
    Represents a bishop piece on a chess board.
    """

    def __init__(self, color):
        """
        Initializes the bishop object with the given color and sets its type.
        """
        super().__init__(color)
        self.__piece_type = 'Bishop'

    def get_piece_type(self):
        """
         Returns the type of the piece.
        """
        return self.__piece_type

    def is_valid_move(self, from_square, to_square, board):
        """
        Validates the movement logic for bishops, ensuring the movement position is within
        the board boundaries. It checks if the bishop moves diagonally and verifies that
        there are no pieces obstructing its path.
        """
        if not ('a' <= to_square[0] <= 'h') or not ('1' <= to_square[1] <= '8'):
            return False

        from_x, from_y = Piece.convert_position(from_square)
        to_x, to_y = Piece.convert_position(to_square)

        if abs(from_x - to_x) != abs(from_y - to_y):
            return False

        if to_x > from_x:
            step_x = 1
        else:
            step_x = -1

        if to_y > from_y:
            step_y = 1
        else:
            step_y = -1

        y = from_y + step_y
        for x in range(from_x + step_x, to_x, step_x):
            if board.get_piece(Piece.convert_to_algebraic(y, x)) is not None:
                return False
            y += step_y

        return True


class Queen(Piece):
    """
    Represents a queen piece on a chess board.
    """

    def __init__(self, color):
        """
        Initializes the queen object with the given color and sets its type.
        """
        super().__init__(color)
        self.__piece_type = 'Queen'

    def get_piece_type(self):
        """
        Returns the type of the piece.
        """
        return self.__piece_type

    def is_valid_move(self, from_square, to_square, board):
        """
        Validates the movement logic for queens, ensuring the movement position is within
        the board boundaries. It checks if the queen's move is a combination of Rook and
        Bishop movements.
        """

        if not ('a' <= to_square[0] <= 'h') or not ('1' <= to_square[1] <= '8'):
            return False

        rook_like = Rook(self.get_color())
        bishop_like = Bishop(self.get_color())
        return (rook_like.is_valid_move(from_square, to_square, board) or
                bishop_like.is_valid_move(from_square, to_square, board))


class King(Piece):
    """
    Represents a king piece on a chess board.
    """

    def __init__(self, color):
        """
        Initializes the king object with the given color and sets its type.
        """
        super().__init__(color)
        self.__piece_type = 'King'

    def get_piece_type(self):
        """
        Returns the type of the piece.
        """
        return self.__piece_type

    def is_valid_move(self, from_square, to_square, board):
        """
        Validates the movement logic for kings, ensuring the movement position is within
        the board boundaries. It checks if the king moves one square in any direction.
        """
        if not ('a' <= to_square[0] <= 'h') or not ('1' <= to_square[1] <= '8'):
            return False

        from_x, from_y = Piece.convert_position(from_square)
        to_x, to_y = Piece.convert_position(to_square)

        if max(abs(from_x - to_x), abs(from_y - to_y)) != 1:
            return False

        return True


class Board:
    """
    Represents the board of the chess game with initial setup of pieces and game state
    """

    def __init__(self):
        """
        Initializes the 8x8 board that contains all pieces in their starting positions.
        """
        self.__board = self._initialize_board()

    def _initialize_board(self):
        """
        Creates the board with 8x8 grid where each cell contains either a Piece object or None.
        """
        board = []
        for i in range(8):
            row = []
            for j in range(8):
                row.append(None)
            board.append(row)

        for i in range(8):
            board[1][i] = Pawn('white')
            board[6][i] = Pawn('black')

        board[0][0] = Rook('white')
        board[0][7] = Rook('white')
        board[7][0] = Rook('black')
        board[7][7] = Rook('black')

        board[0][1] = Knight('white')
        board[0][6] = Knight('white')
        board[7][1] = Knight('black')
        board[7][6] = Knight('black')

        board[0][2] = Bishop('white')
        board[0][5] = Bishop('white')
        board[7][2] = Bishop('black')
        board[7][5] = Bishop('black')

        board[0][3] = Queen('white')
        board[7][3] = Queen('black')

        board[0][4] = King('white')
        board[7][4] = King('black')

        return board

    def get_board_array(self):
        """
        Returns the board in its current state
        """
        return self.__board

    def is_within_bounds(self, pos):
        """
        Check if the given position is within the 8x8 board grid boundary.
        """
        col, row = Piece.convert_position(pos)
        return 0 <= col < 8 and 0 <= row < 8

    def move_piece(self, from_pos, to_pos):
        """
        Takes in algebraic notations as parameters
        and moves a piece from one square to another on the chess board.
        """
        if not ('a' <= from_pos[0] <= 'h' and '1' <= from_pos[1] <= '8') or \
                not ('a' <= to_pos[0] <= 'h' and '1' <= to_pos[1] <= '8'):
            raise ValueError("Position out of bounds")

        from_x, from_y = Piece.convert_position(from_pos)
        to_x, to_y = Piece.convert_position(to_pos)

        self.__board[to_y][to_x] = self.__board[from_y][from_x]
        self.__board[from_y][from_x] = None

    def remove_piece(self, pos):
        """
        Removes a piece from the board at the given position.
        """
        x, y = Piece.convert_position(pos)
        if 0 <= x < 8 and 0 <= y < 8:
            self.__board[y][x] = None
        else:
            raise ValueError("Position out of bounds")

    def get_piece(self, position):
        """
        Returns the piece at a given position, parameter is in algebraic notation
        """
        x, y = Piece.convert_position(position)
        return self.__board[y][x]

