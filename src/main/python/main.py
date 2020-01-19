
# see https://stackoverflow.com/questions/50398483/how-do-i-get-the-animation-to-work-correctly-in-pyqt5-qt3d for3d modeling
# https://gis.stackexchange.com/questions/201732/enable-groupbox-only-when-checkbox-is-checked-pyqgis
# 
#libraries
from __future__ import unicode_literals
from fbs_runtime.application_context import ApplicationContext
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from pprint import pprint
from collections import Counter
import time
import sys
import os
import random
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import sqlite3
import webbrowser
from PIL import Image
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog, QDialog
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
#local
from new import Ui_MainWindow
from herc_tools import determine_region
from import_dialog import Ui_Dialog
from about_dialog import Ui_Dialog2
from change_read_delay import Ui_Dialog3
from change_max_graph_values import Ui_Dialog4

# Setup the Sheets API
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('sheets', 'v4', http=creds.authorize(Http()))

# Spreadsheet operation data
SPREADSHEET_ID = '1K_3HoLemrF0fYTmdT47LxnZcyGHhU7nC4pLsQebIU0s'

# Used with spreadsheets.values.append
value_input_option = 'USER_ENTERED' # should be kept this way since it's familiar, but i think RAW/USER_ENTERED are the main
insert_data_option = 'INSERT_ROWS' # OVERWRITE/INSERT_ROWS
append_range = "'Command Read Queue'!A2:B2" # where to search for the first empty row
appendlist = [] # what's actually gonna go places

# Used with spreadsheets.values.get
value_render_option = "FORMATTED_VALUE"
date_time_render_option = "FORMATTED_STRING"



# Request body values 
def append_data():
    value_range_body = {
        'values': appendlist
    }

    request = service.spreadsheets().values().append(spreadsheetId=SPREADSHEET_ID, range=append_range, valueInputOption=value_input_option, insertDataOption=insert_data_option, body=value_range_body)
    response = request.execute()

    pprint(response)

progname = "AACT Telemetry UI"
# Make sure that we are using QT5


x = []
y = []
y2 = [] #a set for each line, but the x value is shared

x_map = []
y_map = []

isActive = False

main_timer = QtCore.QTimer()
first = False
halt = False
using_db = False
db_target = ''

max_values = 75
read_delay = 1000

current_section = ''
elapsed_section_time = 0

starting_row = 2
timeout = 10
failed_attempts = 0 # The amount of times the client has found no new data.
heal_attempts = 0 #Amount of times healing has occurred in a row.
last_read = starting_row # Last read row; used to determine read_range. (Can't be used to compare against timestamp because of inconsistencies)
queue = [] # Queued data to print, given that its timestamp is unique.
queued_timestamps = [] # All timestamps.
timestamp_counts = {} # Amount of time each timestamp appears.
last_read_timestamp = 0 # Last timestamp read. If a timestamp is missing, the user is notified. (queue)
last_queued_timestamp = 0 # Last non-duplicate timestamp read.
first_timestamp_read = "" # Holds the very first timestamp set read, which often causes issues.
first_read = False # Boolean of "is this the actual first read?"
last_queue = [] #Last successfully printed set of data. Used in the event missing data occurs, in which case the client will replace it with the last known values.
lag_time = 0

def reset_vars():
    global starting_row
    global timeout
    global failed_attempts
    global heal_attempts
    global last_read
    global queue
    global queued_timestamps
    global timestamp_counts
    global last_read_timestamp
    global last_queued_timestamp
    global first_timestamp_read
    global first_read
    global last_queue
    global lag_time
    global x
    global y
    global y2
    global x_map
    global y_map
    global current_section
    global elapsed_section_time
    starting_row = 2
    timeout = 10
    failed_attempts = 0 # The amount of times the client has found no new data.
    heal_attempts = 0 #Amount of times healing has occurred in a row.
    last_read = starting_row # Last read row; used to determine read_range. (Can't be used to compare against timestamp because of inconsistencies)
    queue = [] # Queued data to print, given that its timestamp is unique.
    queued_timestamps = [] # All timestamps.
    timestamp_counts = {} # Amount of time each timestamp appears.
    last_read_timestamp = 0 # Last timestamp read. If a timestamp is missing, the user is notified. (queue)
    last_queued_timestamp = 0 # Last non-duplicate timestamp read.
    first_timestamp_read = "" # Holds the very first timestamp set read, which often causes issues.
    first_read = False # Boolean of "is this the actual first read?"
    last_queue = [] #Last successfully printed set of data. Used in the event missing data occurs, in which case the client will replace it with the last known values.
    lag_time = 0
    x = []
    y = []
    y2 = []
    x_map = []
    y_map = []
    current_section = ''
    elapsed_section_time = 0

