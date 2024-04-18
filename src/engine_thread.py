from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from chess import Move, Board, square_name


class PlayWorker(QObject):
    finished = pyqtSignal(Move)

    def __init__(self, logic_board):
        super().__init__()
        self.logic_board = logic_board

    @pyqtSlot()
    def calc_move(self):
        fen = self.logic_board.fen()
        new_board = Board(fen)
        engine_move = self.logic_board.engine.create_move(new_board)
        self.finished.emit(engine_move.move)


class AnalyzeWorker(QObject):
    finished = pyqtSignal()

    def __init__(self, logic_board):
        super().__init__()
        self.logic_board = logic_board

    @pyqtSlot()
    def analyze_move(self):
        fen = self.logic_board.fen()
        new_board = Board(fen)
        self.logic_board.engine.analyze_procedure(new_board, self.logic_board.halfmove_clock)
        self.finished.emit()
