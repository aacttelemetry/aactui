#region modules/init
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
import random
import logging #logging.debug/info/warning/error/critical("str")
import json
from datetime import datetime
from PIL import Image
from PyQt5 import QtCore, QtWidgets, QtGui, QtWebSockets, QtNetwork
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
#-----------#
import herctools
from new2020 import Ui_MainWindow
from streamoverlay import Ui_OverlayWindow
from preferences import Ui_PreferencesWindow
#-----------#
#get paths and initiate logging
#auto-save to file using basicConfig
#see https://stackoverflow.com/questions/6386698/how-to-write-to-a-file-using-the-logging-python-module
appctxt = ApplicationContext()
logpath = appctxt.get_resource('log.txt')#gets relative/absolute path through fbs
#set log via preferences?
logging.basicConfig(filename=logpath,format='%(asctime)s - %(levelname)s - %(message)s',level=logging.DEBUG)
prefpath = appctxt.get_resource('preferences.json')

#ignore matplotlib's findfont and filling up log.txt
#consider use of preferences file to set this internally later
#changed from setting the entire matplotlib to info or greater to https://stackoverflow.com/questions/56618739/matplotlib-throws-warning-message-because-of-findfont-python
logging.getLogger('matplotlib.font_manager').disabled = True
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
    websocket_object = None
    main_timer = QtCore.QTimer() #main timer running all updates
    first = False #is first read?
    halt = False #i assume somewhere there's supposed to be a check that says "if halt = true, do something" but this technically does anything right now lol
    
    #data_graphs:
    x_data = [] #x axis, timestamps
    temp_values = []
    humidity_values = []
    heartrate_values = []
    heartrate_historical = []
    
    #gps map
    #positioning_graphs:
    x_pos = []
    y_pos = []

    #competition
    current_section = '' #competition section
    elapsed_section_time = 0 #elapsed time, in seconds, that the section hasn't changed

    #debug
    longitude_offset = 0
    latitude_offset = 0

    def reset_vars(self): #reset to initial states
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
        self.websocket_object = None
        self.first = False #is first read?
        self.halt = False #i assume somewhere there's supposed to be a check that says "if halt = true, do something" but this technically does anything right now lol
        self.x_data = [] #x axis, timestamps
        self.temp_values = []
        self.humidity_values = []
        self.heartrate_values = []
        self.heartrate_historical = []
        self.x_pos = []
        self.y_pos = []
        self.current_section = '' #competition section
        self.elapsed_section_time = 0 #elapsed time, in seconds, that the section hasn't changed
        self.longitude_offset = 0
        self.latitude_offset = 0

class global_constants:
    gsheets_service = None
    spreadsheet_id = ""
    value_render_option = "FORMATTED_VALUE"
    date_time_render_option = "FORMATTED_STRING"

    #implement gsheets and external database stuff here
    pass

#endregion

#region global data functions
class WebsocketClient(QtCore.QObject):
    def __init__(self, parent, ip, port):
        super().__init__(parent)

        self.client =  QtWebSockets.QWebSocket("",QtWebSockets.QWebSocketProtocol.Version13,None)
        self.client.error.connect(self.error)

        #I don't understand why, but this doesn't work if we connect to echo.websocket.org (the standalone version of this script does, however.)
        #works otherwise though

        self.client.open(QtCore.QUrl("ws://%s:%s"%(ip,port)))
        #self.client.open(QtCore.QUrl("ws://echo.websocket.org"))
        self.client.pong.connect(self.onPong)
        #on a successful connection, immediately send the identification message
        self.client.updating.connect(self.send_init_message)

        self.client.textMessageReceived.connect(self.message_received)

    def do_ping(self):
        logging.info("client: do_ping")
        #self.client.ping(b"foo")
        self.client.ping()

    def send_init_message(self):
        logging.info("Sending identifying message.")
        self.client.sendTextMessage("ui")

    def onPong(self, elapsedTime, payload):
        logging.info("onPong - time: {} ; payload: {}".format(elapsedTime, payload))

    def error(self, error_code):
        logging.error("error code: {}".format(error_code))
        logging.error(self.client.errorString())
        #consider force-closing/set global_state to none, etc.a

    def close(self):
        self.client.close()

    def message_received(self, message):
        logging.debug(message)
        global_states.queue.append(ast.literal_eval(message))

def get_prefs():
    pref_file = open(prefpath) 
    data = json.load(pref_file)
    pref_file.close()
    return data

def write_prefs(data):
    pref_file = open(prefpath, "w+") #write and truncate
    pref_file.write(json.dumps(data,indent=4)) #reduces compression for the sake of readability
    pref_file.close()  

