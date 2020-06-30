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
import logging #logging.debug/info/warning/error("str")
from datetime import datetime
from PIL import Image
from PyQt5 import QtCore, QtWidgets, QtGui
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
#-----------#
from new2020 import Ui_MainWindow
from testwindow import Ui_MainWindow2
from testdialog import Ui_Dialog
#endregion

#region variables
class global_states:
    #handling:
    starting_row = 2
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
    last_queue = [] #Last successfully printed set of data. Used in the event missing data occurs, in which case the client will replace it with these last known values.
    lag_time = 0

    #constants:
    max_values = 10000 #number of max values on data graphs
    read_delay = 1000 #delay between each update
    timeout = 10 #max failed reads before stopping

    #internal:
    isActive = False #is the whole thing active? (should things be faded out to let the user know data isn't being pulled from somewhere?)
    usingdb = False #using the database? consider deprecating in favor of using an int with data source
    db_target = '' #database path
    data_source = "Nothing" #string representing current data source; consider using an int instead of string
    socket_object = None
    main_timer = QtCore.QTimer() #main timer running all updates
    first = False #is first read?
    halt = False #i assume somewhere there's supposed to be a check that says "if halt = true, do something" but this technically does anything right now lol
    
    #data_graphs:
    x_data = [] #x axis, timestamps
    temp_values = []
    humidity_values = []
    heartrate_values = []
    heartrate_historical = []
    last_valid_hr = 70 #default heartrate is assumed to be 70
    
    #gps map
    #positioning_graphs:
    x_pos = []
    y_pos = []

    #competition
    current_section = '' #competition section
    elapsed_section_time = 0 #elapsed time, in seconds, that the section hasn't changed


    def reset_vars(self):
        #lmao
        self.starting_row = 2
        self.failed_attempts = 0 # The amount of times the client has found no new data.
        self.heal_attempts = 0 #Amount of times healing has occurred in a row.
        self.last_read = self.starting_row # Last read row; used to determine read_range. (Can't be used to compare against timestamp because of inconsistencies)
        self.queue = [] # Queued data to print, given that its timestamp is unique.
        self.queued_timestamps = [] # All timestamps.
        self.timestamp_counts = {} # Amount of time each timestamp appears.
        self.last_read_timestamp = 0 # Last timestamp read. If a timestamp is missing, the user is notified. (queue)
        self.last_queued_timestamp = 0 # Last non-duplicate timestamp read.
        self.first_timestamp_read = "" # Holds the very first timestamp set read, which often causes issues.
        self.first_read = False # Boolean of "is this the actual first read?"
        self.last_queue = [] #Last successfully printed set of data. Used in the event missing data occurs, in which case the client will replace it with these last known values.
        self.lag_time = 0
        self.max_values = 10000 #number of max values on data graphs
        self.read_delay = 1000 #delay between each update
        self.timeout = 10 #max failed reads before stopping
        self.isActive = False #is the whole thing active? (should things be faded out to let the user know data isn't being pulled from somewhere?)
        self.usingdb = False #using the database? consider deprecating in favor of using an int with data source
        self.db_target = '' #database path
        self.data_source = "Nothing" #string representing current data source; consider using an int instead of string
        self.socket_object = None
        self.main_timer = QtCore.QTimer() #main timer running all updates
        self.first = False #is first read?
        self.halt = False #i assume somewhere there's supposed to be a check that says "if halt = true, do something" but this technically does anything right now lol
        self.x_data = [] #x axis, timestamps
        self.temp_values = []
        self.humidity_values = []
        self.heartrate_values = []
        self.heartrate_historical = []
        self.last_valid_hr = 70 #default heartrate is assumed to be 70
        self.x_pos = []
        self.y_pos = []
        self.current_section = '' #competition section
        self.elapsed_section_time = 0 #elapsed time, in seconds, that the section hasn't changed

class global_constants:
    #implement gsheets and external database stuff here
    pass

#endregion

#region global functions
def socket_connect(pi_ip='192.168.1.85', port=12348):
    try:
        global_states.socket_object = socket.socket()          
        global_states.socket_object.connect((pi_ip, port))
        global_states.data_source = "Socket"
        global_states.socket_object.settimeout(5) #socket blocks for five seconds before giving up
    except ConnectionRefusedError:
        logging.error("Port hasn't reset yet or the script isn't running. Try again. (ConnectionRefusedError)")
    except Exception as e:
        logging.error(e)

