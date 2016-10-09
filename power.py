from ctypes import *
#from pigpio import *

class TestingStruct(BigEndianStructure):
    _fields_ = [
        ("field1", c_uint8),
        ("field2", c_uint8),
        ("field3", c_uint16)
    ]

class hkparam_t(BigEndianStructure):
	_fields_ = [
		("pv", 				c_uint16*3), 	# Photo-voltaic input voltage [mV]
		("pc",   			c_uint16),  	# Total photo current [mA]
		("bv",    			c_uint16), 		# Battery voltage [mV]
		("sc",  			c_uint16), 		# Total system current [mA]
		("temp", 		   	c_int16*4), 	# Temp. of boost converters (1,2,3) and onboard battery [degC]
		("batt_temp", 	   	c_int16*2), 	# External board battery temperatures [degC];
		("latchup", 		c_uint16*6), 	# Number of latch-ups on each output 5V and +3V3 channel
							 				# Order[5V1 5V2 5V3 3.3V1 3.3V2 3.3V3]
							 				# Transmit as 5V1 first and 3.3V3 last
		("reset", 			c_uint8), 		# Cause of last EPS reset
		("bootcount", 		c_uint16), 		# Number of EPS reboots
		("sw_errors", 		c_uint16), 		# Number of errors in the eps software
		("ppt_mode", 		c_uint8),  		# 0 = Hardware, 1 = MPPT, 2 = Fixed SW PPT.
		("channel_status", 	c_uint8) 		# Mask of output channel status, 1=on, 0=off
											# MSB - [QH QS 3.3V3 3.3V2 3.3V1 5V3 5V2 5V1] - LSB
											# QH = Quadbat heater, QS = Quadbat switch		
	]

class eps_hk_t(BigEndianStructure):
	_fields_ = [
		("vboost", 				c_uint16*3),	# Voltage of boost converters [mV] [PV1, PV2, PV3]
		("vbatt", 				c_uint16),		# Voltage of battery [mV]
		("curin", 				c_uint16*3),	# Current in [mA]
		("cursun", 				c_uint16),		# Current from boost converters [mA]
		("cursys", 				c_uint16),		# Current out of battery [mA]
		("reserved1", 			c_uint16),		# Reserved for future use
		("curout", 				c_uint16*6),	# Current out (switchable outputs) [mA] 
		("output", 				c_uint8*8),		# Status of outputs**
		("output_on_delta", 	c_uint16*8), 	# Time till power on** [s] 
		("output_off_delta", 	c_uint16*8),	# Time till power off** [s]
		("latchup", 			c_uint16*6),	# Number of latch-ups
		("wdt_i2c_time_left", 	c_uint32),		# Time left on I2C wdt [s] 
		("wdt_gnd_time_left", 	c_uint32),		# Time left on I2C wdt [s] 
		("wdt_csp_pings_left", 	c_uint8*2),		# Pings left on CSP wdt
		("counter_wdt_i2c", 	c_uint32),		# Number of WDT I2C reboots 
		("counter_wdt_gnd", 	c_uint32),		# Number of WDT GND reboots 
		("counter_wdt_csp", 	c_uint32*2),	# Number of WDT CSP reboots 
		("counter_boot", 		c_uint32), 		# Number of EPS reboots
		("temp", 				c_int16*6),		# Temperatures [degC] [0 = TEMP1, TEMP2, TEMP3, TEMP4, BP4a, BP4b]
		("bootcause", 			c_uint8),		# Cause of last EPS reset
		("battmode", 			c_uint8),		# Mode for battery [0 = initial, 1 = undervoltage, 2 = safemode, 3 = nominal, 4=full]
		("pptmode", 			c_uint8),		# Mode of PPT tracker [1=MPPT, 2=FIXED]
		("reserved2", 			c_uint16)
	]
 
class eps_hk_vi_t(BigEndianStructure):
	_fields_ = [
		("vboost", 		c_uint16*3), 		# Voltage of boost converters [mV] [PV1, PV2, PV3]
		("vbatt", 		c_uint16), 			# Voltage of battery [mV]
		("curin", 		c_uint16*3), 		# Current in [mA]
		("cursun", 		c_uint16), 			# Current from boost converters [mA] 
		("cursys", 		c_uint16), 			# Current out of battery [mA]
		("reserved1", 	c_uint16)			# Reserved for future use
	]
	
