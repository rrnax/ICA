import asyncio

import chess.engine
from chess import engine


class ChessEngine:
    _instance = None
    stockfish = r"../engines/stockfish/stockfish-windows-x86-64.exe"
    engine_frame = None
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
        asyncio.set_event_loop_policy(engine.EventLoopPolicy())
        self.actual_engine = None
        self.actual_transport = None
        self.limits = engine.Limit(time=None, depth=15)
        self.opponent = engine.Opponent(name="Player", title="GM", rating=1500, is_engine=False)
        asyncio.run(self.connect_engine(self.stockfish))

    async def connect_engine(self, engine_path):
        self.actual_transport, self.actual_engine = await chess.engine.popen_uci(engine_path)
        print(self.actual_engine)

    async def close_connect(self):
        await self.actual_transport.close()

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
        if engine_txt == "Stockfish":
            self.actual_engine = self.stockfish
        elif engine_txt == "Leela chess zero":
            self.actual_engine = self.stockfish

