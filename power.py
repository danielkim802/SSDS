import ctypes
from ctypes import *

class TestingStruct(BigEndianStructure):
    _fields_ = [
        ("field1", c_uint8),
        ("field2", c_uint8),
        ("field3", c_uint16)
    ]

# class I2CHandler(object):
#   def I2CHandler():
#       self.bus = smbus.SMBus(0)

#   def writeStruct(addr, port, val):
#       # value is a pointer to a struct
#       self.bus.write_byte_data(addr, port, val.contents)


# sending side
struct = TestingStruct()
struct.field1 = 5
struct.field2 = 3
struct.field3 = 257


# converts struct into bytearray
def c_structToByteArray(s):
    byteArray = (c_byte*(sizeof(s))) ()
    cpoint = pointer(byteArray)
    spoint = pointer(s)
    memmove(cpoint, spoint, sizeof(s))
    return byteArray

# converts bytearray to int
def c_byteArrayToInt(b):
    acc = 0
    for n in b:
        acc = (acc << 8) | n
    return acc

# converts bytearray into struct
def c_byteArrayToStruct(b):
	bpoint = pointer(b)
	struct = TestingStruct()
	spoint = pointer(struct)
	memmove(spoint, bpoint, sizeof(b))
	return struct

send = c_structToByteArray(struct)
recv = c_byteArrayToStruct(send)
print recv.field3








