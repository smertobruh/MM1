import pygame
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtGui import QImage, QPainter
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class PygameWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 600)

        # Инициализация Pygame
        pygame.init()
        self.screen = pygame.Surface((800, 600))
        self.screen.fill((0, 0, 0))

    def draw_planet(self, x, y, planet):
        # Логика игры
        m = planet.m
        if m > 1e29:
            pygame.draw.circle(self.screen, (255, 255, 0), (x,y), 6)
        else:
            pygame.draw.circle(self.screen, (255, 255, 255), (x, y), 2)
        # Отображаем Pygame на виджете
        self.update()

    def clear(self):
        self.screen = pygame.Surface((800, 600))
        self.update()

    def paintEvent(self, event):
        """ Переносим изображение Pygame на виджет """
        qt_image = pygame.image.tostring(self.screen, 'RGBA')
        q_image = QImage(qt_image, 800, 600, QImage.Format.Format_RGBA8888)

        painter = QPainter(self)
        painter.drawImage(0, 0, q_image)

    def closeEvent(self, event):
        pygame.quit()
        event.accept()

class Graphic3D(FigureCanvasQTAgg):
    """
    Класс графического окна.
    """
    def __init__(self, 
                 width : int = 5, 
                 height : int = 4, 
                 dpi : int = 100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111, projection="3d")
        super(Graphic3D, self).__init__(figure=fig)

class Rect(QtWidgets.QWidget):
    """
    Класс прямоугольного элемента окна.
    """
    def __init__(self, 
                 width : int = None, 
                 height : int = None):
        """
        Args:
            width: ширина элемента.
            height: высота элемента.
        """
        super(Rect, self).__init__()
        if isinstance(width, int):
            self.setMaximumWidth(width)
        if isinstance(height, int):
            self.setMaximumHeight(height)

class AddableWidget:
    """
    Класс, позволяющий добавить элемент в данный элемент.
    """
    def add_widget(self, 
                   widget : QtWidgets.QWidget):
        """
        Метод добавления виджетов.

        Args:
            widget: графический элемент.
        """
        self.lay.addWidget(widget)

    def add_widgets(self, 
                    widgets : list[QtWidgets.QWidget]):
        """
        Метод добавления виджетов.

        Args:
            widgets: список графических элементов.
        """
        if widgets == None:
            return
        for widget in widgets:
            self.add_widget(widget)

class HBox(Rect, AddableWidget):
    """
    Класс-коробка для горизонтального добавления элементов.
    """
    def __init__(self, 
                 width : int = None, 
                 height : int = None, 
                 widgets : list[QtWidgets.QWidget] = None):
        """
        Args:
            width: ширина элемента.
            height: высота элемента.
            widgets: список графических элементов.
        """
        super(__class__, self).__init__(width, height)
        self.lay = QtWidgets.QHBoxLayout(self)
        self.add_widgets(widgets)

class VBox(Rect, AddableWidget):
    """
    Класс-коробка для вертикального добавления элементов.
    """
    def __init__(self, 
                 width : int = None, 
                 height : int = None, 
                 widgets : list[QtWidgets.QWidget] = None):
        """
        Args:
            width: ширина элемента.
            height: высота элемента.
            widgets: список графических элементов.
        """
        super(__class__, self).__init__(width, height)
        self.lay = QtWidgets.QVBoxLayout(self)
        self.add_widgets(widgets)

class Form(Rect, AddableWidget):
    """
    Класс-коробка для добавления элементов в форму.
    """
    def __init__(self, 
                 width = None, 
                 height = None, 
                 widgets : list[QtWidgets.QWidget] = None):
        """
        Args:
            width: ширина элемента.
            height: высота элемента.
            widgets: список графических элементов.
        """
        super(__class__, self).__init__(width, height)
        self.lay = QtWidgets.QFormLayout(self)
        self.add_widgets(widgets)

class TextLine(QtWidgets.QLineEdit):
    """
    Класс неизменяегомого текстового поля.
    """
    def __init__(self):
        super(__class__, self).__init__()
        self.setEnabled(True)
        self.setText("")
        self.setReadOnly(True)

class Table(QtWidgets.QTableWidget):
    """
    Класс графической таблицы.
    """
    def __init__(self, 
                 cols : int = 0):
        """
        Args:
            cols: число столбцов.
        """
        super(__class__, self).__init__()
        self.setRowCount(0)
        self.setColumnCount(cols)
        self.count = 0

    def add_item(self, 
                 item : QtWidgets.QTableWidgetItem):
        """
        Метод добавления элемента таблицы.

        Args:
            item: графический элемент таблицы.
        """
        self.setHorizontalHeaderItem(self.count, item)
        self.count += 1

    def add_items(self, 
                  items : list[QtWidgets.QTableWidgetItem]):
        """
        Метод добавления списка элементов таблицы.

        Args:
            item: список графических элементов таблицы.
        """
        for item in items:
            self.add_item(item)

    def add_text(self, 
                 text : str):
        """
        Метод добавления текста в таблицу.

        Args:
            texts: текст.
        """
        self.add_item(QtWidgets.QTableWidgetItem())
        item = self.horizontalHeaderItem(self.count-1)
        item.setText(text)

    def add_texts(self, 
                  texts : list[str]):
        """
        Метод добавления списка текстов в таблицу.

        Args:
            texts: список текстов.
        """
        for text in texts:
            self.add_text(text)

class Alert(QtWidgets.QDialog, AddableWidget):
    def __init__(self, 
                 window,
                 text: str):
        """
        Args:
            window: окно для присоединения.
            text: текст ошибки.
        """
        super(__class__, self).__init__(window)
        self.lay = QtWidgets.QHBoxLayout(self)
        self.add_widget(QtWidgets.QLabel(text))