from pigpio import *
from structs import *
import RPi.GPIO as GPIO
import time
import structs

# pipeline operator (>>_>>)
_ = structs._

# device address
POWER_ADDRESS           = 0x02

# raspberry pi bus number
PI_BUS                  = 1

# command registers
CMD_PING                = 0x01
CMD_REBOOT              = 0x04
CMD_GET_HK              = 0x08
CMD_SET_OUTPUT          = 0x09
CMD_SET_SINGLE_OUTPUT   = 0x0A
CMD_SET_PV_VOLT         = 0x0B
CMD_SET_PV_AUTO         = 0x0C
CMD_SET_HEATER          = 0x0D
CMD_RESET_COUNTERS      = 0x0F
CMD_RESET_WDT           = 0x10
CMD_CONFIG_CMD          = 0x11
CMD_CONFIG_GET          = 0x12
CMD_CONFIG_SET          = 0x13
CMD_HARD_RESET          = 0x14
CMD_CONFIG2_CMD         = 0x15
CMD_CONFIG2_GET         = 0x16
CMD_CONFIG2_SET         = 0x17

# struct sizes in bytes
SIZE_HKPARAM_T          = 44
SIZE_EPS_HK_T           = 136
SIZE_EPS_HK_VI_T        = 20
SIZE_EPS_HK_OUT_T       = 64
SIZE_EPS_HK_WDT_T       = 28
SIZE_EPS_HK_BASIC_T     = 24
SIZE_EPS_CONFIG_T       = 58
SIZE_EPS_CONFIG2_T      = 20

# power outputs
OUT_0                   = 0
OUT_1                   = 1
OUT_2                   = 2
OUT_BURNWIRE            = 3
OUT_SOLENOID            = 4
OUT_ELECTROLYZER        = 5     # 3.3v output

# pi outputs
OUT_PI_SPARKPLUG        = 7     # GPIO 4