def update_from_db(initial=False,initial_row=2,initial_timeout=10):
    global starting_row
    global timeout
    global failed_attempts
    global heal_attempts
    global last_read
    global queue
    global queued_timestamps
    global timestamp_counts
    global last_read_timestamp
    global last_queued_timestamp
    global first_timestamp_read
    global first_read
    global last_queue
    global lag_time
    global halt
    global db_target
    if initial:
        last_read = initial_row
        timeout = initial_timeout
    else:
        pass
    if len(queue) < 4 and initial:
        conn = sqlite3.connect(db_target)
        c = conn.cursor()
        c.execute('SELECT * FROM data')
        initial = c.fetchall()
        response = []
        for i in initial:
            response.append(list(i))
        for i in range(0,last_read):
            del response[0]
        if len(response) == 2:
            failed_attempts += 1
            if failed_attempts >= timeout:
                print('Timeout limit reached. Ending data read.')
                halt = True
                return
            else:
                print('No new data found. Retrying %s more time(s).'%(timeout-failed_attempts))
        else:
            first_timestamp_read = response[0][0]
            for i in response: #Perform initial pass. Returns all unique and duplicated timestamps to queued_timestamps.
                queued_timestamps.append(i[0])
            timestamp_counts = Counter(queued_timestamps)
            for i in response: #Perform second pass.
                if timestamp_counts[i[0]] > 1: # if this timestamp has duplicates:
                    if first_timestamp_read == i[0] and not first_read: # if it's the very first timestamp, and this is the actual first set:
                        i = response[(timestamp_counts[i[0]])-1] # set it to be the value of the last duplicated timestamp
                        queue.append(i)
                        last_queued_timestamp = int(i[0])
                        first_read = True
                    elif first_timestamp_read == i[0]:
                        pass # ignore if it's part of the first timestamp read
                    else:
                        print('Duplicate found. Reading as %s.'%(last_queued_timestamp + 1)) # if it's a regular duplicate, use it as the successive value to the last timestamp
                        i[0] = str(last_queued_timestamp + 1)
                        last_queued_timestamp = int(i[0])
                        queue.append(i)
                else:
                    queue.append(i)
                    last_queued_timestamp = int(i[0])
            first_read = True #In case there wasn't a duplicate, so this won't be triggered next round.
            last_read += len(response)
            failed_attempts = 0
    elif len(queue) < 1 and not initial:
        halt = True
    if len(queue) > 0:
        if int(queue[0][0]) - last_read_timestamp > 1 and last_read_timestamp != 0:
            print('attempting to heal data after timestamp %s'%last_read_timestamp) # if data is missing, replace it with the last known values. this should never occur for more than one or two readings.
            heal_attempt = last_queue
            heal_attempt[0] = str(last_read_timestamp + 1)
            queue.insert(0,heal_attempt)
            heal_attempts += 1
            if heal_attempts > timeout:
                print('Detected too large of a gap between values. Ending script.')
                halt = True
                return
        else:
            heal_attempts = 0
        last_read_timestamp = int(queue[0][0])
        last_queue = queue[0]
        lag_time = int(time.time())-last_read_timestamp
    
