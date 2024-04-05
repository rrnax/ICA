from chess import Board, parse_square


class LogicBoard(Board):
    _instance = None
    graphic_board = None

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