class Power(object):
    # initializes power object with bus [bus] and device address [addr]
    def __init__(self, bus=PI_BUS, addr=POWER_ADDRESS, flags=0):
        self._pi = pi()                                     # initialize pigpio object
        self._dev = self._pi.i2c_open(bus, addr, flags)     # initialize i2c device

        # initialize pi outputs
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(OUT_PI_SPARKPLUG, GPIO.OUT)
        GPIO.output(OUT_PI_SPARKPLUG, GPIO.HIGH)

        # initialize eps outputs
        self.set_output(0)

    # prints config/config2/housekeeping
    def displayAll(self):
        displayHK(self.get_hk_1())
        displayConfig(self.config_get())
        displayConfig2(self.config2_get())

    # writes byte list [values] to register [cmd]
    def write(self, cmd, values):
        self._pi.i2c_write_device(self._dev, bytearray([cmd]+values))

    # reads [bytes] number of bytes from the device and returns a bytearray
    def read(self, bytes):
        # first two read bytes -> [command][error code][data]
        (x, r) = self._pi.i2c_read_device(self._dev, bytes+2) 
        if r[1] != 0:
            print "Command %i failed with error code %i" % (r[0], r[1])
        return r[2:]

    # pings value
    # value [1 byte]
    def ping(self, value):
        self.write(CMD_PING, [value])
        return self.read(1)

    # reboot the system
    def reboot(self):
        self.write(CMD_REBOOT, [0x80, 0x07, 0x80, 0x07])

    # returns hkparam_t struct
    def get_hk_1(self):
        self.write(CMD_GET_HK, [])
        array = self.read(SIZE_HKPARAM_T)
        return c_bytesToStruct(array, "hkparam_t")

    # returns eps_hk_t struct
    def get_hk_2(self):
        self.write(CMD_GET_HK, [0x00])
        array = self.read(SIZE_EPS_HK_T)
        return c_bytesToStruct(array, "eps_hk_t")

    # returns eps_hk_vi_t struct
    def get_hk_2_vi(self):
        self.write(CMD_GET_HK, [0x01])
        array = self.read(SIZE_EPS_HK_VI_T)
        return c_bytesToStruct(array, "eps_hk_vi_t")

    # returns eps_hk_out_t struct
    def get_hk_out(self):
        self.write(CMD_GET_HK, [0x02])
        array = self.read(SIZE_EPS_HK_OUT_T)
        return c_bytesToStruct(array, "eps_hk_out_t")

    # returns eps_hk_wdt_t struct
    def get_hk_wdt(self):
        self.write(CMD_GET_HK, [0x03])
        array = self.read(SIZE_EPS_HK_WDT_T)
        return c_bytesToStruct(array, "eps_hk_wdt_t")

    # returns eps_hk_basic_t struct
    def get_hk_2_basic(self):
        self.write(CMD_GET_HK, [0x04])
        array = self.read(SIZE_EPS_HK_BASIC_T)
        return c_bytesToStruct(array, "eps_hk_basic_t")

    # sets voltage output channels with bit mask: 
    # byte [1 byte] -> [NC NC 3.3V3 3.3V2 3.3V1 5V3 5V2 5V1]
    def set_output(self, byte):
        self.write(CMD_SET_OUTPUT, [byte])

    # sets a single output on or off:
    # channel [1 byte]  -> voltage = (0~5), BP4 heater = 6, BP4 switch = 7
    # value   [1 byte]  -> on = 1, off = 0
    # delay   [2 bytes] -> [seconds]
    def set_single_output(self, channel, value, delay):
        d = toBytes(delay, 2)
        self.write(CMD_SET_SINGLE_OUTPUT, [channel, value]+list(d))

    # Set the voltage on the photo- voltaic inputs V1, V2, V3 in mV. 
    # Takes effect when MODE = 2, See SET_PV_AUTO.
    # Transmit voltage1 first and voltage3 last.
    # volt1~volt3 [2 bytes] -> value in mV
    def set_pv_volt(self, volt1, volt2, volt3):
        v = bytearray(6)
        v[0:2] = toBytes(volt1, 2)
        v[2:4] = toBytes(volt2, 2)
        v[4:] = toBytes(volt3, 2)
        self.write(CMD_SET_PV_VOLT, list(v))

    # Sets the solar cell power tracking mode:
    # mode [1 byte] ->
    # MODE = 0: Hardware default power point
    # MODE = 1: Maximum power point tracking
    # MODE = 2: Fixed software powerpoint, value set with SET_PV_VOLT, default 4V
    def set_pv_auto(self, mode):
        self.write(CMD_SET_PV_AUTO, [mode])

    # returns bytearray with heater modes
    # command   [1 byte]  -> 0 = Set heater on/off (toggle?)
    # heater    [1 byte]  -> 0 = BP4, 1 = Onboard, 2 = Both
    # mode      [1 byte]  -> 0 = OFF, 1 = ON
    # return    [2 bytes] -> heater modes
    def set_heater(self, command, heater, mode):
        self.write(CMD_SET_HEATER, [command, heater, mode])
        return self.read(2)

    def get_heater(self):
        self.write(CMD_SET_HEATER, [])
        return self.read(2)

    # resets the boot counter and WDT counters.
    def reset_counters(self):
        self.write(CMD_RESET_COUNTERS, [0x42])

    # resets (kicks) dedicated WDT.
    def reset_wdt(self):
        self.write(CMD_RESET_WDT, [0x78])

    # Use this command to control the config system.
    # cmd [1 byte] -> cmd = 1: Restore default config
    def config_cmd(self, command):
        self.write(CMD_CONFIG_CMD, [command])

    # returns eps_config_t structure
    def config_get(self):
        self.write(CMD_CONFIG_GET, [])
        return c_bytesToStruct(self.read(SIZE_EPS_CONFIG_T), "eps_config_t")

    # takes eps_config_t struct and sets configuration
    def config_set(self, struct):
        assert type(struct) == eps_config_t
        array = struct >>_>> c_structToBytes >>_>> bytesToList
        self.write(CMD_CONFIG_SET, array)

    # Send this command to perform a hard reset of the P31,
    # including cycling permanent 5V and 3.3V and battery outputs.
    def hard_reset(self):
        self.write(CMD_HARD_RESET, [])

    # Use this command to control the config 2 system.
    # cmd [1 byte] -> cmd=1: Restore default config; cmd=2: Confirm current config
    def config2_cmd(self, command): 
        self.write(CMD_CONFIG2_CMD, [command]) 

    # Use this command to request the P31 config 2.
    # returns esp_config2_t struct
    def config2_get(self):
        self.write(CMD_CONFIG2_GET, [])
        return c_bytesToStruct(self.read(SIZE_EPS_CONFIG2_T), "eps_config2_t")

    # Use this command to send config 2 to the P31
    # and save it (remember to also confirm it)
    def config2_set(self, struct):
        assert type(struct) == eps_config2_t
        array = struct >>_>> c_structToBytes >>_>> bytesToList
        self.write(CMD_CONFIG2_SET, array)


    # Higher level functions ---------------------------------------------------------

    # output must be off before the function is called
    # pulses high for duration amount of milliseconds
    def pulse(self, output, duration, delay=0):
        time.sleep(delay)
        self.set_single_output(output, 1, 0)
        time.sleep(duration*.001)
        self.set_single_output(output, 0, 0)

    # output must be off before the function is called
    # pulses high for duration amount of milliseconds
    def pulse_pi(self, output, duration, delay=0):
        time.sleep(delay)
        GPIO.output(output, GPIO.HIGH)
        time.sleep(duration*.001)
        GPIO.output(output, GPIO.LOW)

    # switches on/off electrolyzer
    def electrolyzer(self, switch, delay=0):
        self.set_single_output(OUT_ELECTROLYZER, int(bool(switch != 0)), delay)

    # pulses the solenoid for some number of milliseconds
    # output must be off before the function is called
    def solenoid(self, duration, delay=0):
        self.pulse(OUT_SOLENOID, duration, delay)

    # pulses sparkplug for some number of milliseconds
    # output must be off before the function is called
    def sparkplug(self, duration, delay=0):
        self.pulse_pi(OUT_PI_SPARKPLUG, duration, delay)

    # turns burnwire on for some number of seconds
    def burnwire(self, duration, delay=0):
        time.sleep(delay)
        self.set_single_output(OUT_BURNWIRE, 1, 0)
        time.sleep(duration)
        self.set_single_output(OUT_BURNWIRE, 0, 0)
        