def generate_random_data():
    #does not actually do the calculations for vector math, should be fixed later
    #also does not cap values such as humidity at 0/100 or exhibit asymptotic behavior

    #{"timestamp":<timestamp>,
    # "fitbit_data":[<heartrate>,<pressure>],
    # "sensor_data":[<humidity[0], temperature[1], pitch[2], roll[3], yaw[4], total x[5], total y[6], total vector count[7],this read vector count[8], internal length constant[9], latitude[10], longitude[11], hdop[12], satellite count[13]>]}
    #
    def rval(min, max, places=2): #generate a random number with n decimal places, 2 default
        return random.randint(min*(10**places),max*(10**places))/(10**places)
    #if global_states.halt:
        #break
    if not global_states.queue: #if first run: generate reasonable (random) starting values
        init_fitbit = ["70","100000"]
        init_sensor = ["50.00","15.00","0","0","0","0","0","0","0","0.18","0","0","0","3"]
        full = {"timestamp":math.floor(time.time()),"fitbit_data":init_fitbit,"sensor_data":init_sensor}
        global_states.queue.append(full)
    else: #for successive runs: make slight changes (and do some magic inefficient conversions)
        current = global_states.queue[0]
        init_fitbit = [float(i) for i in current["fitbit_data"]]
        init_sensor = [float(i) for i in current["sensor_data"]]
        #warning: does not prevent values from going to very dumb places if unlucky
        new_fitbit = [rval(-2,2,0), rval(-1000,1000,0)]
        new_sensor = [rval(-5,5),rval(-1,1),rval(-30,30),rval(-30,30),rval(-30,30),rval(-30,30),rval(-30,30),rval(0,5,0),rval(0,5,0),0.18,rval(-0.5,0.5,6),rval(-0.5,0.5,6),0,0]

        final_fitbit = []
        final_sensor = []
        for i in range(0,len(new_fitbit)):
            final_fitbit.append(round(new_fitbit[i]+init_fitbit[i],2))
        for i in range(0,len(new_sensor)):
            final_sensor.append(round(new_sensor[i]+init_sensor[i],2))
        final_fitbit = [str(i) for i in final_fitbit]
        final_sensor = [str(i) for i in final_sensor]
        full = {"timestamp":math.floor(time.time()),"fitbit_data":final_fitbit,"sensor_data":final_sensor}
        global_states.queue.append(full)
            
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
        request = global_constants.gsheets_service.spreadsheets().values().get(spreadsheetId=global_constants.spreadsheet_id, range=read_range, valueRenderOption=global_constants.value_render_option, dateTimeRenderOption=global_constants.date_time_render_option)
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

#region qwidgets
class QTextEditLogger(logging.Handler): #logging as per https://stackoverflow.com/questions/28655198/best-way-to-display-logs-in-pyqt
    def __init__(self, parent):
        super().__init__()
        self.widget = QtWidgets.QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)

