from PyQt6 import QtWidgets
from interface.windows import UiMainWindow, TimerMainWindow
import application.actions as act

class MainWindow(QtWidgets.QMainWindow, UiMainWindow, TimerMainWindow):
    """
    Класс основного окна.
    """
    def __init__(self):
        super(QtWidgets.QMainWindow, self).__init__()
        self.setupUi()
        self.setupTimer(16)

        self.frame_timer.timeout.connect(act.update_window(self))
        self.play_button.clicked.connect(act.start_timer(self))
        self.pause_button.clicked.connect(lambda: self.frame_timer.stop())
        self.reset_button.clicked.connect(act.reset_timer(self))
        self.add_row_button.clicked.connect(act.add_row(self))
        self.delete_row_button.clicked.connect(act.delete_row(self))
        self.clear_button.clicked.connect(act.clear(self))
        self.add_scale_button.clicked.connect(act.add_scale(self))
        self.minus_scale_button.clicked.connect(act.minus_scale(self))
        self.json.clicked.connect(act.safe_json)
        self.open_file_action.triggered.connect(act.open_file_dialog(self))
        self.save_file_action.triggered.connect(act.save_json_dialog(self))