def get_data_sockets():
    #the data-fixing aspects of the db and gsheet functions are not implemented here, as there has yet to be such an issue.
    try:
        received = (global_states.socket_object.recv(1024).decode("utf-8"))
        logging.debug(received)
        #it seems initial data is screwed up, will need the healing functions eventually
        new = received.split("|")
        if len(new) > 2:
            pass
        else:
            temp_list = ast.literal_eval(new[0])
            global_states.last_queued_timestamp = temp_list["timestamp"]
            global_states.queue.append(temp_list)
        
        if len(new) == 0:
            logging.error("Connection seems to have been dropped; halting.")
            if global_states.socket_object != None:
                global_states.main_timer.stop()
                global_states.socket_object.close()
                global_states.socket_object = None
                global_states.data_source = "Nothing"
    except Exception as e:
        logging.error(e)
        global_states.main_timer.stop()
        global_states.socket_object.close()
        global_states.socket_object = None
        global_states.data_source = "Nothing"

def update_data_db(initial=False,initial_row=2,initial_timeout=10):
    if initial:
        global_states.last_read = initial_row
        global_states.timeout = initial_timeout
    else:
        pass
    if len(global_states.queue) < 4 and initial:
        conn = sqlite3.connect(global_states.db_target)
        c = conn.cursor()
        c.execute('SELECT * FROM data')
        initial = c.fetchall()
        response = []
        for i in initial:
            response.append(list(i))
        for i in range(0,global_states.last_read):
            del response[0]
        if len(response) == 2:
            global_states.failed_attempts += 1
            if global_states.failed_attempts >= global_states.timeout:
                logging.info('Timeout limit reached. Ending data read.')
                global_states.halt = True
                return
            else:
                logging.info('No new data found. Retrying %s more time(s).'%(global_states.timeout-global_states.failed_attempts))
        else:
            global_states.first_timestamp_read = response[0][0]
            for i in response: #Perform initial pass. Returns all unique and duplicated timestamps to global_states.queued_timestamps.
                global_states.queued_timestamps.append(i[0])
            global_states.timestamp_counts = Counter(global_states.queued_timestamps)
            for i in response: #Perform second pass.
                if global_states.timestamp_counts[i[0]] > 1: # if this timestamp has duplicates:
                    if global_states.first_timestamp_read == i[0] and not global_states.first_read: # if it's the very global_states.first timestamp, and this is the actual global_states.first set:
                        i = response[(global_states.timestamp_counts[i[0]])-1] # set it to be the value of the last duplicated timestamp
                        global_states.queue.append(i)
                        global_states.last_queued_timestamp = int(i[0])
                        global_states.first_read = True
                    elif global_states.first_timestamp_read == i[0]:
                        pass # ignore if it's part of the global_states.first timestamp read
                    else:
                        logging.info('Duplicate found. Reading as %s.'%(global_states.last_queued_timestamp + 1)) # if it's a regular duplicate, use it as the successive value to the last timestamp
                        i[0] = str(global_states.last_queued_timestamp + 1)
                        global_states.last_queued_timestamp = int(i[0])
                        global_states.queue.append(i)
                else:
                    global_states.queue.append(i)
                    global_states.last_queued_timestamp = int(i[0])
            global_states.first_read = True #In case there wasn't a duplicate, so this won't be triggered next round.
            global_states.last_read += len(response)
            global_states.failed_attempts = 0
    elif len(global_states.queue) < 1 and not initial:
        global_states.halt = True
    if len(global_states.queue) > 0:
        if int(global_states.queue[0][0]) - global_states.last_read_timestamp > 1 and global_states.last_read_timestamp != 0:
            logging.info('attempting to heal data after timestamp %s'%global_states.last_read_timestamp) # if data is missing, replace it with the last known values. this should never occur for more than one or two readings.
            heal_attempt = global_states.last_queue
            heal_attempt[0] = str(global_states.last_read_timestamp + 1)
            global_states.queue.insert(0,heal_attempt)
            global_states.heal_attempts += 1
            if global_states.heal_attempts > global_states.timeout:
                logging.info('Detected too large of a gap between values. Ending script.')
                global_states.halt = True
                return
        else:
            global_states.heal_attempts = 0
        global_states.last_read_timestamp = int(global_states.queue[0][0])
        global_states.last_queue = global_states.queue[0]
        global_states.lag_time = int(time.time())-global_states.last_read_timestamp

