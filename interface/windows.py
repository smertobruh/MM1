from PyQt6 import QtCore, QtWidgets
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QToolBar
from matplotlib.backends.backend_qt import NavigationToolbar2QT

import interface.widgets as widgets

class UiMainWindow:
    """
    Класс, добавляющий в окно визуальные элементы.
    """
    def setupUi(self):
        """
        Метод инициализации визуальных элементов.
        """
        self.setObjectName("MainWindow")
        self.resize(1042, 571)
        self.central_box = widgets.HBox()
        #self.graphic_box = widgets.Graphic3D(width=5, height=4, dpi=100)
        self.graphic_box = widgets.PygameWidget()
        self.sidebar_box = widgets.Form(width=700)

        self.time_sec_line = widgets.TextLine()
        self.time_max_sec_line = widgets.TextLine()
        self.sidebar_box.add_widget(
            widgets.HBox(widgets=[
                QtWidgets.QLabel("Time, sec"), 
                self.time_sec_line,
                QtWidgets.QLabel("of"), 
                self.time_max_sec_line
            ])
        )
        
        self.time_day_line = widgets.TextLine()
        self.time_max_day_line = widgets.TextLine()
        self.sidebar_box.add_widget(
            widgets.HBox(widgets=[
                QtWidgets.QLabel("Time, day"), 
                self.time_day_line,
                QtWidgets.QLabel("of"), 
                self.time_max_day_line
            ])
        )

        self.energy_line = widgets.TextLine()
        self.center_m = widgets.TextLine()
        self.sidebar_box.add_widget(
            widgets.VBox(widgets=[
                QtWidgets.QLabel("Total energy, J"),
                self.energy_line,
                QtWidgets.QLabel("Center m"),
                self.center_m
            ])
        )

        self.table = widgets.Table(cols=7)
        self.table.add_texts(["X", "Y", "Z", "Vx", "Vy", "Vz", "M"])
        self.add_row_button = QtWidgets.QPushButton("ADD ROW")
        self.delete_row_button = QtWidgets.QPushButton("DELETE ROW")


        self.method_list = QtWidgets.QComboBox()
        self.method_list.addItems(["Euler", "Euler Kramer", "Biman", "Vernel"])

        self.time_edit_line = QtWidgets.QLineEdit()
        self.ht_edit_line = QtWidgets.QLineEdit()
        self.sidebar_box.add_widget(
            widgets.Form(widgets=[
                widgets.HBox(widgets=[self.add_row_button, self.delete_row_button]),
                self.table,
                self.method_list,
                widgets.HBox(widgets=[
                    widgets.VBox(widgets=[QtWidgets.QLabel("Time, sec"), self.time_edit_line]),
                    widgets.VBox(widgets=[QtWidgets.QLabel("Ht, sec"), self.ht_edit_line])
                ])
            ])
        )

        self.play_button = QtWidgets.QPushButton("PLAY")
        self.pause_button = QtWidgets.QPushButton("PAUSE")
        self.reset_button = QtWidgets.QPushButton("RESET")
        self.clear_button = QtWidgets.QPushButton("Clear")
        self.sidebar_box.add_widget(
            widgets.HBox(widgets=[
                self.play_button,
                self.pause_button,
                self.reset_button,
                self.clear_button
            ])
        )

        # Создаем тулбар
        toolbar = QToolBar("Мой тулбар")
        self.addToolBar(toolbar)

        # Создаем действие для кнопки
        self.open_file_action = QAction("Открыть")
        self.save_file_action = QAction("Сохранить")
        # Добавляем действие в тулбар
        toolbar.addAction(self.open_file_action)
        toolbar.addAction(self.save_file_action)

        self.setCentralWidget(self.central_box)
        self.central_box.add_widget(self.sidebar_box)
        self.add_scale_button = QtWidgets.QPushButton("Add scale")
        self.minus_scale_button = QtWidgets.QPushButton("Minus scale")
        self.json = QtWidgets.QPushButton("JSON")
        self.load_json =  QtWidgets.QPushButton("Load JSON")
        self.central_box.add_widget(
            widgets.VBox(widgets=[
                widgets.HBox(widgets=[
                    self.add_scale_button,
                    self.minus_scale_button,
                    self.json,
                    self.load_json
                ]),
                self.graphic_box,
                #NavigationToolbar2QT(self.graphic_box, self)
            ])
        )
        #self.graphic_box.axes.format_coord = lambda x, y: ""

class TimerMainWindow:
    """
    Класс, добавляющий в окно таймер.
    """
    def setupTimer(self, 
                   interval : int = 100):
        """
        Метод инициализации таймера.

        Args:
            interval: промежуток времени между срабатываниями таймера.
        """
        self.frame_timer = QtCore.QTimer()
        self.frame_timer.setInterval(interval)