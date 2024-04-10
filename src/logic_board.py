from chess import Board, parse_square, Termination, Move, STARTING_FEN, square_name, WHITE, BLACK


class LogicBoard(Board):
    _instance = None
    graphic_board = None
    game_widget = None
    stats_frame = None
    ended_game = None
    initial_fen = STARTING_FEN
    advanced_history = []
    mode = "analyze"
    forward_moves = []
    player_side = None

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
            self.make_winner_message()
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
        self.forward_moves.clear()
        self.stats_frame.clear_history()
        self.stats_frame.empty_history()
        self.stats_frame.update_buttons()
        self.ended_game = None

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
            last_move = self.advanced_history.pop()
            move = last_move.get('move')
            piece = last_move.get('piece')
            action = last_move.get('about')

            if "Poddanie" in action:
                self.ended_game = None
                self.graphic_board.undo_capture()
            else:
                self.pop()
                self.valid_remove(action, move)
                piece.undo_last_move()
                self.forward_moves.append(last_move)
                self.graphic_board.clear_highlighted()

            if len(self.advanced_history) == 0:
                self.stats_frame.empty_history()
            else:
                new_last_piece = self.advanced_history[-1].get("piece")
                self.graphic_board.highlight_field(new_last_piece.previous_fields[-1])
                self.update_history()

            self.graphic_board.clear_circles()
            self.graphic_board.clear_captures()
            self.stats_frame.update_buttons()

    def valid_remove(self, action, move):
        if action == "Roszada":
            self.graphic_board.undo_castling(move)

        if "Bicie" in action:
            self.graphic_board.undo_capture()

        if self.ended_game is not None:
            self.ended_game = None

        if "Szach" in action:
            self.graphic_board.remove_undo_check()

    def forward_move(self):
        if self.forward_moves:
            next_move = self.forward_moves.pop()
            return next_move
        return None

    def cleaar_forwards(self):
        if self.forward_moves:
            self.forward_moves.clear()
            self.stats_frame.update_buttons()

    def make_surrender(self):
        king = None
        if self.turn:
            king = self.graphic_board.find_piece_by_name("w_king")
        else:
            king = self.graphic_board.find_piece_by_name("b_king")

        move_out = Move.from_uci("0000")
        self.advanced_move(king, move_out, "Poddanie gry")
        self.graphic_board.remove_captured(king.current_field.chess_pos)
        self.ended_game = "Surrender"
        self.update_history()

    def sets_game(self, type):
        if type != self.mode:
            if type == "game":
                self.game_widget.side_up()
                if self.player_side is not None:
                    self.stats_frame.set_game_label(type)
            elif type == "analyze":
                self.player_side = None
                self.stats_frame.set_game_label(type)
            self.prepare_board()
            self.mode = type

    def prepare_board(self):
        self.restart()
        if self.player_side == "black":
            while self.graphic_board.front_side != "black":
                self.graphic_board.rotate_board()
        else:
            while self.graphic_board.front_side != "white":
                self.graphic_board.rotate_board()

    def make_winner_message(self):
        if self.ended_game.winner == WHITE:
            winner_widget = self.game_widget.make_winner_msg("w_king")
        elif self.ended_game.winner == BLACK:
            winner_widget = self.game_widget.make_winner_msg("b_king")
        else:
            winner_widget = self.game_widget.make_winner_msg("draw")
        self.game_widget.winner_up(winner_widget)

