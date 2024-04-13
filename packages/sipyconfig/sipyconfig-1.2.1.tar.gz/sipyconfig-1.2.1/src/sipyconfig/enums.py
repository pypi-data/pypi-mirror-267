"""
submodule providing enums and error classes for the whole module
"""

from typing import Dict
from enum import IntEnum, Enum


class SiError(Exception):
    """General Error for the whole module, all other Errors are derived from this class."""


class CRCError(SiError):
    """Error for not matching CRC"""


class SiCardEventError(SiError):
    """Subclass of this Error are raised, if a SI Card was inserted or removed, while waiting on a command response."""


class SiCardInserted(SiCardEventError):
    """raised when a SI Card is inserted into the station while waiting on a command response."""


class SiCardRemoved(SiCardEventError):
    """raised when the SI Card is removed from the station while waiting on a command response."""


class SiCardAutoSend(SiCardEventError):
    """raised when a SI Card is inserted in Auto Send Mode."""


class SiCardError(SiError):
    """raised when an Error occurred in parsing the SI Card information."""


class misc(IntEnum):  # pylint: disable=invalid-name
    """enum for miscellaneous values"""
    MODE_DIRECT = 0x4D
    MODE_REMOTE = 0x53
    SIAC_ON = 0x07
    SIAC_OFF = 0x05

    DATA_COMMAND_OFFSET = 3


class proto(IntEnum):  # pylint: disable=invalid-name
    """enum for special protocoll characters"""
    STX = 0x02  # Start of text
    ETX = 0x03  # End of text
    ACK = 0x06  # Positive Handshake return
    NAK = 0x15  # Negative Handshake return
    DLE = 0x10  # DeLimitEr for data characters
    WAKEUP = 0xFF  # send to station for wakeup


class com(IntEnum):  # pylint: disable=invalid-name
    """enum for all documented command codes"""
    GET_BACK_MEM = 0x81
    SET_SYS_DATA = 0x82
    GET_SYS_DATA = 0x83
    SRR_WRITE = 0xA2
    SRR_READ = 0xA3
    SRR_QUERY = 0xA6
    SRR_PING = 0xA7
    SRR_ADHOC = 0xA8
    GET_SI_5 = 0xB1
    WRITE_SI_5 = 0xC3
    PUNCH_DATA = 0xD3
    CLEAR_SI = 0xE0
    GET_SI_6 = 0XE1
    DETECT_SI_5 = 0xE5
    DETECT_SI_6 = 0xE6
    SI_REMOVED = 0xE7
    DETECT_SI_8 = 0xE8
    WRITE_SI_8 = 0xEA
    GET_SI_8 = 0xEF
    SET_MS_MODE = 0XF0
    GET_MS_MODE = 0xF1
    ERASE_BACK = 0xF5
    SET_TIME = 0xF6
    GET_TIME = 0xF7
    TURN_OFF = 0xF8
    FEEDBACK = 0xF9
    SET_BAUDRATE = 0xFE
    # Basic Commands
    SET_MS_MODE_BASIC = 0x70
    SET_BAUDRATE_BASIC = 0x7E


com_rev: Dict[int, str] = {v.value: k for k, v in com.__members__.items()}


class memaddr(IntEnum):  # pylint: disable=invalid-name
    """enum for all documented system data memory addresses in SI Stations"""
    SERIAL_NO = 0x00
    SRR_CFG = 0x04
    FIRMWARE = 0x05
    BUILD_DATE = 0x08
    MODEL_ID = 0x0B
    MEM_SIZE = 0x0D
    BAT_DATE = 0x15
    BAT_CAP = 0x19
    BACKUP_PTR_HI = 0x1C
    BACKUP_PTR_LO = 0x21
    SI6_CB = 0x33
    SRR_CHANNEL = 0x34
    USED_BAT_CAP = 0x35
    MEM_OVERFLOW = 0x3D
    SRR_PROTOCOL = 0x3F
    BAT_VOLT = 0x50
    SIAC = 0x5A
    PROGRAM = 0x70
    MODE = 0x71
    CONTROL_NUMBER = 0x72
    SETTINGS_FLAG = 0x73
    PROTOCOL_MODE_FLAG = 0x74
    WAKEUP_DATE = 0x75
    WAKEUP_TIME = 0x78
    SLEEP_TIME = 0x7B
    ACTIVE_TIME = 0x7E


class memlen(IntEnum):  # pylint: disable=invalid-name
    """enum for the length of the values associated with the address described in memaddr"""
    SERIAL_NO = 0x04
    SRR_CFG = 0x01
    FIRMWARE = 0x03
    BUILD_DATE = 0x03
    MODEL_ID = 0x02
    MEM_SIZE = 0x01
    BAT_DATE = 0x03
    BAT_CAP = 0x02
    BACKUP_PTR_HI = 0x02
    BACKUP_PTR_LO = 0x02
    SI6_CB = 0x01
    SRR_CHANNEL = 0x01
    USED_BAT_CAP = 0x03
    MEM_OVERFLOW = 0x01
    SRR_PROTOCOL = 0x01
    BAT_VOLT = 0x02
    SIAC = 0x01
    PROGRAM = 0x01
    MODE = 0x01
    CONTROL_NUMBER = 0x01
    SETTINGS_FLAG = 0x01
    PROTOCOL_MODE_FLAG = 0x01
    WAKEUP_DATE = 0x03
    WAKEUP_TIME = 0x03
    SLEEP_TIME = 0x03
    ACTIVE_TIME = 0x02


