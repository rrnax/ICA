from chess import Board, parse_square, Termination


class LogicBoard(Board):
    _instance = None
    graphic_board = None
    ended_game = None

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