class eps_hk_out_t(BigEndianStructure):
	_fields_ = [
		("curout", 			c_uint16*6),	# Current out (switchable outputs) [mA] 
		("output", 			c_uint8*8),		# Status of outputs**
		("output_on_delta", c_uint16*8), 	# Time till power on** [s]
		("output_off_delta",c_uint16*8), 	# Time till power off** [s]
		("latchup", 		c_uint16*6), 	# Number of latch-ups
	]

class eps_hk_wdt_t(BigEndianStructure):
	_fields_ = [
		("wdt_i2c_time_left", 	c_uint32), 	# Time left on I2C wdt [s] 
		("wdt_gnd_time_left", 	c_uint32),	# Time left on I2C wdt [s] 
		("wdt_csp_pings_left", 	c_uint8*2), # Pings left on CSP wdt
		("counter_wdt_i2c", 	c_uint32), 	# Number of WDT I2C reboots 
		("counter_wdt_gnd", 	c_uint32), 	# Number of WDT GND reboots 
		("counter_wdt_csp", 	c_uint32*2) # Number of WDT CSP reboots
	]

class eps_hk_basic_t(BigEndianStructure):
	_fields_ = [
		("counter_boot", 	c_uint32), 		# Number of EPS reboots
		("temp", 			c_int16*6), 	# Temperatures [degC] [0 = TEMP1, TEMP2, TEMP3, TEMP4, BATT0, BATT1]
		("bootcause", 		c_uint8), 		# Cause of last EPS reset
		("battmode", 		c_uint8), 		# Mode for battery [0 = initial, 1 = undervoltage, 2 = safemode, 3 = nominal, 4=full]
		("pptmode", 		c_uint8), 		# Mode of PPT tracker [1=MPPT, 2=FIXED]
		("reserved2", 		c_uint16)
	]

class eps_config_t(BigEndianStructure):
	_fields_ = [
		("ppt_mode", 					c_uint8), 		# Mode for PPT [1 = AUTO, 2 = FIXED]
		("battheater_mode", 			c_uint8), 		# Mode for battheater [0 = Manual, 1 = Auto]
		("battheater_low", 				c_int8), 		# Turn heater on at [degC]
		("battheater_high", 			c_int8), 		# Turn heater off at [degC]
		("output_normal_value", 		c_uint8*8), 	# Nominal mode output value
		("output_safe_value", 			c_uint8*8), 	# Safe mode output value
		("output_initial_on_delay", 	c_uint16*8), 	# Output switches: init with these on delays [s]
		("output_initial_off_delay", 	c_uint16*8), 	# Output switches: init with these on delays [s]
		("vboost", 						c_uint16*3) 	# Fixed PPT point for boost converters [mV]
	]

class eps_config2_t(BigEndianStructure):
	_fields_ = [
		("batt_maxvoltage", 		c_uint16),
		("batt_safevoltage", 		c_uint16),
		("batt_criticalvoltage", 	c_uint16),
		("batt_normalvoltage", 		c_uint16),
		("reserved1", 				c_uint32*2),
		("reserved2", 				c_uint8*4)
	]


# ----------------------------------------------HELPERS
# struct -> c_bytearray
def c_structToByteArray(s):
    byteArray = (c_byte*(sizeof(s))) ()
    spoint = pointer(s)
    cpoint = pointer(byteArray)
    memmove(cpoint, spoint, sizeof(s))
    return byteArray

# c_bytearray -> bytearray
def c_byteArrayToBytes(b):
    acc = []
    for n in b:
        acc += [n]
    return bytearray(acc)

# c_bytearray -> struct
def c_byteArrayToStruct(b, s):
	bpoint = pointer(b)
	struct = structMaker(s)
	spoint = pointer(struct)
	memmove(spoint, bpoint, sizeof(b))
	return struct