class stationmode(IntEnum):  # pylint: disable=invalid-name
    """enum for all supported operating modes of the SI station"""
    CONTROL = 0x02
    START = 0x03
    FINISH = 0x04
    READOUT = 0x05
    CLEAR_OLD = 0x06
    CLEAR = 0x07
    CHECK = 0x0A
    PRINTOUT = 0x0B
    START_TRIG = 0x0C
    FINISH_TRIG = 0x0D
    SIAC_TEST = 0x11
    SIAC_CONTROL = 0x32
    SIAC_START = 0x33
    SIAC_FINISH = 0x34
    SIAC_SPECIAL = 0x01
    SIAC_BATTERY_TEST = 0x7B
    SIAC_ON = 0x7C
    SIAC_OFF = 0x7D
    SIAC_RADIO_READOUT = 0x7F
    UNKNOWN = 0xFF


mode_rev: Dict[int, str] = {
    v.value: k for k, v in stationmode.__members__.items()}


class siacmode(IntEnum):  # pylint: disable=invalid-name
    """enum for different SIAC radio modes"""
    NO_SIAC = 0x00
    SIAC_SPECIAL = 0x10
    NO_RADIO = 0x30
    LAST_RECORD = 0x70
    ALL_RECORDS = 0xb0
    UNSENT_RECORDS = 0xf0


siacmode_rev: Dict[int, str] = {
    v.value: k for k, v in siacmode.__members__.items()}


class MODELID(Enum):  # pylint: disable=invalid-name
    """enum for station model id"""
    SIMSSR1_AP = b'\x6F\x21'
    BSF3 = b'\x80\x03'
    BSF4 = b'\x80\x04'
    BSM4_RS232 = b'\x80\x84'
    BSM6_USB = b'\x80\x86'
    BSF5 = b'\x81\x15'
    BSF7 = b'\x81\x17'
    BSF8 = b'\x81\x18'
    BSF6 = b'\x81\x46'
    BSF7_SI_MASTER = b'\x81\x87'
    BSF8_SI_MASTER = b'\x81\x88'
    BSF7_2 = b'\x81\x97'
    BSF8_2 = b'\x81\x98'
    BSM7_USB = b'\x91\x97'
    BSM8_USB = b'\x91\x98'
    BS7_S = b'\x95\x97'
    BS11_BL = b'\x9D\x9A'
    BS7_P = b'\xB1\x97'
    BS8_P = b'\xB1\x98'
    BS7_GSM = b'\xB8\x97'
    BS11_BS_RED = b'\xCD\x9B'
    UNKNOWN = b'\xff\xff'


model_rev: Dict[bytes, str] = {
    v.value: k for k, v in MODELID.__members__.items()}


class CPC(IntEnum):
    """enum of the bit mask for the communications protocol byte"""
    EXTENDED_PROTCOL = 0x01
    AUTO_SEND = 0x02
    HANDSHAKE = 0x04
    ACCESS_PASSWORD = 0x10
    READ_AFTER_PUNCH = 0x40


class SETTINGS(IntEnum):
    """enum of the bit mask for the settings byte"""
    OPTICAL_FEEDBACK = 0x01
    ACOUSTIC_FEEDBACK = 0x04
    NUMBER_HIGH_BIT = 0x40


class coderange(IntEnum):  # pylint: disable=invalid-name
    """suggested code range for different operating modes"""
    READOUT = 15
    PRINTOUT = 11
    CLEAR = 1
    START_FINISH_CHECK_FROM = 2
    START_FINISH_CHECK_TO = 30
    CONTROL_FROM = 31
    CONTROL_TO = 511


class defaulttime(IntEnum):  # pylint: disable=invalid-name
    """"enum for the default/suggested operating times for the operating modes"""
    CLEAR = 4
    CHECK = 4
    START = 4
    CONTROL = 4
    FINISH = 4
    READOUT = 1
    BEACON_START = 12
    BEACON_CONTROL = 12
    BEACON_FINISH = 12
    SIAC_BATTERY = 1
    SIAC_ON = 1
    SIAC_OFF = 1
    SIAC_READOUT = 1
    SIAC_TEST = 12


class SIAC_BEEP(Enum):  # pylint: disable=invalid-name
    """enum for the different SIAC feedback (beep) modes"""
    DEFAULT = b'\x18\x00\x05\x4A'
    SHORT = b'\x06\x00\x05\x4A'
    LONG = b'\x30\x00\x05\x4A'
    BLINK_ONLY = b'\x20\x00\x66\x00'


siac_rev: Dict[bytes, str] = {
    v.value: k for k, v in SIAC_BEEP.__members__.items()}

"""holds the mapping for the SRR autodetect feature, can be modified at runtime if needed"""
control_number_to_mode: Dict[int, stationmode] = {
    1: stationmode.CLEAR,
    2: stationmode.CHECK,
    3: stationmode.START,
    4: stationmode.FINISH
}
