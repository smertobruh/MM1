from application.params import AppPapams
from interface.windows import UiMainWindow, TimerMainWindow
import interface.widgets as widgets
from PyQt6.QtWidgets import QTableWidgetItem, QFileDialog
import math
import json


from gravity.planets import Planet
import gravity.difference_schemes as ds

def update_window(window : UiMainWindow):
    """
    Функция обновления окна.

    Args:
        window: окно с визуальными элементами.
    """
    app = AppPapams()
    update_window.num = 0
    graphic = window.graphic_box
    time_sec = window.time_sec_line
    time_day = window.time_day_line
    energy = window.energy_line
    center_m = window.center_m

    def wraper():
        if update_window.num == app.n // app.step:
            return
        planets = AppPapams().planets
        # if update_window.num == 0:
        #     max_planet = planets[0]
        #     for planet in planets:
        #         if max_planet.dist < planet.dist:
        #             max_planet = planet
        #
        #     return max(planet.movement.get_r(0)[0], planet.movement.get_r(1)[0], planet.movement.get_r(2)[0])
        # print(AppPapams().max_coord())

        ht = AppPapams().ht
        step = AppPapams().step
        AppPapams().calculate(planets, update_window.num*step, step, ht)

        update_axes(update_window.num, graphic)
        update_lines(update_window.num, time_sec, time_day, energy, center_m)

        update_window.num += 1
        #graphic.draw()
    return wraper

def update_axes(num : int, 
                graphic : widgets.PygameWidget):
    """
    Функция обновления графика на окне.

    Args:
        num: номер временного узла.
        graphic: окно графика.
    """
    planets = AppPapams().planets
    step = AppPapams().step
    scale = (AppPapams().scale * 50000)+1000

    # ax = graphic.axes
    # ax.clear()
    u = 0
    for planet in planets:
        r = planet.movement._r
        m = planet.m
        # print("x = {}".format(r[0, (num)*step-1]/scale))
        # print("y = {}".format(r[1, (num)*step-1]))
        # print("z = {}".format(r[2, (num)*step-1]))

        graphic.draw_planet(r[0, ((num+1)*step-1)]/scale+400, r[1, ((num+1)*step-1)]/scale+300, planet)
        # ax.plot3D(r[0, :(num+1)*step], r[1, :(num+1)*step], r[2, :(num+1)*step])
        # if m > 1e29:
        #     ax.scatter(r[0, (num+1)*step-1], r[1, (num+1)*step-1], r[2, (num+1)*step-1], s=60)
        # else:
        #     ax.scatter(r[0, (num+1)*step-1], r[1, (num+1)*step-1], r[2, (num+1)*step-1], s=20)
        u += planet.energy.get_u(num*step)

    # ax.set_title(f'Time = {ht*(num+1)*step-1} sec\nEnergy = {u}')
    # ax.set_xlabel('x')
    # ax.set_ylabel('y')
    # ax.set_zlabel('z')

