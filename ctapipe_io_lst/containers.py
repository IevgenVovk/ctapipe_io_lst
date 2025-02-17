"""
Container structures for data that should be read or written to disk
"""
from astropy import units as u
from numpy import nan
from ctapipe.core import Container, Field, Map
from ctapipe.io.containers import DataContainer, MonitoringContainer


__all__ = [
    'LSTDriveContainer',
    'LSTEventContainer',
    'LSTMonitoringContainer',
    'LSTServiceContainer',
    'LSTCameraContainer',
    'LSTContainer',
    'LSTMonitoringContainer',
    'LSTDataContainer'
]


class LSTDriveContainer(Container):
    """
    Drive report container
    """
    date = Field(" ", "observation date")
    time_stamp = Field(-1, "timestamp")
    epoch = Field(-1, "Epoch")
    time = Field(-1, "time",)
    azimuth_avg = Field(nan * u.rad, "Azimuth", unit=u.rad)
    azimuth_min = Field(nan * u.rad, "Azimuth min", unit=u.rad)
    azimuth_max = Field(nan * u.rad, "Azimuth max", unit=u.rad)
    azimuth_rmse = Field(nan * u.rad, "Azimuth root-mean-square error", unit=u.rad)
    altitude_avg = Field(nan * u.rad, "Altitude", unit=u.rad)
    altitude_min = Field(nan * u.rad, "Altitude min", unit=u.rad)
    altitude_max = Field(nan * u.rad, "Altitude max", unit=u.rad)
    altitude_rmse = Field(nan * u.rad, "Altitude root-mean-square error", unit=u.rad)


class LSTServiceContainer(Container):
    """
    Container for Fields that are specific to each LST camera configuration
    """

    # Data from the CameraConfig table
    telescope_id = Field(-1, "telescope id")
    cs_serial = Field(None, "serial number of the camera server")
    configuration_id = Field(None, "id of the CameraConfiguration")
    date = Field(None, "NTP start of run date")
    num_pixels = Field(-1, "number of pixels")
    num_samples = Field(-1, "num samples")
    pixel_ids = Field([], "id of the pixels in the waveform array")
    data_model_version = Field(None, "data model version")

    idaq_version = Field(0o0, "idaq version")
    cdhs_version = Field(0o0, "cdhs version")
    algorithms = Field(None, "algorithms")
    pre_proc_algorithms = Field(None, "pre processing algorithms")
    module_ids = Field([], "module ids")
    num_modules = Field(-1, "number of modules")


class LSTEventContainer(Container):
    """
    Container for Fields that are specific to each LST event
    """

    # Data from the CameraEvent table
    configuration_id = Field(None, "id of the CameraConfiguration")
    event_id = Field(None, "local id of the event")
    tel_event_id = Field(None, "global id of the event")
    pixel_status = Field([], "status of the pixels (n_pixels)")
    ped_id = Field(None, "tel_event_id of the event used for pedestal substraction")
    module_status = Field([], "status of the modules (n_modules)")
    extdevices_presence = Field(None, "presence of data for external devices")

    tib_event_counter = Field(None, "TIB event counter")
    tib_pps_counter = Field(None, "TIB pps counter")
    tib_tenMHz_counter = Field(None, "TIB 10 MHz counter")
    tib_stereo_pattern = Field(None, "TIB stereo pattern")
    tib_masked_trigger = Field(None, "TIB trigger mask")

    ucts_event_counter =  Field(None, "UCTS event counter")
    ucts_pps_counter = Field(None, "UCTS pps counter")
    ucts_clock_counter = Field(None, "UCTS clock counter")
    ucts_timestamp = Field(None, "UCTS timestamp")
    ucts_camera_timestamp = Field(None, "UCTS camera timestamp")
    ucts_trigger_type = Field(None, "UCTS trigger type")
    ucts_white_rabbit_status = Field(None, "UCTS whiteRabbit status")

    swat_timestamp = Field(None, "SWAT timestamp")
    swat_counter1 = Field(None, "SWAT event counter 1")
    swat_counter2 = Field(None, "SWAT event counter 2")
    swat_event_type = Field(None, "SWAT event type")
    swat_camera_flag = Field(None, "SWAT camera flag ")
    swat_camera_event_num = Field(None, "SWAT camera event number")
    swat_array_flag = Field(None, "SWAT array negative flag")
    swat_array_event_num = Field(None, "SWAT array event number")

    pps_counter= Field([], "Dragon pulse per second counter (n_modules)")
    tenMHz_counter = Field([], "Dragon 10 MHz counter (n_modules)")
    event_counter = Field([], "Dragon event counter (n_modules)")
    trigger_counter = Field([], "Dragon trigger counter (n_modules)")
    local_clock_counter = Field([], "Dragon local 133 MHz counter (n_modules)")

    chips_flags = Field([], "chips flags")
    first_capacitor_id = Field([], "first capacitor id")
    drs_tag_status = Field([], "DRS tag status")
    drs_tag = Field([], "DRS tag")


class LSTMonitoringContainer(Container):
    """
    Container for Fields/containers that are specific for the LST monitoring
    e.g. the pointing data
    """
    drive = Field(LSTDriveContainer(), "container for LST drive reports")
     

class LSTCameraContainer(Container):
    """
    Container for Fields that are specific to each LST camera
    """
    evt = Field(LSTEventContainer(), "LST specific event Information")
    svc = Field(LSTServiceContainer(), "LST specific camera_config Information")
    mon = Field(LSTMonitoringContainer(), "LST specific monitoring Information")


class LSTContainer(Container):
    """
    Storage for the LSTCameraContainer for each telescope
    """
    tels_with_data = Field([], "list of telescopes with data")

    # create the camera container
    tel = Field(
        Map(LSTCameraContainer),
        "map of tel_id to LSTTelContainer")


class LSTDataContainer(DataContainer):
    """
    Data container including LST and monitoring information
    """
    lst = Field(LSTContainer(), "LST specific Information")
    mon = Field(MonitoringContainer(), "container for LST monitoring data (MON)")