# takes an int and outputs a bytearray with the int divided into 
# [num] number of bytes
def toBytes(i, num):
	binary = bin(i)[2:]
	rem = len(binary) % 8 
	binary = '0'*(8-rem)+binary 	# add zeros to make it 8 bit
	size = len(binary)/8
	bytes = '0'*8*(num-size)+binary # add zeros to make it into right num of bytes

	acc = []
	for n in range(num):
		acc += [int(bytes[8*n:8*(n+1)], 2)]

	return bytearray(acc)

# bytearray -> c_bytearray
def c_bytesToByteArray(i):
	return (c_byte*len(i)) (*i) 

# struct -> c_bytearray -> bytearray
def c_structToBytes(s):
	return c_byteArrayToBytes(c_structToByteArray(s))

# bytearray -> c_bytearray -> struct
def c_bytesToStruct(i, s):
	return c_byteArrayToStruct(c_bytesToByteArray(i), s)

# bytearray -> int[]
def bytesToList(b):
	acc = []
	for n in b:
		acc += [n]
	return acc

# creates a struct given a string
def structMaker(s):
	if s == "hkparam_t": return hkparam_t()
	if s == "eps_hk_t": return eps_hk_t()
	if s == "eps_hk_vi_t": return eps_hk_vi_t()
	if s == "eps_hk_out_t": return eps_hk_out_t()
	if s == "eps_hk_wdt_t": return eps_hk_wdt_t()
	if s == "eps_hk_basic_t": return eps_hk_basic_t()
	return TestingStruct()

#----------------------------------------------POWER
# device address
POWER_ADDRESS   		= 0x00

# command registers
CMD_PING				= 0x01
CMD_REBOOT				= 0x04
CMD_GET_HK 	    		= 0x08
CMD_SET_OUTPUT  		= 0x09
CMD_SET_SINGLE_OUTPUT 	= 0x0A
CMD_SET_PV_VOLT			= 0x0B
CMD_SET_PV_AUTO			= 0x0C
CMD_SET_HEATER			= 0x0D
CMD_RESET_COUNTERS		= 0x0F
CMD_RESET_WDT			= 0x10
CMD_CONFIG_CMD			= 0x11
CMD_CONFIG_GET			= 0x12
CMD_CONFIG_SET			= 0x13
CMD_HARD_RESET			= 0x14
CMD_CONFIG2_CMD			= 0x15
CMD_CONFIG2_GET			= 0x16
CMD_CONFIG2_SET			= 0x17

# struct lengths
SIZE_HKPARAM_T 			= 44
SIZE_EPS_HK_T 			= 136
SIZE_EPS_HK_VI_T 		= 20
SIZE_EPS_HK_OUT_T 		= 64
SIZE_EPS_HK_WDT_T 		= 28
SIZE_EPS_HK_BASIC_T 	= 24
SIZE_ESP_CONFIG_T		= 58
SIZE_ESP_CONFIG2_T		= 20