def update_data(initial=False,initial_row=2,initial_timeout=10):
    global starting_row
    global timeout
    global failed_attempts
    global heal_attempts
    global last_read
    global queue
    global queued_timestamps
    global timestamp_counts
    global last_read_timestamp
    global last_queued_timestamp
    global first_timestamp_read
    global first_read
    global last_queue
    global lag_time
    global halt
    if initial:
        last_read = initial_row
        timeout = initial_timeout
    else:
        pass
    if len(queue) < 4: #Only attempt to read new data if there are less than four seconds of data remaining. 
        read_range = ("Data!A%s:N"%last_read)
        request = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=read_range, valueRenderOption=value_render_option, dateTimeRenderOption=date_time_render_option)
        response = request.execute()
        if len(response) == 2:
            failed_attempts += 1
            if failed_attempts >= timeout:
                print('Timeout limit reached. Ending data read.')
                halt = True
                return
            else:
                print('No new data found. Retrying %s more time(s).'%(timeout-failed_attempts))
        else:
            first_timestamp_read = response['values'][0][0]
            for i in response['values']: #Perform initial pass. Returns all unique and duplicated timestamps to queued_timestamps.
                queued_timestamps.append(i[0])
            timestamp_counts = Counter(queued_timestamps)
            for i in response['values']: #Perform second pass.
                if timestamp_counts[i[0]] > 1: # if this timestamp has duplicates:
                    if first_timestamp_read == i[0] and not first_read: # if it's the very first timestamp, and this is the actual first set:
                        i = response['values'][(timestamp_counts[i[0]])-1] # set it to be the value of the last duplicated timestamp
                        queue.append(i)
                        last_queued_timestamp = int(i[0])
                        first_read = True
                    elif first_timestamp_read == i[0]:
                        pass # ignore if it's part of the first timestamp read
                    else:
                        print('Duplicate found. Reading as %s.'%(last_queued_timestamp + 1)) # if it's a regular duplicate, use it as the successive value to the last timestamp
                        i[0] = str(last_queued_timestamp + 1)
                        last_queued_timestamp = int(i[0])
                        queue.append(i)
                else:
                    queue.append(i)
                    last_queued_timestamp = int(i[0])
            first_read = True #In case there wasn't a duplicate, so this won't be triggered next round.
            last_read += len(response['values'])
            failed_attempts = 0
    if len(queue) > 0:
        if int(queue[0][0]) - last_read_timestamp > 1 and last_read_timestamp != 0:
            print('attempting to heal data after timestamp %s'%last_read_timestamp) # if data is missing, replace it with the last known values. this should never occur for more than one or two readings.
            heal_attempt = last_queue
            heal_attempt[0] = str(last_read_timestamp + 1)
            queue.insert(0,heal_attempt)
            heal_attempts += 1
            if heal_attempts > timeout:
                print('Detected too large of a gap between values. Ending script.')
                halt = True
                return
        else:
            heal_attempts = 0
        last_read_timestamp = int(queue[0][0])
        last_queue = queue[0]
        lag_time = int(time.time())-last_read_timestamp
        

