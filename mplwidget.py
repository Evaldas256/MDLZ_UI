# ------------------------------------------------------
# -------------------- mplwidget.py --------------------
# ------------------------------------------------------
import numpy as np
from PySide2.QtCore import QSize, Qt
from PySide2.QtGui import QIcon, QColor

from matplotlib.widgets import SpanSelector
from PySide2.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.ticker as ticker

class MplWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.canvas = FigureCanvas(Figure())

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        self.figure = Figure(facecolor='black')
        self.figure = self.canvas.figure


        self.axes = self.figure.add_subplot(111,snap=True)
        self.selector = SpanSelector(self.axes, self.onselect, 'horizontal', useblit=True)

        # def onmove(xmin, xmax):
        #     print(f"xmin: {xmin}, xmax: {xmax}")
        #
        # self.selector.onmove_callback = onmove
        # self.axes.tick_params(axis='x', labelrotation=90)
        # self.figure.subplots_adjust(bottom=0.4)

        # set the x-axis format to display only the time

        self.setLayout(vertical_layout)
        self.axes.clear()

        # Plot the data on the axes
        self.axes.plot()

        self.formatter = mdates.DateFormatter('%H:%M:%S')
        self.axes.xaxis.set_major_formatter(self.formatter)
        locator = ticker.MultipleLocator(10)
        self.axes.xaxis.set_major_locator(locator)


        self.toolbar = NavigationToolbar(self.canvas, self)
        klavisai = []
        # print(self.toolbar.findChildren(QToolButton))
        home_icon = QIcon(":/icons/Icons/home.png")
        backward_icon = QIcon(":/icons/Icons/arrow-left.png")
        forward_icon = QIcon(":/icons/Icons/arrow-right.png")

        zoomIn_icon = QIcon(":/icons/Icons/zoom-in.png")
        save_icon = QIcon(":/icons/Icons/save.png")

        self.toolbar.findChildren(QToolButton)[1].setIcon(home_icon)
        self.toolbar.findChildren(QToolButton)[2].setIcon(backward_icon)
        self.toolbar.findChildren(QToolButton)[3].setIcon(forward_icon)
        self.toolbar.findChildren(QToolButton)[5].setIcon(zoomIn_icon)
        self.toolbar.findChildren(QToolButton)[8].setIcon(save_icon)

        # for tool_button in self.toolbar.findChildren(QToolButton):
        #
        #     new_icon = QIcon(":/icons/Icons/activity.png")
        #
        #     tool_button.setIcon(new_icon)
        # print(klavisai)

        vertical_layout.addWidget(self.toolbar)

        self.axes.set_facecolor('black')
        self.axes.spines['bottom'].set_color('darkgray')
        self.axes.spines['top'].set_color('darkgray')
        self.axes.spines['right'].set_color('darkgray')
        self.axes.spines['left'].set_color('darkgray')

        # Set the color of the tick labels and tick lines to white
        self.axes.tick_params(axis='both', colors='white')

        self.figure.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.2, hspace=0.2)
        self.figure.patch.set_facecolor('black')

        # Refresh the canvas to show the plot
        self.canvas.draw()

    def onselect(self, xmin, xmax):
        # this function will be called when the user selects an interval with the SpanSelector
        # do something with the selected interval here
        xmin_dt = np.datetime64(int(xmin), 'D') + np.timedelta64(int((xmin % 1) * 86400), 's')

        # Format the datetime object into a string
        xmin_str = np.datetime_as_string(xmin_dt, unit='s')

        print(xmin_str)
        pass
