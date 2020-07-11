import math

def pressure_to_height(pressure, places=2):
    '''
    Converts pressure in pascals (as sent by the Fitbit) to height in meters.
    Uses the (inverse of the) formula found here: https://www.math24.net/barometric-formula/
    '''
    return round(math.log((float(pressure)/1000)/101.325)/-0.00012,places)

'''
preferences_mapping = {
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
    "stream_key_edit":"data['strings']['stream_key']",
    "rpi_stream_edit":"data['strings']['livestream_ip']"
}
'''