class Power(object):
	# initializes power object with bus [bus] and device address [addr]
	def __init__(self, bus, addr, flags=0):
		self._pi = pigpio.pi()								# initialize pigpio object
		self._dev = self._pi.i2c_open(bus, addr, flags)		# initialize i2c device

	# writes byte list [values] to register [cmd]
	def write(self, cmd, values):
		self._pi.i2c_write_device(self._dev, bytearray([cmd]+values))

	# reads [bytes] number of bytes from the device and returns a bytearray
	def read(self, bytes):
		(x, r) = self._pi.i2c_read_device(self._dev, bytes)
		return r

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
		return c_bytesToStruct(array)

	# returns eps_hk_t struct
	def get_hk_2(self):
		self.write(CMD_GET_HK, [0x00])
		array = self.read(SIZE_EPS_HK_T)
		return c_bytesToStruct(array)

	# returns eps_hk_vi_t struct
	def get_hk_2_vi(self):
		self.write(CMD_GET_HK, [0x01])
		array = self.read(SIZE_EPS_HK_VI_T)
		return c_bytesToStruct(array)

	# returns eps_hk_out_t struct
	def get_hk_out(self):
		self.write(CMD_GET_HK, [0x02])
		array = self.read(SIZE_EPS_HK_OUT_T)
		return c_bytesToStruct(array)

	# returns eps_hk_wdt_t struct
	def get_hk_wdt(self):
		self.write(CMD_GET_HK, [0x03])
		array = self.read(SIZE_EPS_HK_WDT_T)
		return c_bytesToStruct(array)

	# returns eps_hk_basic_t struct
	def get_hk_2_basic(self):
		self.write(CMD_GET_HK, [0x04])
		array = self.read(SIZE_EPS_HK_BASIC_T)
		return c_bytesToStruct(array)

	# sets voltage output channels with bit mask: 
	# byte [1 byte] -> [NC NC 3.3V3 3.3V2 3.3V1 5V3 5V2 5V1]
	def set_output(self, byte):
		self.write(CMD_SET_OUTPUT, [byte])

	# sets a single output on or off:
	# channel [1 byte]  -> voltage = (0~5), BP4 heater = 6, BP4 switch = 7
	# value   [1 byte]  -> on = 1, off = 0
	# delay   [2 bytes] -> [seconds]
	def set_single_output(self, channel, value, delay):
		d = toBytes(delay)
		self.write(CMD_SET_SINGLE_OUTPUT, [channel, value]+[d[0], d[1]])

	# Set the voltage on the photo- voltaic inputs V1, V2, V3 in mV. 
	# Takes effect when MODE = 2, See SET_PV_AUTO.
	# Transmit voltage1 first and voltage3 last.
	# volt1~volt3 [2 bytes] -> value in mV
	def set_pv_volt(self, volt1, volt2, volt3):
		v = bytearray(6)
		v[0:1] = toBytes(volt1)
		v[2:3] = toBytes(volt2)
		v[4:5] = toBytes(volt3)
		self.write(CMD_SET_PV_VOLT, [v[0], v[1], v[2], v[3], v[4], v[5], v[6]])

	# Sets the solar cell power tracking mode:
	# mode [1 byte] ->
	# MODE = 0: Hardware default power point
	# MODE = 1: Maximum power point tracking
	# MODE = 2: Fixed software powerpoint, value set with SET_PV_VOLT, default 4V
	def set_pv_auto(self, mode):
		self.write(CMD_SET_PV_AUTO, [mode])

	# returns bytearray with heater modes
	# command 	[1 byte]  -> 0 = Set heater on/off (toggle?)
	# heater 	[1 byte]  -> 0 = BP4, 1 = Onboard, 2 = Both
	# mode 		[1 byte]  -> 0 = OFF, 1 = ON
	# return 	[2 bytes] -> heater modes
	def set_heater(self, command, heater, mode):
		self.write(CMD_SET_HEATER, [command, heater, mode])
		return self.read(2)

	# resets boot counter and WDT counters.
	def reset_counters(self):
		self.write(CMD_RESET_COUNTERS, [0x42])

	# resets (kicks) dedicated WDT.
	def reset_wdt(self):
		self.write(CMD_RESET_WDT, [0x78])

	# Use this command to control the config system.
	# cmd [1 byte] -> cmd = 1: Restore default config
	def config_cmd(self, command):
		self.write(CMD_CONFIG2_CMD, [command])

	# returns eps_config_t structure
	def config_get(self):
		self.write(CMD_CONFIG_GET, [])
		return c_bytesToStruct(self.read())

	# takes eps_config_t struct and sets configuration
	def config_set(self, struct):
		array = bytesToList(c_structToBytes(struct))
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
		return self.read(SIZE_ESP_CONFIG2_T)

	# Use this command to send config 2 to the P31
	# and save it (remember to also confirm it)
	def config2_set(self, struct):
		array = bytesToList(c_structToBytes(struct))
		self.write(CMD_CONFIG2_SET, array)

# ----------------------------------------------TESTS
# sending side
teststruct = eps_config2_t()
teststruct.field1 = 5
teststruct.field2 = 3
teststruct.field3 = 257
send = c_structToBytes(teststruct)
print len(send)

# receiving side
recv = c_bytesToStruct(send, "hkparam_t")
# print recv.field1
# print recv.field2
# print recv.field3