class dht_plot_class(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=7.49, height=2.72, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(121) #1x2x1 grid;see https://stackoverflow.com/questions/3584805/in-matplotlib-what-does-the-argument-mean-in-fig-add-subplot111
        self.axes2 = fig.add_subplot(122) 
        
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

class herc_map_class(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5.35984, height=2.37743, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111) #1x1x1 grid;see https://stackoverflow.com/questions/3584805/in-matplotlib-what-does-the-argument-mean-in-fig-add-subplot111
        im = Image.open("map.png")
        im = im.resize((416,183))
        fig.figimage(im,xo=67,yo=26) #maybe i'll just resize image and reset origin lol
        self.axes.patch.set_alpha(0)
        
        #self.axes is of the class AxesSubplot.

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

class dht_plots(dht_plot_class):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        dht_plot_class.__init__(self, *args, **kwargs)
        main_timer.timeout.connect(self.update_figure)

    def update_figure(self):
        global isActive
        global queue
        global x
        global y
        global y2
        global max_values
        if isActive and queue:
            if len(x) > max_values:
                for i in range(0,(len(x)-max_values)):
                    del x[0]
                    del y[0]
                    del y2[0]
            x.append(int(queue[0][0]))
            y.append(float(queue[0][1]))
            y2.append(float(queue[0][2]))
            self.axes.cla()
            self.axes2.cla()
            self.axes.plot(x, y, 'b') #self.axes.plot(<list of x values>, <list of y values>, <formatting string>)
            # for more information on format strings: https://matplotlib.org/api/_as_gen/matplotlib.pyplot.plot.html
            self.axes2.plot(x, y2, 'r')#in order to add a new line to the same subplot, add another self.axes.plot() instance
            self.draw()
        else:
            pass

class herc_map(herc_map_class):

    def __init__(self, *args, **kwargs):
        herc_map_class.__init__(self, *args, **kwargs)
        main_timer.timeout.connect(self.update_figure)
        self.axes.patch.set_alpha(0)
        self.axes.set_xticks([])
        self.axes.set_yticks([])
        self.axes.set_xlim(left=-86.655442,right=-86.651886)
        self.axes.set_ylim(bottom=34.709939,top=34.711136)
        self.axes.set_title("U.S. Space & Rocket Center: NASA HERC Course 2019")

    def update_figure(self):
        global isActive
        global queue
        global x_map
        global y_map
        if isActive and queue:
            if len(x_map) == 1:
                del x_map[0]
                del y_map[0]
            if queue[0][9] != "NO_ENCODE":
                x_map.append(float(queue[0][10]))
                y_map.append(float(queue[0][9]))
            else:
                x_map.append(0)
                y_map.append(0)
            self.axes.cla() #clear current axes
            self.axes.plot(x_map, y_map, 'bo') #self.axes.plot(<list of x values>, <list of y values>, <formatting string>)
            self.axes.patch.set_alpha(0)
            self.axes.set_xticks([])
            self.axes.set_yticks([])
            self.axes.set_xlim(left=-86.655442,right=-86.651886)
            self.axes.set_ylim(bottom=34.709939,top=34.711136)
            self.axes.set_title("U.S. Space & Rocket Center: NASA HERC Course 2019")
            self.draw()
        else:
            pass


class ApplicationWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)

        self.groupBox.setEnabled(False)
        self.groupBox_3.setEnabled(False)
        self.groupBox_4.setEnabled(False)
        self.groupBox_5.setEnabled(False)

        self.widget = dht_plots(self.horizontalLayoutWidget)
        self.widget_3 = herc_map(self.horizontalLayoutWidget_3)

        self.pushButton.clicked.connect(self.open_herc_book)
        self.pushButton_2.clicked.connect(self.open_obstacle_table)
        self.pushButton_5.clicked.connect(self.toggle_reading)
        self.actionOpen_db.triggered.connect(self.open_file_dialog)
        self.actionAbout.triggered.connect(self.open_about_dialog)
        self.actionOpen_Obstacle_Task_Table.triggered.connect(self.open_obstacle_table)
        self.actionOpen_Guidebook.triggered.connect(self.open_herc_book)
        self.actionTelemetry_Guidebook.triggered.connect(self.open_guidebook)
        self.actionOpen_in_Google_Sheets.triggered.connect(self.open_data_sheet)
        self.actionChange_Read_Delay.triggered.connect(self.open_delay_window)
        self.actionChange_Max_Graph_Values.triggered.connect(self.open_value_window)

    #lol
    def open_herc_book(self):
        webbrowser.open("https://www.nasa.gov/sites/default/files/atoms/files/guide-human-exploration-rover-challenge-2019.pdf")
    def open_obstacle_table(self):
        webbrowser.open("https://docs.google.com/spreadsheets/d/14vqGlR-rk38IQtcsFvLhAfZBQCuorKXU-1DswQZSrjY/edit?usp=sharing")
    def open_data_sheet(self):
        webbrowser.open("https://docs.google.com/spreadsheets/d/1K_3HoLemrF0fYTmdT47LxnZcyGHhU7nC4pLsQebIU0s/edit?usp=sharing")
    def open_guidebook(self):
        webbrowser.open("https://docs.google.com/document/d/1xEh56nXU770y0y_1TPwB-EDTDZ-non385fOOhK12YIE/edit?usp=sharing")
    
    def toggle_reading(self):
        global isActive
        global main_timer
        global first
        global using_db
        global read_delay
        if not isActive:
            init_row = int(self.lineEdit.text())
            init_timeout = int(self.lineEdit_3.text())
            if not using_db:
                update_data(True,init_row,init_timeout)
            else:
                update_from_db(True,init_row,init_timeout)

            self.groupBox.setEnabled(True)
            self.groupBox_3.setEnabled(True)
            self.groupBox_4.setEnabled(True)
            self.groupBox_5.setEnabled(True)
            
            isActive = True

            if not first:
                main_timer.timeout.connect(self.update_alltext)
                first = True
            else:
                pass
            main_timer.start(read_delay)
            print(read_delay)
        else:
            reset_vars()
                    
            main_timer.stop()
            
            self.groupBox.setEnabled(False)
            self.groupBox_3.setEnabled(False)
            self.groupBox_4.setEnabled(False)
            self.groupBox_5.setEnabled(False)
            
            isActive = False

    def update_alltext(self):
        global using_db
        if not using_db:
            update_data()
        else:
            update_from_db()
        global starting_row
        global timeout
        global failed_attempts
        global heal_attempts
        global last_read
        global queue
        global queued_timestamps
        global timestamp_counts
        global last_read_timestamp
        global last_queued_timestamp
        global first_timestamp_read
        global first_read
        global last_queue
        global lag_time
        global halt
        global elapsed_section_time
        global current_section
        self.label_2.setText(str(last_read_timestamp))#current/last timestamp being read
        self.label_4.setText(str(lag_time)+"s")#lag time = current time - currently reading timestamp
        self.label_12.setText(str(len(queue)))#debug: len(queue)
        self.label_13.setText(str(last_read))#debug: last_read
        self.label_14.setText(str(failed_attempts))#debug: failed_attempts
        self.label_15.setText(str(heal_attempts))#debug: heal_attempts
        if queue:
            temp_f = str(round(((float(queue[0][2])*1.8)+32),2))#Convert C to F
            self.label_16.setText(str(queue[0][2])+"/"+temp_f)#Temperature
            self.label_18.setText(str(queue[0][1])+"%")#Humidity
            self.label_25.setText(str(queue[0][9]))#Latitude
            self.label_26.setText(str(queue[0][10]))#Longitude
            self.label_27.setText(str(queue[0][11]))#Speed
            self.label_28.setText(str(queue[0][12]))#Altitude
            self.label_29.setText(str(queue[0][13]))#Course
            self.label_47.setText(str(queue[0][3]))#Pitch
            self.label_48.setText(str(queue[0][4]))#Roll
            self.label_49.setText(str(queue[0][5]))#Yaw
            self.label_50.setText(str(queue[0][6]))#Pitch_avg_delta
            self.label_51.setText(str(queue[0][7]))#Roll_avg_delta
            self.label_52.setText(str(queue[0][8]))#Yaw_avg_delta
            #Other GPS data
            region_data = determine_region(queue[0][10],queue[0][9])
            if region_data[0] == current_section:
                elapsed_section_time += 1
            else:
                current_section = region_data[0]
                elapsed_section_time = 0
            section_minutes = elapsed_section_time // 60
            section_seconds = elapsed_section_time % 60
            self.label_34.setText("%01i:%02i"%(section_minutes,section_seconds))
            self.label_35.setText(region_data[0])
            self.label_32.setText(region_data[0])
            self.label_33.setText(region_data[1])
            self.label_36.setText(region_data[2])
            self.label_39.setText(region_data[3])
            self.label_40.setText(region_data[4])
            del queue[0]
        if halt:
            self.toggle_reading()
            halt = False
    def open_file_dialog(self):
        fileName = QFileDialog.getOpenFileName(self,"Open Database File", "","Database Files (*.db);;All Files (*);;")
        global db_target
        if fileName:
            db_target = fileName[0]
        else:
            return
        try:
            self.conf_dialog = ImportWindow()
            self.conf_dialog.show()
            self.conf_dialog.accepted.connect(self.start_db)
        except Exception as e:
            print(e)
    def start_db(self):
        global using_db
        if isActive:
            self.toggle_reading()
        using_db = True
        self.label_54.setText("(Database)")
    def open_about_dialog(self):
        self.about_dialog = AboutWindow()
        self.about_dialog.show()
    def open_delay_window(self):
        try:
            self.delay_dialog = ReadDelayWindow()
            self.delay_dialog.show()
        except Exception as e:
            print(e)
    def open_value_window(self):
        self.value_dialog = GraphValuesWindow()
        self.value_dialog.show()
        
