import ctypes
from ctypes import *

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

# struct -> byte array
def c_structToByteArray(s):
    byteArray = (c_byte*(sizeof(s))) ()
    spoint = pointer(s)
    cpoint = pointer(byteArray)
    memmove(cpoint, spoint, sizeof(s))
    return byteArray

# byte array -> long[]
def c_byteArrayToLongList(b):
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

# byte array -> struct
def c_byteArrayToStruct(b, s):
	bpoint = pointer(b)
	struct = structMaker(s)
	spoint = pointer(struct)
	memmove(spoint, bpoint, sizeof(b))
	return struct

# takes an int and outputs a long list with the int divided into 
# [num] number of bytes
def toBytes(i, num):
	binary = bin(i)[2:]
	rem = len(binary) % 8 
	binary = '0'*(8-rem)+binary 	# add zeros to make it into bytes
	size = len(binary)/8
	bytes = '0'*8*(num-size)+binary # add zeros to make it into right num of bytes

	acc = []
	for n in range(num):
		acc += [int(bytes[8*n:8*(n+1)], 2)]

	return acc

# long[] -> byte array
def c_longListToByteArray(i):
	return (c_byte*len(i)) (*i) 

# struct -> byte array -> long[]
def c_structToLongList(s):
	return c_byteArrayToLongList(c_structToByteArray(s))

# long[] -> byte array -> struct
def c_longListToStruct(i, s):
	return c_byteArrayToStruct(c_longListToByteArray(i), s)

# ----------------------------------------------COMMANDS
POWER_ADDRESS = 0x00

# pings 1 byte value
def ping(value):
	cmd = 0x01
	write_i2c_block_data(POWER_ADDRESS, cmd, [value])
	return read_i2c_block_data(POWER_ADDRESS, cmd)

# reboot the system
def reboot():
	cmd = 0x04
	write_i2c_block_data(POWER_ADDRESS, cmd, [0x80, 0x07, 0x80, 0x07])

# returns hkparam_t struct
def get_hk_1():
	cmd = 0x08
	write_i2c_block_data(POWER_ADDRESS, cmd, [])
	recv = read_i2c_block_data(POWER_ADDRESS, cmd)
	return c_longListToStruct(recv, "hkparam_t")

# returns eps_hk_t struct
def get_hk_2():
	cmd = 0x08
	write_i2c_block_data(POWER_ADDRESS, cmd, [0x00])
	recv = read_i2c_block_data(POWER_ADDRESS, cmd)
	return c_longListToStruct(recv, "eps_hk_t")

# returns eps_hk_vi_t
def get_hk_2_vi():
	cmd = 0x08
	write_i2c_block_data(POWER_ADDRESS, cmd, [0x01])
	recv = read_i2c_block_data(POWER_ADDRESS, cmd)
	return c_longListToStruct(recv, "eps_hk_vi_t")

# returns eps_hk_out_t
def get_hk_out():
	cmd = 0x08
	write_i2c_block_data(POWER_ADDRESS, cmd, [0x02])
	recv = read_i2c_block_data(POWER_ADDRESS, cmd)
	return c_longListToStruct(recv, "eps_hk_out_t")

# returns eps_hk_wdt_t
def get_hk_wdt():
	cmd = 0x08
	write_i2c_block_data(POWER_ADDRESS, cmd, [0x03])
	recv = read_i2c_block_data(POWER_ADDRESS, cmd)
	return c_longListToStruct(recv, "eps_hk_wdt_t")

# returns eps_hk_basic_t
def get_hk_2_basic():
	cmd = 0x08
	write_i2c_block_data(POWER_ADDRESS, cmd, [0x04])
	recv = read_i2c_block_data(POWER_ADDRESS, cmd)
	return c_longListToStruct(recv, "eps_hk_basic_t")

# sets voltage output channels with bit mask: 
# byte [8] -> [NC NC 3.3V3 3.3V2 3.3V1 5V3 5V2 5V1]
def set_output(byte):
	cmd = 0x09
	write_i2c_block_data(POWER_ADDRESS, cmd, [byte])

