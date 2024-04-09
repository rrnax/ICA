from chess import Board, parse_square, Termination, Move, STARTING_FEN, square_name


class LogicBoard(Board):
    _instance = None
    graphic_board = None
    stats_frame = None
    ended_game = None
    initial_fen = STARTING_FEN
    advanced_history = []
    mode = "analyze"

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def find_possible_fields(self, field_id):
        possible_fields = []
        field = parse_square(field_id)
        for move in self.legal_moves:
            if move.from_square == field:
                field_position = square_name(move.to_square)
                for graphic_field in self.graphic_board.fields:
                    if graphic_field.chess_pos == field_position:
                        possible_fields.append(graphic_field)
        return possible_fields

    def check_turn(self, piece_color):
        if self.ended_game is None:
            if self.turn:
                if piece_color == 'w':
                    return True
            else:
                if piece_color == 'b':
                    return True
        return False

    def check_end(self):
        self.ended_game = self.outcome()
        if self.ended_game is not None:
            result = self.ended_game.termination
            if result == Termination.CHECKMATE:
                return "Mat"
            elif result == Termination.STALEMATE:
                return "Pat-impas"
            elif result == Termination.INSUFFICIENT_MATERIAL:
                return "Pat-brak pionów"
            elif result == Termination.SEVENTYFIVE_MOVES:
                return "Pat-75 ruchów"
            elif result == Termination.FIVEFOLD_REPETITION:
                return "Pat-5 powtórzeń"
            elif result == Termination.FIFTY_MOVES:
                return "Pat-50 ruchów"
            elif result == Termination.THREEFOLD_REPETITION:
                return "Pat-3 powtórzenia"
        else:
            if self.is_check():
                return "Szach"
            else:
                return ""

    def restart(self):
        self.reset()
        self.graphic_board.clear_pieces()
        self.graphic_board.init_pieces()
        self.graphic_board.draw_pieces()
        self.advanced_history.clear()
        self.stats_frame.clear_history()
        self.stats_frame.empty_history()

    def find_info(self, move):

        if self.is_capture(move):
            return "Bicie"
        elif self.is_castling(move):
            return "Roszada"
        elif self.is_en_passant(move):
            return "W przelocie"
        elif move.promotion:
            return "Promocja"
        else:
            return ""

    def advanced_move(self, piece, move, add_info):
        advanced = {"move": move,
                    "piece": piece,
                    "about": add_info}
        self.advanced_history.append(advanced)

    def update_history(self):
        self.stats_frame.update_history()

    def remove_last_move(self):
        if self.advanced_history:
            self.pop()
            last_move = self.advanced_history.pop()
            move = last_move.get('move')
            piece = last_move.get('piece')
            action = last_move.get('about')

            self.valid_remove(action, move)
            piece.undo_last_move()
            self.graphic_board.clear_highlighted()
            if len(self.advanced_history) == 0:
                self.stats_frame.empty_history()
            else:
                new_last_piece = self.advanced_history[-1].get("piece")
                self.graphic_board.highlight_field(new_last_piece.previous_fields[-1])
                self.update_history()

            self.graphic_board.clear_circles()
            self.graphic_board.clear_captures()

    def valid_remove(self, action, move):
        if action == "Roszada":
            self.graphic_board.undo_castling(move)

        if "Bicie" in action:
            self.graphic_board.undo_capture()

        if self.ended_game is not None:
            self.ended_game = None

        if "Szach" in action:
            self.graphic_board.remove_undo_chess()