def update_data_gsheets(initial=False,initial_row=2,initial_timeout=10):
    if initial:
        global_states.last_read = initial_row
        global_states.timeout = initial_timeout
    else:
        pass
    if len(global_states.queue) < 4: #Only attempt to read new data if there are less than four seconds of data remaining. 
        read_range = ("Data!A%s:N"%global_states.last_read)
        request = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=read_range, valueRenderOption=value_render_option, dateTimeRenderOption=date_time_render_option)
        response = request.execute()
        if len(response) == 2:
            global_states.failed_attempts += 1
            if global_states.failed_attempts >= global_states.timeout:
                logging.info('Timeout limit reached. Ending data read.')
                global_states.halt = True
                return
            else:
                logging.info('No new data found. Retrying %s more time(s).'%(global_states.timeout-global_states.failed_attempts))
        else:
            global_states.first_timestamp_read = response['values'][0][0]
            for i in response['values']: #Perform initial pass. Returns all unique and duplicated timestamps to global_states.queued_timestamps.
                global_states.queued_timestamps.append(i[0])
            global_states.timestamp_counts = Counter(global_states.queued_timestamps)
            for i in response['values']: #Perform second pass.
                if global_states.timestamp_counts[i[0]] > 1: # if this timestamp has duplicates:
                    if global_states.first_timestamp_read == i[0] and not global_states.first_read: # if it's the very global_states.first timestamp, and this is the actual global_states.first set:
                        i = response['values'][(global_states.timestamp_counts[i[0]])-1] # set it to be the value of the last duplicated timestamp
                        global_states.queue.append(i)
                        global_states.last_queued_timestamp = int(i[0])
                        global_states.first_read = True
                    elif global_states.first_timestamp_read == i[0]:
                        pass # ignore if it's part of the global_states.first timestamp read
                    else:
                        logging.info('Duplicate found. Reading as %s.'%(global_states.last_queued_timestamp + 1)) # if it's a regular duplicate, use it as the successive value to the last timestamp
                        i[0] = str(global_states.last_queued_timestamp + 1)
                        global_states.last_queued_timestamp = int(i[0])
                        global_states.queue.append(i)
                else:
                    global_states.queue.append(i)
                    global_states.last_queued_timestamp = int(i[0])
            global_states.first_read = True #In case there wasn't a duplicate, so this won't be triggered next round.
            global_states.last_read += len(response['values'])
            global_states.failed_attempts = 0
    if len(global_states.queue) > 0:
        if int(global_states.queue[0][0]) - global_states.last_read_timestamp > 1 and global_states.last_read_timestamp != 0:
            logging.info('attempting to heal data after timestamp %s'%global_states.last_read_timestamp) # if data is missing, replace it with the last known values. this should never occur for more than one or two readings.
            heal_attempt = global_states.last_queue
            heal_attempt[0] = str(global_states.last_read_timestamp + 1)
            global_states.queue.insert(0,heal_attempt)
            global_states.heal_attempts += 1
            if global_states.heal_attempts > global_states.timeout:
                logging.info('Detected too large of a gap between values. Ending script.')
                global_states.halt = True
                return
        else:
            global_states.heal_attempts = 0
        global_states.last_read_timestamp = int(global_states.queue[0][0])
        global_states.last_queue = global_states.queue[0]
        global_states.lag_time = int(time.time())-global_states.last_read_timestamp
#endregion

