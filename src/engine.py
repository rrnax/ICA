import logging
from chess import engine
from PyQt5.QtCore import Qt

class ChessEngine:
    _instance = None
    stockfish = r"../engines/stockfish/stockfish-windows-x86-64.exe"
    engine_frame = None
    moves_frame = None
    engine_name = None
    actual_engine = None
    actual_transport = None
    opponent = None
    limits = None
    multi = None

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
        print(self.actual_engine)

    def close_connect(self):
        self.actual_engine.close()

    def set_elo(self, raiting):
        self.opponent.rating = raiting
        self.engine_frame.set_elo_label(str(raiting))
        print(self.opponent)

    def set_time(self, time):
        self.limits.time = time
        print(self.limits)

    def set_depth(self, depth):
        self.limits.depth = depth
        self.engine_frame.set_depth_label(str(depth))
        print(self.limits)

    def set_title(self, title):
        self.opponent.title = title
        print(self.opponent)

    def set_amount_moves(self, amount):
        self.multi = amount
        print(self.multi)

    def set_engine(self, engine_txt):
        self.engine_frame.set_engine_label(engine_txt)
        self.engine_name = engine_txt

    def analyze_procedure(self, board, halfs):
        self.moves_frame.head_widget.hide()
        self.moves_frame.content_area.hide()
        self.moves_frame.setAlignment(Qt.AlignCenter)
        self.moves_frame.loader.show()
        results = self.actual_engine.analyse(board=board, limit=self.limits, multipv=self.multi)
        message = self.create_log_message(results, halfs)
        logging.info(message)
        option_list = self.creat_option_list(results)
        print(option_list)
        self.moves_frame.setAlignment(Qt.AlignTop)
        self.moves_frame.set_move_table(option_list)
        self.moves_frame.loader.hide()
        self.moves_frame.head_widget.show()
        self.moves_frame.content_area.show()

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