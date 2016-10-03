import ctypes
from ctypes import *
import pickle

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
def c_makeByteArray(s):
    byteArray = (c_byte*(sizeof(s))) ()
    cpoint = pointer(byteArray)
    spoint = pointer(s)
    memmove(cpoint, spoint, sizeof(struct))
    return byteArray

# converts bytearray to hex
def c_byteArrayToHex(b):
    acc = 0
    for n in b:
        acc = (acc << 8) | n
    return acc

byteArray = c_makeByteArray(struct)
b = c_byteArrayToHex(byteArray)

print hex(b)


# receiving side
byteArray2 = (c_byte*4) (b)
print byteArray2[0]
bpoint = pointer(byteArray2)
struct2 = TestingStruct()
s2point = pointer(struct2)

memmove(s2point, bpoint, sizeof(byteArray2))

print struct2.field2






