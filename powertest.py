from power import *

print "TESTING SEND/RECV"
struct = eps_config2_t()
struct.batt_maxvoltage = 10
struct.batt_safevoltage = 7
struct.batt_criticalvoltage = 5
struct.batt_normalvoltage = 8
struct.reserved1 = (10, 2)
struct.reserved2 = (1, 2, 3, 4)
byte = c_structToByteArray(struct)
for n in byte:
	print n
array = c_byteArrayToBytes(byte)

structend = c_bytesToStruct(array, "eps_config2_t")
print structend.batt_maxvoltage
print structend.batt_safevoltage
print structend.batt_criticalvoltage
print structend.batt_normalvoltage
print structend.reserved1[0]
print structend.reserved1[1]
print structend.reserved2[0]
print structend.reserved2[1]
print structend.reserved2[2]
print structend.reserved2[3]
print "end"