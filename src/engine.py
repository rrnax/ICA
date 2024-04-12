import asyncio
import chess.engine
from chess import engine


class ChessEngine:
    _instance = None
    stockfish = r"../engines/stockfish/stockfish-windows-x86-64.exe"
    engine_frame = None
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
        # asyncio.set_event_loop_policy(engine.EventLoopPolicy())
        self.engine_name = "Stockfish"
        self.multi = 4
        self.limits = engine.Limit(time=None, depth=15)
        self.opponent = engine.Opponent(name="Player", title="None", rating=1500, is_engine=False)
        self.connect_engine(self.stockfish)
        self.engine_frame.update_values()

    # async def connect_engine(self, engine_path):
    #     self.actual_transport, self.actual_engine = await chess.engine.popen_uci(engine_path)
    #     print(self.actual_engine)
    #
    # async def close_connect(self):
    #     await self.actual_transport.close()

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

    def analyze_procedure(self, board, half):
        self.take_data(board, half)

    # async def take_data(self, board):
    #     result = await self.actual_engine.analysis(board=board, limit=self.limits, multipv=self.multi)
    #     print(result)

    def take_data(self, board, half):
        results = self.actual_engine.analyse(board=board, limit=self.limits, multipv=self.multi)
        for item in results:
            print(item['score'].black())
            print(item['score'].white())
            print(item['score'].wdl(model='sf16', ply=half).relative)