#region classes for plots (qwidgets)
class QTextEditLogger(logging.Handler): #logging as per https://stackoverflow.com/questions/28655198/best-way-to-display-logs-in-pyqt
    def __init__(self, parent):
        super().__init__()
        self.widget = QtWidgets.QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)

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
        global_states.main_timer.timeout.connect(self.update_figure)

    def update_figure(self):
        if global_states.data_source != "Nothing" and global_states.queue:
            if len(global_states.x_data) > global_states.max_values:
                for i in range(0,(len(global_states.x_data)-global_states.max_values)):
                    del global_states.x_data[0]
                    del global_states.humidity_values[0]
                    del global_states.temp_values[0]
                    del global_states.heartrate_values[0]
            global_states.x_data.append(int(global_states.queue[0]["timestamp"]))
            global_states.temp_values.append(float(global_states.queue[0]["sensor_data"][1]))
            global_states.humidity_values.append(float(global_states.queue[0]["sensor_data"][0]))
            heartrate = float(global_states.queue[0]["fitbit_data"][0])

            self.axes1.cla()
            self.axes2.cla()
            self.axes3.cla()
            self.axes1.plot(global_states.x_data, global_states.temp_values, 'r') #self.axes.plot(<list of global_states.x_data values>, <list of y values>, <formatting string>)
            self.axes2.plot(global_states.x_data, global_states.humidity_values, 'b')
            if heartrate == 0:
                global_states.heartrate_values.append(global_states.last_valid_hr)
                self.axes3.plot(global_states.x_data, global_states.heartrate_values, 'm--')
            else:
                global_states.heartrate_values.append(heartrate)
                global_states.heartrate_historical.append(heartrate)
                self.axes3.plot(global_states.x_data, global_states.heartrate_values, 'm')
                global_states.last_valid_hr = heartrate
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
        global_states.main_timer.timeout.connect(self.update_figure)

    def update_figure(self):
        if global_states.data_source != "Nothing" and global_states.queue:
            self.axes1.cla()
            self.axes1.hist(global_states.heartrate_historical,bins=20)
            self.draw()
        else:
            pass
#endregion