#class animation..

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

        #set default values
        data = get_prefs()
        self.default_heartrate = float(data['debug']['randomization_init']['heartrate'])
        self.default_humidity = float(data['debug']['randomization_init']['relative_humidity'])
        self.default_temperature = float(data['debug']['randomization_init']['temperature'])

    def update_defaults(self):
        data = get_prefs()
        self.default_heartrate = int(data['debug']['randomization_init']['heartrate'])
        self.default_humidity = float(data['debug']['randomization_init']['relative_humidity'])
        self.default_temperature = float(data['debug']['randomization_init']['temperature'])

    def update_figure(self):
        if global_states.data_source != "Nothing" and global_states.queue:
            if len(global_states.x_data) > global_states.max_values:
                for _ in range(0,(len(global_states.x_data)-global_states.max_values)):
                    del global_states.x_data[0]
                    del global_states.humidity_values[0]
                    del global_states.temp_values[0]
                    del global_states.heartrate_values[0]
            global_states.x_data.append(int(global_states.queue[0]["timestamp"]))
            if global_states.queue[0]["sensor_data"][0] == "--": #we can reasonably assume that if humidity isn't available, temperature shouldn't either
                global_states.temp_values.append(self.default_temperature)
                global_states.humidity_values.append(self.default_humidity)
            else:
                global_states.temp_values.append(float(global_states.queue[0]["sensor_data"][1]))
                global_states.humidity_values.append(float(global_states.queue[0]["sensor_data"][0]))
            if global_states.queue[0]["fitbit_data"][0] == "--":
                heartrate = self.default_heartrate
            else:
                heartrate = float(global_states.queue[0]["fitbit_data"][0])

            self.axes1.cla()
            self.axes2.cla()
            self.axes3.cla()
            if global_states.queue[0]["sensor_data"][0] == "--":
                self.axes1.plot(global_states.x_data, global_states.temp_values, 'r--') #self.axes.plot(<list of global_states.x_data values>, <list of y values>, <formatting string>)
                self.axes2.plot(global_states.x_data, global_states.humidity_values, 'b--')
            else:
                self.axes1.plot(global_states.x_data, global_states.temp_values, 'r') #self.axes.plot(<list of global_states.x_data values>, <list of y values>, <formatting string>)
                self.axes2.plot(global_states.x_data, global_states.humidity_values, 'b')
            if global_states.queue[0]["fitbit_data"][0] == "--" or  global_states.queue[0]["fitbit_data"][0] == "0":
                #Consider changing the behavior of no fitbit/fitbit not worn to simply not add to the graph. 
                global_states.heartrate_values.append(self.default_heartrate)
                self.axes3.plot(global_states.x_data, global_states.heartrate_values, 'm--')
            else:
                global_states.heartrate_values.append(heartrate)
                global_states.heartrate_historical.append(heartrate)
                self.axes3.plot(global_states.x_data, global_states.heartrate_values, 'm')
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
        #tab 1 - data source
        self.connect_raspi_button.clicked.connect(self.ws_connect)
        self.socket_load_button.clicked.connect(self.load_socket_values)
        self.socket_save_button.clicked.connect(self.save_socket_values)
        self.sheets_load_button.clicked.connect(self.load_sheet_values)
        self.sheets_save_button.clicked.connect(self.save_sheet_values)
        self.open_db_button.clicked.connect(self.open_db_file_dialog)

        #tab 2 - data uploading

        #tab 3 - positioning/competition data
        self.open_obstacles_button.clicked.connect(self.open_obstacle_table)
        self.open_guidebook_button.clicked.connect(self.open_herc_book)   

        #tab 4 - environmental data

        #tab 5 - streaming/utilities
        self.open_github_button.clicked.connect(self.open_github)
        self.open_report_button.clicked.connect(self.open_report)
        self.open_website_button.clicked.connect(self.open_website)
        self.open_data_button.clicked.connect(self.open_data_spreadsheet)
        self.open_overlay_button.clicked.connect(self.open_stream_window)
        self.ts_human_button.clicked.connect(self.find_equivalent_row)  
        self.save_stream_values_button.clicked.connect(self.save_stream_values)
        self.load_stream_values_button.clicked.connect(self.load_stream_values)

        #top menu bar
        self.actionOpen_Preferences.triggered.connect(self.open_prefs_window)
        self.actionObstacle_Task_Table.triggered.connect(self.open_herc_book)
        self.actionGithub.triggered.connect(self.open_github)
        self.actionWebsite.triggered.connect(self.open_website)
        self.actionReport.triggered.connect(self.open_report)
        self.actionAbout.triggered.connect(self.open_about_dialog)
        self.actionGenerate_random_data.triggered.connect(self.start_reading_debug_random)
        self.actionClear_log.triggered.connect(self.clear_log_file)

        global_states.main_timer.timeout.connect(self.update_data)
    def ws_connect(self):
        #implement toggle, i.e. change button text and test for enabled/not
        #if nothing, do below; if websockets, close websocket; if anything else, reset variables and close websocket
        logging.info("Connecting to Raspberry Pi via Websockets...")
        target_ip = self.rpi_ip_edit.text()
        target_port = self.rpi_port_edit.text()
        global_states.websocket_object = WebsocketClient(self,target_ip,target_port)
        global_states.data_source = "Websocket"
        global_states.main_timer.start(1000)
    def clear_log_file(self):
        log_file = open(logpath, 'r')
        lines = 0
        for _ in log_file:
            lines += 1
        log_file.close()
        open(logpath, 'w').close() #overwrite with nothing
        logging.debug("Cleared %s lines in log.txt"%lines) #technically it also adds this but then we know who to blame for a blank log file
    def open_prefs_window(self):
        self.prefs_dialog = PreferencesWindow()
        self.prefs_dialog.setWindowTitle("Preferences")
        self.prefs_dialog.show()
    def open_stream_window(self):
        self.about_dialog = StreamWindow()
        self.about_dialog.setWindowTitle("Stream Overlay")
        self.about_dialog.show()
    def start_reading_socket(self):
        socket_connect()
        global_states.main_timer.start(1000)
    def start_reading_debug_random(self):
        if global_states.data_source != "Debug":
            global_states.data_source = "Debug"
            global_states.main_timer.start(1000)
            logging.info("Started randomized data generation.")
        else: #if == debug
            global_states.main_timer.stop()
            global_states.data_source = "Nothing"
            logging.info("Stopped randomized data generation.")
    def update_data(self):
        if global_states.data_source == "Socket" and global_states.socket_object != None:
            get_data_sockets()
        elif global_states.data_source == "Debug":
            generate_random_data()
        if len(global_states.queue) > 1:
        #... all text label updates go here     
        # {"timestamp":<timestamp>,
        # "fitbit_data":[<heartrate>,<pressure>],
        # "sensor_data":[<humidity[0], temperature[1], pitch[2], roll[3], yaw[4], total x[5], total y[6], total vector count[7],this read vector count[8], internal length constant[9], latitude[10], longitude[11], hdop[12], satellite count[13]>]}
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
            self.altitude_label.setText(str(herctools.pressure_to_height(global_states.queue[0]["fitbit_data"][1]))+" m")
            self.pressure_label.setText(global_states.queue[0]["fitbit_data"][1]+" Pa")
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
                #these two were edited so that floating point precision issues (without round, these end up being n.999999999999994 or something) aren't there
                #check to make sure they still work if normal data is used
                self.total_distance_label.setText(str(round(float(global_states.queue[0]["sensor_data"][7])*float(global_states.queue[0]["sensor_data"][9]),2))+"units")
                self.this_read_distance_label.setText(str(round(float(global_states.queue[0]["sensor_data"][8])*float(global_states.queue[0]["sensor_data"][9]),2))+"units")
            else:
                self.total_distance_label.setText("--")
                self.this_read_distance_label.setText("--")
            #tab 3 labels (course)
                #unimplemented
            #tab 4 labels
            self.temperature_label.setText(global_states.queue[0]["sensor_data"][1])
            self.humiditity_label.setText(global_states.queue[0]["sensor_data"][0])
            if global_states.queue[0]["fitbit_data"][0] == "--":
                self.body_presence_label.setText("Fitbit is not updating.")
                self.bpm_label.setText(global_states.queue[0]["fitbit_data"][0])
            elif global_states.queue[0]["fitbit_data"][0] == "0":
                self.body_presence_label.setText("Body is not currently present on Fitbit.")
                self.bpm_label.setText("--")
            else:
                self.body_presence_label.setText("Body currently present on Fitbit.")
                self.bpm_label.setText(global_states.queue[0]["fitbit_data"][0])
            del global_states.queue[0]
        else:
            #reset all labels to initial state, *then* stop the timer
            pass
            #global_states.main_timer.stop()f
    def convert_timestamp(self):
        pass
        #val = self.lineedit.text()
    def find_equivalent_row(self):
        print(self.dateTimeEdit.dateTime().toPyDateTime()) #to native python time object ("yyyy-mm-dd hh:mm:ss")
        print(self.dateTimeEdit.dateTime().toPyDateTime().timestamp()) #unix timestamp
        print(time.time()) #unix timestamp
    def load_stream_values(self):
        data = get_prefs()
        self.livestream_ip_edit.setText(data['strings']['livestream_ip'])
        self.stream_key_edit.setText(data['strings']['stream_key'])
        logging.info('Loaded stream values.')
    def save_stream_values(self):
        data = get_prefs()
        data['strings']['livestream_ip'] = self.livestream_ip_edit.text()
        data['strings']['stream_key'] = self.stream_key_edit.text()
        write_prefs(data)
        logging.info('Saved stream values.')
    def load_socket_values(self):
        data = get_prefs()
        self.rpi_ip_edit.setText(data['strings']['raspberry_ip'])
        self.rpi_port_edit.setText(data['strings']['raspberry_port'])
        logging.info('Loaded socket values.')
    def save_socket_values(self):
        data = get_prefs()
        data['strings']['raspberry_ip'] = self.rpi_ip_edit.text()
        data['strings']['raspberry_port'] = self.rpi_port_edit.text()
        write_prefs(data)
        logging.info('Saved socket values.')
    def load_sheet_values(self):
        data = get_prefs()
        self.sheet_id_edit.setText(data['strings']['spreadsheet_id'])
        self.sheet_range_edit.setText(data['strings']['spreadsheet_range'])
        logging.info('Loaded sheet values.')
    def save_sheet_values(self):
        data = get_prefs()
        data['strings']['spreadsheet_id'] = self.sheet_id_edit.text()
        data['strings']['spreadsheet_range'] = self.sheet_range_edit.text()
        write_prefs(data)
        logging.info('Saved sheet values.')
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
    def open_db_file_dialog(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(self,"Open Database File", "","Database Files (*.db);;All Files (*)")
        if fileName:
            self.database_path_edit.setText(fileName[0])
        else:
            logging.info("No file selected, ignoring.")
    def open_about_dialog(self):
        pass

#endregion

#region other dialogues
#
class StreamWindow(QtWidgets.QMainWindow,Ui_OverlayWindow):
    #the icon will show with the use of qt resource files, but will normally fail without absolute references
    #consider trying to use fbs's resource system instead?
    
    #it would be a good idea to disconnect the slot on close, in addition to a button
    def __init__(self):
        super().__init__()
        self.ui = Ui_OverlayWindow()
        self.ui.setupUi(self)
        self.ui.start_updating_button.clicked.connect(self.toggle_updating)
        self.ui.help_button.clicked.connect(self.test_boxes)

        self.updating = False
        self.cycle_index = 0
        #self.aboutToQuit.connect(self.quitting)
        #self.ui.test_icon.setPixmap(QtGui.QPixmap('C:/Users/Kisun/Desktop/ui-new/src/main/resources/flag-test.svg'))
        #self.ui.test_icon.setPixmap(QtGui.QPixmap('flag.png'))
    def closeEvent(self, event):
        if self.updating:
            global_states.main_timer.timeout.disconnect(self.update_labels)
            logging.debug("Auto-disconnected global_states.main_timer.timeout signal on close.")
        # close window
        event.accept()
    def toggle_updating(self):
        if not self.updating:
            global_states.main_timer.timeout.connect(self.update_labels)
            logging.debug("animation toggle on")
            self.updating = True
        else:
            global_states.main_timer.timeout.disconnect(self.update_labels)
            logging.debug("animation toggle off")
            self.updating = False
    def update_labels(self):
        
        #any additional calcs..

        #figure out what data should appear on the lower-left next based on checked boxes
        states = [self.ui.environmental_checkbox.isChecked(),self.ui.athlete_checkbox.isChecked(),self.ui.data_read_checkbox.isChecked(),self.ui.cumulative_position_checkbox.isChecked(),self.ui.gps_checkbox.isChecked()]
        if any(states):
            for i in range(1,6):
                if states[(self.cycle_index+i)%5]:
                    self.cycle_index = (self.cycle_index+i)%5
                    print("cycled to index %s"%self.cycle_index)
                    break
        else:
            #what behavior should occur here?
            print("all boxes unchecked")

        #update everything else
        self.ui.next_obstacle_label.setText(str(global_states.queue[0]["timestamp"]))
        print("updated labels at%s"%math.floor(time.time()))
    def test_boxes(self):
        #correct athlete - athelete
        states = [self.ui.environmental_checkbox.isChecked(),self.ui.athlete_checkbox.isChecked(),self.ui.data_read_checkbox.isChecked(),self.ui.cumulative_position_checkbox.isChecked(),self.ui.gps_checkbox.isChecked()]
        for i in range(1,6):
            if states[(self.cycle_index+i)%5]:
                self.cycle_index = (self.cycle_index+i)%5
                print("cycled to index %s"%self.cycle_index) 

class PreferencesWindow(QtWidgets.QMainWindow,Ui_PreferencesWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_PreferencesWindow()
        self.ui.setupUi(self)
        self.ui.save_prefs_button.clicked.connect(self.save_prefs)
        self.ui.toggle_variables_button.clicked.connect(self.toggle_advanced)

        #toggle debug labels
        self.debug_labels = False

        #load prefs
        data = get_prefs()
        for i in herctools.preferences_mapping:
            exec('self.ui.%s.setText(%s)'%(i,herctools.preferences_mapping[i]))
    def toggle_advanced(self):
        if self.debug_labels:
            self.debug_labels = False
            for i in herctools.label_toggles:
                exec('self.ui.%s.setText("%s")'%(i,herctools.label_toggles[i][0]))
            self.ui.toggle_variables_button.setText("Show internal variable names")
        else:
            self.debug_labels = True
            for i in herctools.label_toggles:
                exec('self.ui.%s.setText("%s")'%(i,herctools.label_toggles[i][1]))
                self.ui.toggle_variables_button.setText("Hide internal variable names")
    def save_prefs(self):
        data = get_prefs()
        lineedits = self.findChildren(QtWidgets.QLineEdit) #get every QLineEdit (object), iterable
        full={}
        for element in lineedits:
            full[element.objectName()] = element.text()
        #i'm sure there's a better way to do this but i don't know what it is nor could i find it
        for i in herctools.preferences_mapping:
            exec('%s = "%s"'%(herctools.preferences_mapping[i],full[i]))
        write_prefs(data)
        logging.info('Updated preferences.')
        self.close()

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