class ImportWindow(QDialog):
    def __init__(self):
        super().__init__()
        global db_target
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.reject)#of course they're switched
        self.ui.pushButton_2.clicked.connect(self.accept)
        self.ui.label_2.setText(db_target)

class AboutWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog2()
        self.ui.setupUi(self)

class ReadDelayWindow(QDialog):
    def __init__(self):
        super().__init__()
        global read_delay
        self.ui = Ui_Dialog3()
        self.ui.setupUi(self)
        self.ui.lineEdit.setText(str(read_delay))
        self.ui.pushButton.clicked.connect(self.update_delay)#of course they're switched
    def update_delay(self):
        global read_delay
        new_delay = int(self.ui.lineEdit.text())
        if new_delay < 125:
            read_delay = 125
        else:
            read_delay = new_delay
        print(read_delay)
        if isActive:
            main_timer.start(read_delay)
        self.close()
        
class GraphValuesWindow(QDialog):
    def __init__(self):
        super().__init__()
        global max_values
        self.ui = Ui_Dialog4()
        self.ui.setupUi(self)
        self.ui.lineEdit.setText(str(max_values))
        self.ui.pushButton.clicked.connect(self.update_max)
    def update_max(self):
        global max_values
        max_values = int(self.ui.lineEdit.text())
        self.close()

class AppContext(ApplicationContext):           # 1. Subclass ApplicationContext
    def run(self):                              # 2. Implement run()
        aw = ApplicationWindow()
        aw.setWindowTitle("%s" % progname)
        aw.show()
        return self.app.exec_()                 # 3. End run() with this line

if __name__ == '__main__':
    appctxt = AppContext()                      # 4. Instantiate the subclass
    exit_code = appctxt.run()                   # 5. Invoke run()
    sys.exit(exit_code)
            
'''
qApp = QtWidgets.QApplication(sys.argv)

aw = ApplicationWindow()
aw.setWindowTitle("%s" % progname)
aw.show()
sys.exit(qApp.exec_())
'''
#qApp.exec_()
