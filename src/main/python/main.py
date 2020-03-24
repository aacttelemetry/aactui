#region modules/imports
from __future__ import unicode_literals
from fbs_runtime.application_context.PyQt5 import ApplicationContext
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
import socket
import webbrowser
import ast
import math
from datetime import datetime
from PIL import Image
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog, QDialog, QMainWindow
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
#-----------#
from new2020 import Ui_MainWindow
#endregion

#region variables
#contains socket object
s = None

#for the data graphs
x = []
temp_plot_values = []
humidity_plot_values = []
heartrate_plot_values = []
heartrate_plot_historical = []
last_valid_hr = 70

#for the gps map
x_map = [] 
y_map = []

#is the whole thing active? (should things be faded out to let the user know data isn't being pulled from somewhere?)
isActive = False
using_db = False #using the database?
db_target = '' #database path

#replace where necessary
data_source = "Nothing"

main_timer = QtCore.QTimer() #main timer running all updates
first = False
halt = False

max_values = 10000 #number of max values on data graphs
read_delay = 1000 #delay between each update

current_section = '' #competition section
elapsed_section_time = 0 #elapsed time, in seconds, that the section hasn't changed

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
#endregion

#region global functions
def socket_connect():
    global s
    global main_timer
    global data_source
    pi_ip = '192.168.1.85'
    port = 12348
    try:
        s = socket.socket()          
        s.connect((pi_ip, port))
        data_source = "Socket"
    except ConnectionRefusedError:
        print("Port hasn't reset yet or the script isn't running. Try again.")
    except Exception as e:
        print(e)

def get_data_sockets():
    global s
    global main_timer
    global queue
    global last_queued_timestamp
    global data_source
    global first
    #the data-fixing aspects of the db and gsheet functions are not implemented here, as there has yet to be such an issue.
    try:
        received = (s.recv(1024).decode("utf-8"))
        print(received)
        #it seems initial data is screwed up, will need the healing functions eventually
        new = received.split("|")
        if len(new) > 2:
            pass
        else:
            temp_list = ast.literal_eval(new[0])
            last_queued_timestamp = temp_list["timestamp"]
            queue.append(temp_list)
        
        if len(new) == 0:
            print("Connection seems to have been dropped; halting.")
            if s != None:
                main_timer.stop()
                s.close()
                s = None
                data_source = "Nothing"
    except Exception as e:
        print(e)
        main_timer.stop()
        s.close()
        s = None
        data_source = "Nothing"

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

def update_data_db(initial=False,initial_row=2,initial_timeout=10):
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

def update_data_gsheets(initial=False,initial_row=2,initial_timeout=10):
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
#endregion

