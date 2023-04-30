import json

import numpy as np
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_pdf import PdfPages
import random
from datetime import datetime
from PySide2.QtCore import QTimer, Qt
from ui_interface import *
########################################################################
# IMPORT Custom widgets
from Custom_Widgets.Widgets import *
from step_comment_widget import StepCommentWidget


########################################################################


########################################################################
## MAIN WINDOW CLASS
########################################################################
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        with open("data.json", "r") as f:
            json_data = f.read()

        # Convert the JSON string to a dictionary
        data = json.loads(json_data)
        self.production_steps = data['production_steps']
        print(self.production_steps)

        for steps in self.production_steps:
            self.ui.productionStepComboBox.addItem(steps['name'], userData=steps['color'])

        ########################################################################
        # APPLY JSON STYLESHEET
        ########################################################################
        # self = QMainWindow class
        # self.ui = Ui_MainWindow / user interface class
        loadJsonStyle(self, self.ui)
        ########################################################################

        ########################################################################

        self.show()

        ########################################################################
        # UPDATE APP SETTINGS LOADED FROM JSON STYLESHEET
        # ITS IMPORTANT TO RUN THIS AFTER SHOWING THE WINDOW
        # THIS PROCESS WILL RUN ON A SEPARATE THREAD WHEN GENERATING NEW ICONS
        # TO PREVENT THE WINDOW FROM BEING UNRESPONSIVE
        ########################################################################
        # self = QMainWindow class

        # READ ALL THEME NAMES CREATED FROM THE JSON FILE
        # NOTE THAT TWO THEMES (LIGHT AND DARK) WILL BE AUTOMATICALLY ADDED TO THE LIST
        # WHEN CREATING THEMES ON YOUR JSON FILE AVOID USING LIGHT OR DARK AS YOUR THEME NAME
        # settings = QSettings()

        # CHANGE THE THEME NAME IN SETTINGS
        # Use one of the app themes from your JSON file
        # settings.setValue("THEME", "Default-Dark")

        # RE APPLY THE NEW SETINGS
        # CompileStyleSheet might also work
        # CompileStyleSheet.applyCompiledSass(self)
        # QAppSettings.updateAppSettings(self)

        # EXPAND CENTER MENU WIDGET SIZE
        self.ui.settingsBtn.clicked.connect(lambda: self.ui.centerMenuContainer.expandMenu())
        self.ui.infoBtn.clicked.connect(lambda: self.ui.centerMenuContainer.expandMenu())
        self.ui.helpBtn.clicked.connect(lambda: self.ui.centerMenuContainer.expandMenu())

        # CLOSE CENTER MENU WIDGET SIZE
        self.ui.closeCenterMenuBtn.clicked.connect(lambda: self.ui.centerMenuContainer.collapseMenu())

        # EXPAND RIGHT MENU WIDGET SIZE
        self.ui.moreMenuBtn.clicked.connect(lambda: self.ui.rightMenuContainer.expandMenu())
        self.ui.profileMenuBtn.clicked.connect(lambda: self.ui.rightMenuContainer.expandMenu())

        # CLOSE RIGHT MENU WIDGET
        self.ui.closeRightMenuBtn.clicked.connect(lambda: self.ui.rightMenuContainer.collapseMenu())
        # CLOSE NOTIFICATION MENU WIDGET
        self.ui.closeNotificationBtn.clicked.connect(lambda: self.ui.popupNotificationContainer.collapseMenu())

        self.ui.tableWidget.cellClicked.connect(self.handle_cell_click)
        # SETTING TIMER TO UPDATE PLOT

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_graph)
        self.ui.startBtn.clicked.connect(lambda: self.timer.start(10000))
        # Update every 10 seconds (10000 milliseconds)
        self.ui.stopBtn.clicked.connect(lambda: self.save_to_pdf())

        self.ui.pauseBtn.clicked.connect(lambda: self.data_analysis())

        self.ui.anddNewRowBtn.clicked.connect(self.addRow)
        self.ui.deleteRowBtn.clicked.connect(self.deleteSelectedRow)
        self.ui.saveRecordsBtn.clicked.connect(self.save_to_json)
        self.ui.productionStepComboBox.setStyleSheet("QComboBox { border: 1px solid #ffa500; }")
        # Setting TableWidget column header background color
        self.ui.tableWidget.setStyleSheet(
            "QHeaderView::section {background-color:#16191d} QTableWidget { border: 1px solid #ffa500; }")

        self.ui.loadGraphBtn.clicked.connect(self.load_graph_data)
        self.ui.MplWidget.selector.onmove_callback=self.onmove

    def onmove(self,xmin, xmax):
        xmin_dt = np.datetime64(int(xmin), 'D') + np.timedelta64(int((xmin % 1) * 86400), 's')
        # Format the datetime object into a string
        xmin_str = np.datetime_as_string(xmin_dt, unit='s')
        xmax_dt = np.datetime64(int(xmax), 'D') + np.timedelta64(int((xmax % 1) * 86400), 's')
        # Format the datetime object into a string
        xmax_str = np.datetime_as_string(xmax_dt, unit='s')

        print(f"xmin: {xmin_str}, xmax: {xmax_str}")

    def save_to_json(self):
        data = []
        for row in range(self.ui.tableWidget.rowCount()):
            name = self.ui.tableWidget.item(row, 0).text()
            color = self.ui.tableWidget.item(row, 1).background().color()
            color_hex = color.name()
            data.append({'name': name, 'color': color_hex})
        with open("data.json", "w") as f:
            json.dump({"production_steps": data}, f, indent=4)

    def deleteSelectedRow(self):
        selected_items = self.ui.tableWidget.selectedItems()
        if selected_items:
            # Get the row index of the first selected item
            row = selected_items[0].row()
            self.ui.tableWidget.removeRow(row)

    def deleteLastRow(self):
        numRows = self.ui.tableWidget.rowCount()
        if numRows > 0:
            self.ui.tableWidget.removeRow(numRows - 1)

    def addRow(self):
        numRows = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.insertRow(numRows)
        item = QTableWidgetItem()
        item.setBackground(Qt.white)
        self.ui.tableWidget.setItem(numRows, self.ui.tableWidget.columnCount() - 1, item)
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)

    def handle_cell_click(self, row, column):
        if column == 1:
            color = QColorDialog.getColor()
            if color.isValid():
                # set the background color of the clicked cell
                self.ui.tableWidget.item(row, column).setBackground(color)

        # connect the slot to the cellClicked signal
        # Define the showColorPicker slot

    def showColorPicker(self, row, column):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            # Create a QTableWidgetItem with the selected color
            item = QtWidgets.QTableWidgetItem()
            item.setBackground(QtGui.QBrush(color))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            # Set the QTableWidgetItem in the selected cell
            self.ui.tableWidget.setItem(row, column, item)

    def load_graph_data(self):

        self.xy = np.load('my_array.npy', allow_pickle=True)

        self.ui.MplWidget.axes.clear()

        self.ui.MplWidget.axes.plot(self.xy[:, 0], self.xy[:, 1], label='Temperature',snap=True)
        self.ui.MplWidget.axes.scatter(self.xy[:, 0], self.xy[:, 1], color='red')
        self.y_min = np.amin(self.xy[:, 1])
        self.y_max = np.amax(self.xy[:, 1])
        # Define the colors

        # Loop through the data and plot each segment
        handles = []
        fill_dict = {}
        unique_colors = []
        unique_labels = []
        for i in range(len(self.xy) - 1):
            x = [self.xy[i][0], self.xy[i + 1][0]]
            y = [self.xy[i][1], self.xy[i + 1][1]]
            color = self.xy[i][2]
            production_step = self.xy[i][3]
            # check if color is already in unique colors list
            if color not in unique_colors:
                unique_colors.append(color)  # add color to unique colors list
                label = production_step  # set label to color if it's the first occurrence
            else:
                label = None  # set label to None if color already occurred

            # check if label already in unique labels list
            if label not in unique_labels:
                unique_labels.append(label)  # add label to unique labels list
                # create fill between plot with label if it's the first occurrence
                self.ui.MplWidget.axes.fill_between(x, self.y_min, self.y_max, color=color, alpha=0.5, label=label)
            else:
                # create fill between plot without label if label already occurred
                self.ui.MplWidget.axes.fill_between(x, self.y_min, self.y_max, color=color, alpha=0.5)

        # add legend with unique colors and labels

        self.ui.MplWidget.axes.legend(
            handles=[mpatches.Patch(color=color, label=label) for color, label in zip(unique_colors, unique_labels)])

        # self.ui.MplWidget.axes.legend(labels=colors.keys(), loc='upper right')
        self.ui.MplWidget.axes.set_title('Temperature in time')
        self.formatter = mdates.DateFormatter('%H:%M:%S')
        self.ui.MplWidget.axes.xaxis.set_major_formatter(self.formatter)
        # Set the x-axis locator
        locator = mdates.MinuteLocator(interval=1)
        self.ui.MplWidget.axes.xaxis.set_major_locator(locator)

        # Set the grid every 10 seconds
        minor_locator = mdates.SecondLocator(interval=10)
        self.ui.MplWidget.axes.xaxis.set_minor_locator(minor_locator)
        self.ui.MplWidget.axes.grid(True)
        # get the current time
        current_time = np.datetime64(datetime.now())

        # calculate the start time for the 15-minute window
        # start_time = current_time - np.timedelta64(15, 'm')
        # future_time = current_time + np.timedelta64(15, 'm')
        # set the x-axis limits
        # self.ui.MplWidget.axes.set_xlim(start_time, future_time)

        handles, labels = self.ui.MplWidget.axes.get_legend_handles_labels()

        for fill, fill_color in fill_dict.items():
            if fill not in handles:
                handles.append(fill)
                labels.append(fill_color)

        self.ui.MplWidget.axes.legend(handles=handles, labels=labels, loc='upper center', bbox_to_anchor=(0.5, 1.15),
                                      ncol=4)

        self.ui.MplWidget.canvas.draw()


    def update_graph(self):

        selected_index = self.ui.productionStepComboBox.currentIndex()
        # Or get the data of the selected item (if you set data using setItemData())
        self.color_fill = self.ui.productionStepComboBox.itemData(selected_index)
        self.production_step = self.ui.productionStepComboBox.currentText()
        try:
            self.xy = np.load('my_array.npy', allow_pickle=True)
            self.temperature = random.randint(-10, 100)
            self.current_datetime = np.datetime64(datetime.datetime.now())
            self.new_row = [self.current_datetime, self.temperature, self.color_fill, self.production_step]
            self.xy = np.vstack([self.xy, self.new_row])
            print(self.new_row)
        except:
            self.xy = np.ndarray((0, 4))
            self.temperature = random.randint(-10, 100)
            self.current_datetime = np.datetime64(datetime.datetime.now())
            self.new_row = [self.current_datetime, self.temperature, self.color_fill, self.production_step]
            self.xy = np.vstack([self.xy, self.new_row])
            print(self.new_row)

        self.ui.MplWidget.axes.clear()

        self.ui.MplWidget.axes.plot(self.xy[:, 0], self.xy[:, 1], label='Temperature')
        self.ui.MplWidget.axes.scatter(self.xy[:, 0], self.xy[:, 1], color='red')
        self.y_min = np.amin(self.xy[:, 1])
        self.y_max = np.amax(self.xy[:, 1])
        # Define the colors

        # Loop through the data and plot each segment
        handles = []
        fill_dict = {}
        unique_colors = []
        unique_labels = []
        for i in range(len(self.xy) - 1):
            x = [self.xy[i][0], self.xy[i + 1][0]]
            y = [self.xy[i][1], self.xy[i + 1][1]]
            color = self.xy[i][2]
            production_step = self.xy[i][3]
            # check if color is already in unique colors list
            if color not in unique_colors:
                unique_colors.append(color)  # add color to unique colors list
                label = production_step  # set label to color if it's the first occurrence
            else:
                label = None  # set label to None if color already occurred

            # check if label already in unique labels list
            if label not in unique_labels:
                unique_labels.append(label)  # add label to unique labels list
                # create fill between plot with label if it's the first occurrence
                self.ui.MplWidget.axes.fill_between(x, self.y_min, self.y_max, color=color, alpha=0.5, label=label)
            else:
                # create fill between plot without label if label already occurred
                self.ui.MplWidget.axes.fill_between(x, self.y_min, self.y_max, color=color, alpha=0.5)

        # add legend with unique colors and labels

        self.ui.MplWidget.axes.legend(
            handles=[mpatches.Patch(color=color, label=label) for color, label in zip(unique_colors, unique_labels)])

        # self.ui.MplWidget.axes.legend(labels=colors.keys(), loc='upper right')
        self.ui.MplWidget.axes.set_title('Temperature in time')
        self.formatter = mdates.DateFormatter('%H:%M:%S')
        self.ui.MplWidget.axes.xaxis.set_major_formatter(self.formatter)

        # get the current time
        current_time = np.datetime64(datetime.now())

        # calculate the start time for the 15-minute window
        start_time = current_time - np.timedelta64(15, 'm')
        future_time = current_time + np.timedelta64(15, 'm')
        # set the x-axis limits
        self.ui.MplWidget.axes.set_xlim(start_time, future_time)
        np.save('my_array.npy', self.xy)

        handles, labels = self.ui.MplWidget.axes.get_legend_handles_labels()

        for fill, fill_color in fill_dict.items():
            if fill not in handles:
                handles.append(fill)
                labels.append(fill_color)

        self.ui.MplWidget.axes.legend(handles=handles, labels=labels, loc='upper center', bbox_to_anchor=(0.5, 1.15),
                                      ncol=4)

        self.ui.MplWidget.canvas.draw()

    def save_to_pdf(self):
        self.timer.stop()
        self.xy = np.load('my_array.npy', allow_pickle=True)
        # set page size to A4 in landscape orientation
        # Set A4 size in inches

        fig, ax = plt.subplots(figsize=(11.69, 8.27))

        ax.plot(self.xy[:, 0], self.xy[:, 1], label='Temperature')
        self.y_min = np.amin(self.xy[:, 1])
        self.y_max = np.amax(self.xy[:, 1])
        # Define the colors

        # Loop through the data and plot each segment
        fill_dict = {}
        unique_colors = []
        unique_labels = []
        for i in range(len(self.xy) - 1):
            x = [self.xy[i][0], self.xy[i + 1][0]]
            y = [self.xy[i][1], self.xy[i + 1][1]]
            color = self.xy[i][2]
            # check if color is already in unique colors list
            if color not in unique_colors:
                unique_colors.append(color)  # add color to unique colors list
                label = color  # set label to color if it's the first occurrence
            else:
                label = None  # set label to None if color already occurred

            # check if label already in unique labels list
            if label not in unique_labels:
                unique_labels.append(label)  # add label to unique labels list
                # create fill between plot with label if it's the first occurrence
                ax.fill_between(x, self.y_min, self.y_max, color=color, alpha=0.5, label=label)
            else:
                # create fill between plot without label if label already occurred
                ax.fill_between(x, self.y_min, self.y_max, color=color, alpha=0.5)

        # add legend with unique colors and labels

        ax.legend(
            handles=[mpatches.Patch(color=color, label=label) for color, label in zip(unique_colors, unique_labels)])

        ax.set_title('Temperature in time')
        self.formatter = mdates.DateFormatter('%H:%M:%S')
        ax.xaxis.set_major_formatter(self.formatter)

        handles, labels = ax.get_legend_handles_labels()

        for fill, fill_color in fill_dict.items():
            if fill not in handles:
                handles.append(fill)
                labels.append(fill_color)

        ax.legend(handles=handles, labels=labels, loc='upper right')

        # create a PdfPages object and save the figure to PDF
        with PdfPages('output.pdf') as pdf:
            pdf.savefig(orientation='portrait')

    def data_analysis(self):
        # load data file
        arr = np.load('my_array.npy', allow_pickle=True)
        # Define the logging interval
        logging_interval = 11000000

        # Sort the numpy array based on the step name and time columns
        arr = arr[np.lexsort((arr[:, 0], arr[:, 3]))]

        # Create a dictionary to store the intervals for each color name
        interval_dict = {}

        # Iterate through the sorted numpy array, tracking the current step name, start time of an interval, and previous time point
        current_step = arr[0, 3]
        interval_start = arr[0, 0]
        prev_time = arr[0, 0]
        for i in range(1, len(arr)):
            if arr[i, 3] != current_step or arr[i, 0] - prev_time > logging_interval:
                # Add the start and end times of the interval to the corresponding entry in the dictionary
                if current_step in interval_dict:
                    interval_dict[current_step].append((interval_start, prev_time))
                else:
                    interval_dict[current_step] = [(interval_start, prev_time)]
                # Update the current step, start time of the interval, and previous time point
                current_step = arr[i, 3]
                interval_start = arr[i, 0]
                prev_time = arr[i, 0]
            else:
                # Update the previous time point
                prev_time = arr[i, 0]

        # Add the start and end times of the final interval to the corresponding entry in the dictionary
        if current_step in interval_dict:
            interval_dict[current_step].append((interval_start, prev_time))
        else:
            interval_dict[current_step] = [(interval_start, prev_time)]
        self.list_of_event = []

        # Display all intervals from/to for each step
        for step, intervals in interval_dict.items():
            print(f"Step: {step}")
            for interval in intervals:
                interval_start = interval[0]
                time_str = str(interval_start.astype(datetime))
                time_start = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S.%f').time()
                time_start_withoutmicroseconds = time_start.replace(microsecond=0)
                interval_end = interval[1]
                time_str = str(interval_end.astype(datetime))
                time_end = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S.%f').time()
                time_end_withoutmicroseconds = time_end.replace(microsecond=0)
                for steps in self.production_steps:
                    if steps['name'] == step:
                        a = StepCommentWidget(step_name=step, start=f'{time_start_withoutmicroseconds}',
                                              end=f'{time_end_withoutmicroseconds}', background_color=steps['color'])
                        self.list_of_event.append(a)

                print(f"  Interval: ({interval_start}, {interval_end})")

        # Sorting lis_of_event and filling layout for step_comment_widget

        self.sorted_events = sorted(self.list_of_event, key=lambda e: e.start)

        for q in self.sorted_events:
            self.ui.verticalLayout_14.addWidget(q)


########################################################################
## EXECUTE APP
########################################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
########################################################################
## END===>
########################################################################
