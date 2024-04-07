from chess import Board, parse_square, Termination, Move, STARTING_FEN


class LogicBoard(Board):
    _instance = None
    graphic_board = None
    ended_game = None
    initial_fen = STARTING_FEN
    advanced_history = []
    mode = "analyze"
    stats_frame = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def piece_moves(self, field_name):
        moves_list = []
        field = parse_square(field_name)
        piece = self.piece_at(field)
        if piece is not None:
            for move in self.legal_moves:
                if move.from_square == field:
                    moves_list.append(move.uci()[2] + move.uci()[3])
        return moves_list

    def check_turn(self):
        if self.turn:
            return "w"
        else:
            return "b"

    def check_end(self):
        self.ended_game = self.outcome()
        if self.ended_game is not None:
            result = self.ended_game.termination
            print(result)
            if result == Termination.CHECKMATE:
                print("Mat")
            elif result == Termination.STALEMATE:
                print("Imapss")
            elif result == Termination.INSUFFICIENT_MATERIAL:
                print("Niemożliwy")
            elif result == Termination.SEVENTYFIVE_MOVES:
                print("Remis 75 ruchow")
            elif result == Termination.FIVEFOLD_REPETITION:
                print("Remis powtorzenia")
            elif result == Termination.FIFTY_MOVES:
                print("zasada 50 ruchow")
            elif result == Termination.THREEFOLD_REPETITION:
                print("powtórzenie 3 ruchow")

            print(self.ended_game.winner)

    def restart(self):
        self.reset()
        self.graphic_board.clear_pieces()
        self.graphic_board.init_pieces()
        self.graphic_board.draw_pieces()
        self.advanced_history.clear()
        self.stats_frame.clear_history()
        self.stats_frame.empty_history()

    def find_info(self, move):
        if self.is_into_check(move):
            return "Szach"
        elif self.is_capture(move):
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
                    "image": piece.image,
                    "about": add_info}
        self.advanced_history.append(advanced)