def update_lines(num : int, 
                 time_sec : widgets.TextLine, 
                 time_day : widgets.TextLine, 
                 energy : widgets.TextLine,
                 center_m : widgets.TextLine):
    """
    Функция обновления текстовых полей окна.

    Args:
        num: номер временного узла.
        time_sec: текстовое поле со значением времени в секундах.
        time_day: текстовое поле со значением времени в днях.
        energy: текстовое поле со значением энергии.
    """
    planets = AppPapams().planets
    ht = AppPapams().ht
    step = AppPapams().step

    u = 0
    for planet in planets:
        u += planet.energy.get_u(num*step)
    time = ht*(num+1)*step-1
    m = ds.calculate_center_m(planets, num*step)

    energy.setText(str(u))
    time_sec.setText(str(time))
    time_day.setText(str(time // (3600*24)))
    center_m.setText(f"{m[0]}, {m[1]}, {m[2]}")

def start_timer(window : TimerMainWindow):
    """
    Функция начала обновления данных системы.

    Args:
        window: окно с таймером.
    """
    frame_timer = window.frame_timer
    def wraper():
        if AppPapams().reseted:
            frame_timer.start()
        else:
            dlg = widgets.Alert(window, text="Error in start data!")
            dlg.exec()
    return wraper

def reset_timer(window : UiMainWindow):
    """
    Функция обновления данных о системе с элементов окна.

    Args:
        window: окно с визуальными элементами.
    """
    def wraper():
        update_window.num = 0
        table = window.table
        n = AppPapams().n

        try:

            t = int(window.time_edit_line.text())
            ht = int(window.ht_edit_line.text())
            planets = []
            for i in range(0, table.rowCount()):
                x = float(table.item(i, 0).text())
                y = float(table.item(i, 1).text())
                z = float(table.item(i, 2).text())
                vx = float(table.item(i, 3).text())
                vy = float(table.item(i, 4).text())
                vz = float(table.item(i, 5).text())
                m = float(table.item(i, 6).text())
                planets.append(Planet(m, 3, n, r0=[x, y, z], v0=[vx, vy, vz]))
        except ValueError:
            dlg = widgets.Alert(window, text="Error in data!")
            dlg.exec()
            return

        AppPapams().planets = planets
        AppPapams().scale = scale()
        AppPapams().calculate = AppPapams().methods[window.method_list.currentText()]
        AppPapams().t = t
        AppPapams().ht = ht
        AppPapams().reseted = True

        window.time_max_sec_line.setText(str(t))
        window.time_max_day_line.setText(str(t // (3600*24)))
        clear(window)()
    return wraper

def add_row(window : UiMainWindow):
    """
    Функция добавления строки в таблице окна.

    Args:
        window: окно с визуальными элементами.
    """
    table = window.table
    def wraper():
        table.insertRow(table.rowCount())
        if table.rowCount() == 1:
            params = [0, 0, 0, 0, 0, 0, 1.2166E30]
            for i in range(table.columnCount()):
                table.setItem(table.rowCount() - 1, i, QTableWidgetItem(str(params[i])))
        else:
            planets_num = table.rowCount() - 1
            # print(23297.8704870374 / math.sqrt(planets_num))
            params = [planets_num * 149500000000, 0, 0, 0, 23297.8704870374 / math.sqrt(planets_num), 0, planets_num * 6.083E24]
            for i in range(table.columnCount()):
                table.setItem(table.rowCount() - 1, i, QTableWidgetItem(str(params[i])))
    return wraper

def delete_row(window : UiMainWindow):
    """
    Функция удаления строки в таблице окна.

    Args:
        window: окно с визуальными элементами.
    """
    table = window.table
    def wraper():
        if len(table.selectedIndexes()) != 1:
            table.removeRow(table.rowCount()-1)
        else:
            table.removeRow(table.selectedIndexes()[0].row())
    return wraper

def draw_planet_on_screen(self):
    return None

def clear(window : UiMainWindow):
    graphic_box = window.graphic_box

    def wraper():
        graphic_box.clear()

    return wraper

def add_scale(window : UiMainWindow):
    def wraper():
        AppPapams().scale = AppPapams().scale * 1.2
        clear(window)()

    return wraper

def minus_scale(window : UiMainWindow):
    def wraper():
        AppPapams().scale = AppPapams().scale / 1.2
        clear(window)()

    return wraper

def scale():
    max_planet = AppPapams().planets[0]
    for planet in AppPapams().planets:
        if max_planet.dist < planet.dist:
            max_planet = planet
    coord = max(max_planet.movement.get_r(0)[0], max_planet.movement.get_r(0)[1])
    scale = coord // 10000000
    return scale


def safe_json(path):
    appParams = AppPapams()
    data = {}
    data['planets'] = []
    for planet in appParams.planets:
        data['planets'].append({
            'x': planet.movement.get_r(0)[0],
            'y': planet.movement.get_r(0)[1],
            'z': planet.movement.get_r(0)[2],
            'vx': planet.movement.get_v(0)[0],
            'vy': planet.movement.get_v(0)[1],
            'vz': planet.movement.get_v(0)[2],
            'm': planet.m
        })
    data['params'] = []
    data['params'].append({
        't': appParams.t,
        'ht': appParams.ht
    })
    try:
        with open(path[0], 'w') as outfile:
            json.dump(data, outfile)
    except FileNotFoundError:
        print(f"File not fount with path: {path[0]}")

def load_json(path, window):
    table = window.table
    try:
        with open(path[0]) as json_file:
            data = json.load(json_file)
            for p in data['planets']:
                x = float(p['x'])
                y = float(p['y'])
                z = float(p['z'])
                vx = float(p['vx'])
                vy = float(p['vy'])
                vz = float(p['vz'])
                m = float(p['m'])
                table.insertRow(table.rowCount())
                params = [x, y, z, vx, vy, vz, m]
                for i in range(table.columnCount()):
                    table.setItem(table.rowCount() - 1, i, QTableWidgetItem(str(params[i])))
            for i in data['params']:
                window.time_edit_line.setText(str(i['t']))
                window.ht_edit_line.setText(str(i['ht']))
    except FileNotFoundError:
        print(f"File not found with path: {path[0]}")


def open_file_dialog(window : UiMainWindow):
    def wrapper():
        load_json(QFileDialog.getOpenFileName(window, "Выберите файл"),window)
    return wrapper

def save_json_dialog(window : UiMainWindow):
    def wrapper():
        safe_json(QFileDialog.getSaveFileName(window, "Сохранить как"))
    return wrapper
