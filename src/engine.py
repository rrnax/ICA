import asyncio

import chess.engine
from chess import engine


class ChessEngine:
    _instance = None
    stockfish = r"../engines/stockfish/stockfish-windows-x86-64.exe"
    actual_engine = None
    actual_transport = None
    opponent = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def initialize(self):
        asyncio.set_event_loop_policy(engine.EventLoopPolicy())
        stockfish = r"../engines/stockfish/stockfish-windows-x86-64.exe"
        self.actual_engine = None
        self.actual_transport = None
        asyncio.run(self.connect_engine(stockfish))

    async def connect_engine(self, engine_path):
        self.actual_transport, self.actual_engine = await chess.engine.popen_uci(engine_path)
        print(self.actual_engine)

    async def close_connect(self):
        await self.actual_transport.close()