#region main window stuff
class ApplicationWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        
        #logging as referenced above
        self.logboxwidget = QTextEditLogger(self)
        self.logboxwidget.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(self.logboxwidget)
        #logging level is set below
        logging.getLogger().setLevel(logging.DEBUG)
        self.verticalLayout_4.addWidget(self.logboxwidget.widget)

        self.widget_2 = data_plots(self.widget_2)
        self.widget_6 = histogram_plot(self.widget_6)


        #event handlers
        #tab 1
        self.connect_raspi_button.clicked.connect(self.start_reading)
        
        #tab 2

        #tab 3
        self.open_obstacles_button.clicked.connect(self.open_obstacle_table)
        self.open_guidebook_button.clicked.connect(self.open_herc_book)

        #tab 5
        self.open_github_button.clicked.connect(self.open_github)
        self.open_report_button.clicked.connect(self.open_report)
        self.open_website_button.clicked.connect(self.open_website)
        self.open_data_button.clicked.connect(self.open_data_spreadsheet)

        #top menu bar
        self.actionChange_Graph_Size.triggered.connect(self.open_graph_size_dialog)
        self.actionChange_Read_Rate.triggered.connect(self.open_read_delay_dialog)
        self.actionHERC_Guidebook.triggered.connect(self.open_graph_size_dialog)
        self.actionObstacle_Task_Table.triggered.connect(self.open_herc_book)
        self.actionGithub.triggered.connect(self.open_github)
        self.actionWebsite.triggered.connect(self.open_website)
        self.actionReport.triggered.connect(self.open_report)
        self.actionAbout.triggered.connect(self.open_about_dialog)

        global_states.main_timer.timeout.connect(self.update_data)
        #https://eli.thegreenplace.net/2011/04/25/passing-extra-arguments-to-pyqt-slot
        #self.pushButton.clicked.connect(lambda: self.add_msg("a"))

        self.pushButton_11.clicked.connect(self.open_stream_window)        
        self.find_row_button.clicked.connect(self.open_dialog_window)
    def open_dialog_window(self):
        self.new_dialog = Test_Dialog()
        self.new_dialog.show()
    def open_stream_window(self):
        self.about_dialog = StreamWindow()
        self.about_dialog.show()

    def start_reading(self):
        socket_connect()
        global_states.main_timer.start(1000)
        
    def update_data(self):
        if global_states.data_source == "Socket" and global_states.socket_object != None:
            get_data_sockets()
        if len(global_states.queue) > 1:
        #... all text label updates go here     
        # {"timestamp":<timestamp>,
        # "fitbit_data":[<heartrate>,<pressure>],
        # "sensor_data":[<humidity[0], temperature[1], pitch[2], roll[3], yaw[4], total global_states.x_data[5], total y[6], total vector count[7],this read vector count[8], internal length constant[9], latitude[10], longitude[11], hdop[12], satellite count[13]>]}
        # 
            #all tab 1/global labels
            self.global_source_label.setText(global_states.data_source)
            self.global_cvtime_label.setText(datetime.fromtimestamp(global_states.queue[0]["timestamp"]).strftime('%m/%d/%y %H:%M:%S'))
            self.reading_label.setText(str(global_states.queue[0]["timestamp"]))
            global_states.lag_time = str(math.floor(time.time())-global_states.queue[0]["timestamp"])+"s"
            self.lag_time_label.setText(global_states.lag_time)
            self.global_lag_label.setText(global_states.lag_time)
            self.queue_size_label.setText(str(len(global_states.queue)))
            self.last_read_label.setText("ts:"+str(global_states.last_queued_timestamp))
            self.failed_attempts_label.setText(str(global_states.failed_attempts))
            self.heal_attempts_label.setText(str(global_states.heal_attempts))
            #tab 3 labels (non-course)
            self.latitude_label.setText(global_states.queue[0]["sensor_data"][10])
            self.longitude_label.setText(global_states.queue[0]["sensor_data"][11])
            self.altitude_label.setText("unimplemented") ####implement barometric formula
            self.pressure_label.setText(global_states.queue[0]["fitbit_data"][1])
            self.delta_x_label.setText(global_states.queue[0]["sensor_data"][5])
            self.delta_y_label.setText(global_states.queue[0]["sensor_data"][6])
            self.resultant_label.setText("unimplemented")
            self.hdop_label.setText(global_states.queue[0]["sensor_data"][12])
            self.satellite_label.setText(global_states.queue[0]["sensor_data"][13])
            self.total_vectors_label.setText(global_states.queue[0]["sensor_data"][7])
            self.this_read_vectors_label.setText(global_states.queue[0]["sensor_data"][8])
            self.instantaneous_speed_label.setText("unimplemented")
            self.moving_average_speed_label.setText("unimplemented")
            self.pitch_label.setText(global_states.queue[0]["sensor_data"][2])
            self.roll_label.setText(global_states.queue[0]["sensor_data"][3])
            self.yaw_label.setText(global_states.queue[0]["sensor_data"][4])
            if(global_states.queue[0]["sensor_data"][7] != "--"):
                self.total_distance_label.setText(str(int(global_states.queue[0]["sensor_data"][7])*float(global_states.queue[0]["sensor_data"][9]))+"units")
                self.this_read_distance_label.setText(str(int(global_states.queue[0]["sensor_data"][8])*float(global_states.queue[0]["sensor_data"][9]))+"units")
            else:
                self.total_distance_label.setText("--")
                self.this_read_distance_label.setText("--")
            #tab 3 labels (course)
                #unimplemented
            #tab 4 labels
            self.temperature_label.setText(global_states.queue[0]["sensor_data"][1])
            self.humiditity_label.setText(global_states.queue[0]["sensor_data"][0])
            if global_states.queue[0]["fitbit_data"][0] != "0":
                self.body_presence_label.setText("Body currently present on Fitbit.")
                self.bpm_label.setText(global_states.queue[0]["fitbit_data"][0])
            else:
                self.body_presence_label.setText("Body is not currently present on Fitbit.")
                self.bpm_label.setText("--")
            del global_states.queue[0]
        else:
            pass
            #global_states.main_timer.stop()
    #hmmm
    def open_herc_book(self):
        webbrowser.open("https://www.nasa.gov/sites/default/files/atoms/files/edu_herc-guidebook_2020v2.pdf")
    def open_obstacle_table(self):
        webbrowser.open("https://docs.google.com/spreadsheets/d/14vqGlR-rk38IQtcsFvLhAfZBQCuorKXU-1DswQZSrjY/edit?usp=sharing")
    def open_github(self):
        webbrowser.open("https://github.com/aacttelemetry")
    def open_website(self):
        webbrowser.open("https://aacttelemetry.github.io/index.html")
    def open_report(self):
        webbrowser.open("https://drive.google.com/open?id=1vNWtVX-0AonVTZm8llp3Dfd-jVqxUuPi")
    def open_data_spreadsheet(self):
        pass
        #webbrowser.open("")
    def find_equivalent_row(self):
        pass
    def open_stream_overlay(self):
        pass
    def open_db_file_dialog(self):
        pass
    def open_about_dialog(self):
        pass
    def open_graph_size_dialog(self):
        pass
    def open_read_delay_dialog(self):
        pass

#endregion

#region other dialogues
#
class StreamWindow(QtWidgets.QMainWindow,Ui_MainWindow2):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow2()
        self.ui.setupUi(self)

class Test_Dialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        global_states.main_timer.timeout.connect(self.update_data)
    def update_data(self):
        self.ui.label.setText(str(global_states.last_queued_timestamp))
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