#region classes for plots (qwidgets)
class data_plot_class(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=4.11, height=3.79, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes1 = fig.add_subplot(311) #1x1 grid, position 1;see https://stackoverflow.com/questions/3584805/in-matplotlib-what-does-the-argument-mean-in-fig-add-subplot111
        self.axes2 = fig.add_subplot(312) 
        self.axes3 = fig.add_subplot(313) #1x1 grid, position 1;see https://stackoverflow.com/questions/3584805/in-matplotlib-what-does-the-argument-mean-in-fig-add-subplot111
        self.axes1.get_xaxis().set_visible(False)
        self.axes2.get_xaxis().set_visible(False)
        self.axes3.get_xaxis().set_visible(False)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

class data_plots(data_plot_class):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        data_plot_class.__init__(self, *args, **kwargs)
        main_timer.timeout.connect(self.update_figure)

    def update_figure(self):
        global data_source
        global queue
        global x
        global humidity_plot_values
        global temp_plot_values
        global heartrate_plot_values
        global heartrate_plot_historical
        global max_values
        global last_valid_hr
        if data_source != "Nothing" and queue:
            if len(x) > max_values:
                for i in range(0,(len(x)-max_values)):
                    del x[0]
                    del humidity_plot_values[0]
                    del temp_plot_values[0]
                    del heartrate_plot_values[0]
            x.append(int(queue[0]["timestamp"]))
            temp_plot_values.append(float(queue[0]["sensor_data"][1]))
            humidity_plot_values.append(float(queue[0]["sensor_data"][0]))
            heartrate = float(queue[0]["fitbit_data"][0])

            self.axes1.cla()
            self.axes2.cla()
            self.axes3.cla()
            self.axes1.plot(x, temp_plot_values, 'r') #self.axes.plot(<list of x values>, <list of y values>, <formatting string>)
            self.axes2.plot(x, humidity_plot_values, 'b')
            if heartrate == 0:
                heartrate_plot_values.append(last_valid_hr)
                self.axes3.plot(x, heartrate_plot_values, 'm--')
            else:
                heartrate_plot_values.append(heartrate)
                heartrate_plot_historical.append(heartrate)
                self.axes3.plot(x, heartrate_plot_values, 'm')
                last_valid_hr = heartrate
            self.draw()
        else:
            pass

class heartrate_histogram_class(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=3.21, height=2.21, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes1 = fig.add_subplot(111) #1x1 grid, position 1;see https://stackoverflow.com/questions/3584805/in-matplotlib-what-does-the-argument-mean-in-fig-add-subplot111

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

class histogram_plot(heartrate_histogram_class):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        heartrate_histogram_class.__init__(self, *args, **kwargs)
        main_timer.timeout.connect(self.update_figure)

    def update_figure(self):
        global data_source
        global queue
        global heartrate_plot_historical
        if data_source != "Nothing" and queue:
            self.axes1.cla()
            self.axes1.hist(heartrate_plot_historical,bins=20)
            self.draw()
        else:
            pass
#endregion

#region main window stuff
class ApplicationWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        
        self.widget_2 = data_plots(self.widget_2)
        self.widget_6 = histogram_plot(self.widget_6)

        self.pushButton.clicked.connect(self.start_reading)

        main_timer.timeout.connect(self.update_data)
        #https://eli.thegreenplace.net/2011/04/25/passing-extra-arguments-to-pyqt-slot
        #self.pushButton.clicked.connect(lambda: self.add_msg("a"))
        
    #def add_msg(self,msg):
        #self.textEdit.append(time.strftime('%m/%d/%y %H:%M:%S - ')+msg)
    def start_reading(self):
        global main_timer
        socket_connect()
        main_timer.start(1000)
        
    def update_data(self):
        global s
        global last_queued_timestamp
        global queue
        global data_source
        if data_source == "Socket" and s != None:
            get_data_sockets()
        if len(queue) > 1:
        #... all text label updates go here     
        # {"timestamp":<timestamp>,
        # "fitbit_data":[<heartrate>,<pressure>],
        # "sensor_data":[<humidity[0], temperature[1], pitch[2], roll[3], yaw[4], total x[5], total y[6], total vector count[7],this read vector count[8], internal length constant[9], latitude[10], longitude[11], hdop[12], satellite count[13]>]}
        # 
            #all tab 1/global labels
            self.global_source_label.setText(data_source)
            self.global_cvtime_label.setText(datetime.fromtimestamp(queue[0]["timestamp"]).strftime('%m/%d/%y %H:%M:%S'))
            self.reading_label.setText(str(queue[0]["timestamp"]))
            lag_time = str(math.floor(time.time())-queue[0]["timestamp"])+"s"
            self.lag_time_label.setText(lag_time)
            self.global_lag_label.setText(lag_time)
            self.queue_size_label.setText(str(len(queue)))
            self.last_read_label.setText("ts:"+str(last_queued_timestamp))
            self.failed_attempts_label.setText(str(failed_attempts))
            self.heal_attempts_label.setText(str(heal_attempts))
            #tab 3 labels (non-course)
            self.latitude_label.setText(queue[0]["sensor_data"][10])
            self.longitude_label.setText(queue[0]["sensor_data"][11])
            self.altitude_label.setText("unimplemented") ####implement barometric formula
            self.pressure_label.setText(queue[0]["fitbit_data"][1])
            self.delta_x_label.setText(queue[0]["sensor_data"][5])
            self.delta_y_label.setText(queue[0]["sensor_data"][6])
            self.resultant_label.setText("unimplemented")
            self.hdop_label.setText(queue[0]["sensor_data"][12])
            self.satellite_label.setText(queue[0]["sensor_data"][13])
            self.total_vectors_label.setText(queue[0]["sensor_data"][7])
            self.this_read_vectors_label.setText(queue[0]["sensor_data"][8])
            self.instantaneous_speed_label.setText("unimplemented")
            self.moving_average_speed_label.setText("unimplemented")
            self.pitch_label.setText(queue[0]["sensor_data"][2])
            self.roll_label.setText(queue[0]["sensor_data"][3])
            self.yaw_label.setText(queue[0]["sensor_data"][4])
            if(queue[0]["sensor_data"][7] != "--"):
                self.total_distance_label.setText(str(int(queue[0]["sensor_data"][7])*float(queue[0]["sensor_data"][9]))+"units")
                self.this_read_distance_label.setText(str(int(queue[0]["sensor_data"][8])*float(queue[0]["sensor_data"][9]))+"units")
            else:
                self.total_distance_label.setText("--")
                self.this_read_distance_label.setText("--")
            #tab 3 labels (course)
                #unimplemented
            #tab 4 labels
            self.temperature_label.setText(queue[0]["sensor_data"][1])
            self.humiditity_label.setText(queue[0]["sensor_data"][0])
            if queue[0]["fitbit_data"][0] != "0":
                self.body_presence_label.setText("Body currently present on Fitbit.")
                self.bpm_label.setText(queue[0]["fitbit_data"][0])
            else:
                self.body_presence_label.setText("Body is not currently present on Fitbit.")
                self.bpm_label.setText("--")
            del queue[0]
        else:
            pass
            #main_timer.stop()
#endregion

#region other dialogues
#endregion
try:
#region execution
    class AppContext(ApplicationContext):           # 1. Subclass ApplicationContext
        def run(self):                              # 2. Implement run()
            aw = ApplicationWindow()
            aw.setWindowTitle("AACT Telemetry UI")
            aw.show()
            return self.app.exec_()                 # 3. End run() with this line

    if __name__ == '__main__':
        appctxt = AppContext()                      # 4. Instantiate the subclass
        exit_code = appctxt.run()                   # 5. Invoke run()
        sys.exit(exit_code)
except Exception as e:
    print(e)
#endregion