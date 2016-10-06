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

# returns a struct given a string
def structMaker(s):
	if s == "TestingStruct": return TestingStruct()
	if s == "hkparam_t": return hkparam_t()
	return None

# byte array -> struct
def c_byteArrayToStruct(b, s):
	bpoint = pointer(b)
	struct = structMaker(s)
	spoint = pointer(struct)
	memmove(spoint, bpoint, sizeof(b))
	return struct

# long[] -> byte array
def c_longListToByteArray(i):
	return (c_byte*len(i)) (*i) 

# struct -> byte array -> long[]
def c_structToLongList(s):
	return c_byteArrayToLongList(c_structToByteArray(s))

# long[] -> byte array -> struct
def c_longListToStruct(i, s):
	return c_byteArrayToStruct(c_longListToByteArray(i), s)

def get_hk_1():
	address = 0x00
	cmd = 0x08
	write_i2c_block_data(address, cmd, [])
	recv = read_i2c_block_data(address, cmd)
	return c_longListToStruct(recv, "hkparam_t")

# TESTS
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



