from ib_insync import *

ib = IB()
ib.connect()

print(ib.orders())