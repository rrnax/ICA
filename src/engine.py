import logging
from chess import engine, Board, square_name
from PyQt5.QtCore import Qt


class ChessEngine:
    _instance = None
    stockfish = r"../engines/stockfish/stockfish-windows-x86-64.exe"
    engine_frame = None
    stats_frame = None
    moves_frame = None
    engine_name = None
    actual_engine = None
    actual_transport = None
    opponent = None
    limits = None
    multi = None
    last_fen = None
    last_result = None
    pieces_ids_list = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def initialize(self):
        logging.basicConfig(level=logging.INFO,
                            filename="../log/engine.log",
                            format='%(asctime)s ----------------------------------------- %(message)s',
                            datefmt='%d-%b-%y %H:%M:%S')
        self.engine_name = "Stockfish"
        self.multi = 4
        self.limits = engine.Limit(time=None, depth=15)
        self.opponent = engine.Opponent(name="Player", title="None", rating=1500, is_engine=False)
        self.connect_engine(self.stockfish)
        self.engine_frame.update_values()

    def connect_engine(self, engine_path):
        self.actual_engine = engine.SimpleEngine.popen_uci(engine_path)

    def close_connect(self):
        self.actual_engine.close()

    def set_elo(self, raiting):
        self.opponent.rating = raiting
        self.engine_frame.set_elo_label(str(raiting))

    def set_time(self, time):
        self.limits.time = time

    def set_depth(self, depth):
        self.limits.depth = depth
        self.engine_frame.set_depth_label(str(depth))

    def set_title(self, title):
        self.opponent.title = title

    def set_amount_moves(self, amount):
        self.multi = amount

    def set_engine(self, engine_txt):
        self.engine_frame.set_engine_label(engine_txt)
        self.engine_name = engine_txt

    def analyze_procedure(self, board, halfs):
        try:
            self.last_fen = board.fen()
            self.moves_frame.head_widget.hide()
            self.moves_frame.content_area.hide()
            self.moves_frame.setAlignment(Qt.AlignCenter)
            self.moves_frame.loader.show()
            results = self.actual_engine.analyse(board=board, limit=self.limits, multipv=self.multi)
            message = self.create_log_message(results, halfs)
            logging.info(message)
            self.last_result = self.creat_option_list(results)
            self.pieces_ids_list = self.find_pieces_ids()
            self.moves_frame.set_move_table(self.last_result)
            self.send_wdl(results, halfs)
            self.moves_frame.loader.hide()
            self.moves_frame.setAlignment(Qt.AlignTop)
            self.moves_frame.head_widget.show()
            self.moves_frame.content_area.show()
        except Exception as e:
            print("Błąd: ", e)

    def send_wdl(self, results, halfs):
        wdl_result = results[0]['score'].wdl(model='sf16', ply=halfs)
        final = None
        if not wdl_result.turn:
            wdl_result = results[-1]['score'].wdl(model='sf16', ply=halfs)
            final = wdl_result.black()
        else:
            final = wdl_result.white()
        self.stats_frame.set_probability(values=final)

    def create_log_message(self, results, halfs):
        message = ""
        for result in results:
            message += ("\n" + "Nr przeszukiwania:" + str(result['multipv'])
                        + ",### Czas przeszukiwania: " + str(result['time'])
                        + ",\n" + "Głebokość przeszukiwania: " + str(result['depth'])
                        + ",### Faktyczna głębokość: " + str(result['seldepth'])
                        + ",\n" + "Przeszukane pozycje: " + str(result['nodes'])
                        + ",### Przeszukane psunięcia[na sekunde]: " + str(result['nps'])
                        + ",\n" + "PovScore: " + str(result['score'].relative)
                        + ",### WDL: " + str(result['score'].wdl(model='sf16', ply=halfs).pov(True).expectation()) + "\n")
        return message

    def creat_option_list(self, results):
        list_of_options = []
        for result in results:
            list_of_moves = [result['score'].relative]
            for move in result['pv']:
                list_of_moves.append(move)
            list_of_options.append(list_of_moves)
        return list_of_options

    def find_pieces_ids(self):
        lists_list = []
        initial_fen = self.last_fen
        for row in self.last_result:
            pices_list = [0]
            row_board = Board(initial_fen)
            for i, item in enumerate(row):
                if i != 0:
                    if item is not None:
                        piece = row_board.piece_at(item.from_square)
                        if piece is not None:
                            pices_list.append(piece.symbol())
                        if row_board.is_pseudo_legal(item):
                            row_board.push(item)
            lists_list.append(pices_list)
        return lists_list

    def create_move(self, board):
        result = self.actual_engine.play(board=board, limit=self.limits, opponent=self.opponent)
        return result