# sets a single output on or off:
# channel [8]  -> voltage = (0~5), BP4 heater = 6, BP4 switch = 7
# value   [8]  -> on = 1, off = 0
# delay   [16] -> [seconds]
def set_single_output(channel, value, delay):
	cmd = 0x0A
	delay2bytes = toBytes(delay, 2)
	write_i2c_block_data(POWER_ADDRESS, cmd, [channel, value]+delay2bytes)

# sets voltage on photovoltaic inputs in mV
# takes effect when MODE = 2 (set_pv_auto)
def set_pv_volt(volt1, volt2, volt3):
	cmd = 0x0B
	v1 = toBytes(volt1, 2)
	v2 = toBytes(volt2, 2)
	v3 = toBytes(volt3, 2)
	write_i2c_block_data(POWER_ADDRESS, cmd, v1+v2+v3)

# Sets the solar cell power tracking mode:
# MODE = 0: Hardware default power point
# MODE = 1: Maximum power point tracking
# MODE = 2: Fixed software powerpoint, value set with SET_PV_VOLT, default 4V
def set_pv_auto(mode):
	cmd = 0x0C
	write_i2c_block_data(POWER_ADDRESS, cmd, [mode])

# Cmd = 0: Set heater on/off 
# Heater: 0 = BP4, 1= Onboard, 2 = Both
# Mode: 0 = OFF, 1 = ON
# returns long list with heater modes
def set_heater(command, heater, mode):
	cmd = 0x0D
	write_i2c_block_data(POWER_ADDRESS, cmd, [command, heater, mode])
	return get_heater()

# returns long list with heater modes
def get_heater():
	cmd = 0x0D
	return read_i2c_block_data(POWER_ADDRESS, cmd)

# resets boot counter and WDT counters.
def reset_counters():
	cmd = 0x0F
	write_i2c_block_data(POWER_ADDRESS, cmd, [0x42])

# resets (kicks) dedicated WDT.
def reset_wdt():
	cmd = 0x10
	write_i2c_block_data(POWER_ADDRESS, cmd, [0x78])

# Use this command to control the config system.
# cmd=1: Restore default config
def config_cmd(command):
	cmd = 0x11
	write_i2c_block_data(POWER_ADDRESS, cmd, [command])

# returns eps_config_t structure
def config_get():
	cmd = 0x12
	return read_i2c_block_data(POWER_ADDRESS, cmd)

# takes eps_config_t struct and sets configuration
def config_set(struct):
	cmd = 0x13
	longlist = c_structToLongList(struct)
	write_i2c_block_data(POWER_ADDRESS, cmd, longlist)

# Send this command to perform a hard reset of the P31,
# including cycling permanent 5V and 3.3V and battery outputs.
def hard_reset():
	cmd = 0x14
	write_i2c_block_data(POWER_ADDRESS, cmd, [])

# Use this command to control the config 2 system.
# cmd=1: Restore default config cmd=2: Confirm current config
def config2_cmd(command):
	cmd =  0x15
	write_i2c_block_data(POWER_ADDRESS, cmd, [command])

# Use this command to request the P31 config 2.
def config2_get():
	cmd = 0x16
	return read_i2c_block_data(POWER_ADDRESS, cmd)

# Use this command to send config 2 to the P31
# and save it (remember to also confirm it)
def config2_set(struct):
	cmd = 0x17
	longlist = c_structToLongList(struct)
	write_i2c_block_data(POWER_ADDRESS, cmd, longlist)

# ----------------------------------------------TESTS
# sending side
teststruct = TestingStruct()
teststruct.field1 = 5
teststruct.field2 = 3
teststruct.field3 = 257
send = c_structToLongList(teststruct)

# receiving side
recv = c_longListToStruct(send, "TestingStruct")
print recv.field1
print recv.field2
print recv.field3

longlist = [1, 5, 300]
array = c_longListToByteArray(longlist)
print array[1]
print bin(300)
print int('00101100', 2)


