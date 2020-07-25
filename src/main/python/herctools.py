import math

def pressure_to_height(pressure, places=2):
    '''
    Converts pressure in pascals (as sent by the Fitbit) to height in meters.
    Uses the (inverse of the) formula found here: https://www.math24.net/barometric-formula/
    '''
    if pressure == '--':
        return "--"
    else:
        return round(math.log((float(pressure)/1000)/101.325)/-0.00012,places)

preferences_mapping = {
    "debug_level_edit":"data['debug']['logging_level']",
    "offset_longitude_edit":"data['debug']['plotting']['longitude_offset']",
    "debug_heartrate_edit":"data['debug']['randomization_init']['heartrate']",
    "debug_pressure_edit":"data['debug']['randomization_init']['air_pressure']",
    "debug_humidity_edit":"data['debug']['randomization_init']['relative_humidity']",
    "debug_temperature_edit":"data['debug']['randomization_init']['temperature']",
    "debug_pitch_edit":"data['debug']['randomization_init']['pitch']",
    "debug_roll_edit":"data['debug']['randomization_init']['roll']",
    "debug_yaw_edit":"data['debug']['randomization_init']['yaw']",
    "debug_toty_edit":"data['debug']['randomization_init']['total_y_disp']",
    "debug_totx_edit":"data['debug']['randomization_init']['total_x_disp']",
    "debug_totall_edit":"data['debug']['randomization_init']['total_vectors']",
    "debug_vectors_edit":"data['debug']['randomization_init']['this_read_vectors']",
    "debug_length_constant_edit":"data['debug']['randomization_init']['internal_length_constant']",
    "debug_latitude_edit":"data['debug']['randomization_init']['latitude']",
    "debug_longitude_edit":"data['debug']['randomization_init']['longitude']",
    "debug_hdop_edit":"data['debug']['randomization_init']['hdop']",
    "debug_satellite_edit":"data['debug']['randomization_init']['satellite_count']",
    "offset_latitude_edit":"data['debug']['plotting']['latitude_offset']",
    "max_values_edit":"data['general']['max_values_on_graphs']",
    "read_delay_edit":"data['general']['data_read_delay']",
    "timeout_edit":"data['general']['max_timeout']",
    "rpi_ip_edit":"data['strings']['raspberry_ip']",
    "rpi_port_edit":"data['strings']['raspberry_port']",
    "gsheets_id_edit":"data['strings']['spreadsheet_id']",
    "gsheets_range_edit":"data['strings']['spreadsheet_range']",
    "gsheets_row_edit":"data['strings']['spreadsheet_starting_row']",
    "mongodb_host_edit":"data['strings']['mongodb_host']",
    "mongodb_database_edit":"data['strings']['mongodb_database_name']",
    "mongodb_timestamp_edit":"data['strings']['mongodb_starting_timestamp']",
    "stream_key_edit":"data['strings']['stream_key']",
    "rpi_stream_edit":"data['strings']['livestream_ip']"
}

label_toggles = {
    "enable_font_debug_label":["Enable logging of matplotlib font debug statements.","logging.getLogger('matplotlib.font_manager').disabled = bool"],
    "debug_heartrate_label":["Heartrate","queue['fitbit_data'][0]; int (internally float)"],
    "debug_pressure_label":["Air pressure","queue['fitbit_data'][1]; int (internally float)"],
    "debug_humidity_label":["Relative humidity (0-99.9%)","queue['sensor_data'][0]; float"],
    "debug_temperature_label":["Temperature","queue['sensor_data'][1]; float"],
    "debug_pitch_label":["Pitch","queue['sensor_data'][2]; float"],
    "debug_roll_label":["Roll","queue['sensor_data'][3]; float"],
    "debug_yaw_label":["Yaw","queue['sensor_data'][4]; float"],
    "debug_totx_label":["Total x displacement","queue['sensor_data'][5]; float"],
    "debug_toty_label":["Total y displacement","queue['sensor_data'][6]; float"],
    "debug_totall_label":["Total number of vectors read","queue['sensor_data'][7]; int (internally float)"],
    "debug_this_read_label":["Vectors read this data frame","queue['sensor_data'][8]; int (internally float)"],
    "debug_length_constant_label":["Internal length constant","queue['sensor_data'][9]; float"],
    "debug_latitude_label":["Latitude","queue['sensor_data'][10]; float"],
    "debug_longitude_label":["Longitude","queue['sensor_data'][11]; float"],
    "debug_hdop_label":["HDOP (horizontal dilution of precision, GPS)","queue['sensor_data'][12]; float"],
    "debug_satellite_label":["Satellite count (GPS)","queue['sensor_data'][13]; int (internally float)"],
    "offset_longitude_label":["Longitude","global_states.longitude_offset = float"],
    "offset_latitude_label":["Latitude","global_states.latitude_offset = float"],
    "max_values_label":["Number of max values represented on data graphs.","global_states.max_values = int"],
    "read_delay_label":["Read delay, in ms, between each new frame of data. Works best if quickly reading data from a static data source (i.e. not a live source).","global_states.read_delay = int"],
    "timeout_label":["Number of max failed reads from a data source before the client stops trying.","global_states.timeout = int"],
    "rpi_ip_label":["IP address of Raspberry Pi handling most of the data.","self.rpi_ip_edit"],
    "rpi_port_label":["Port of Raspberry Pi handling most data (same as above).","self.rpi_port_edit"],
    "gsheets_id_label":["ID of the Google Sheets spreadsheet for reading and writing data.","self.external_1_edit"],
    "gsheets_range_label":["Range to use for the Google Sheets spreadsheet.","self.external_2_edit"],
    "gsheets_row_label":["Starting row for the Google Sheets spreadsheet.","self.external_3_edit"],
    "mongodb_host_label":["MongoDB Atlas host address.","self.external_1_edit"],
    "mongodb_database_label":['Default MongoDB database. Note that the collection "main" is always used (and may be created if it does not exist on the given database).',"self.external_2_edit"],
    "mongodb_timestamp_label":["Starting timestamp for reading from MongoDB Atlas.","self.external_3_edit"],
    "stream_key_label":["Stored key for streaming, if applicable. Use in OBS Studio.","self.livestream_ip_edit"],
    "rpi_stream_label":["Full IP address and port of the Raspberry Pi handling video streaming.","self.stream_key_edit"]
}