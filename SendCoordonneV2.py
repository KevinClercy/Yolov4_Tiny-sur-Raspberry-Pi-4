'''
Rédigé par K. Clercy, R. Lupien et M. Le Vergos
PFE2021
Avr. 2021
Aou. 2021
'''

import struct
from smbus import SMBus
import time

ManuelON = 0xA1
ManuelOFF = 0xA0


def TransformeIntEnMSBLSB(X,x,Y,y):
    stroutX = struct.pack('>h', X)
    stroutx = struct.pack('>h',x)
    stroutY = struct.pack('>h',Y)
    strouty = struct.pack('>h',y)
    
    c = stroutX + stroutx +stroutY + strouty

    print("chainedeCaratere MSB LSB : {}".format(c))

    liste = list(c)
    print("devenue une liste {} : type : {}".format(liste, type(liste)))

    liste2 = map(ord, liste)
    print("devenue une liste {} : type : {}".format(liste2, type(liste2)))
    
    return liste

def PT(value):
    print(type(value))

# def sendX(Xmax,Xmin):
#     bus.write_i2c_block_data(adr, 0xA1, writeNumber(Xmax))   
#     bus.write_i2c_block_data(adr, 0xA2, writeNumber(Xmin)) 

# def sendY(Ymax,Ymin):
#     bus.write_i2c_block_data(adr, 0xA3, writeNumber(Ymax))   
#     bus.write_i2c_block_data(adr, 0xA4, writeNumber(Ymin))   

def EnvoyerCoord(inCMD, inlist = [0,0,0,0,0,0,0,0]):
    print("inEnvoyerCommand :{} ".format(inCMD))
    bus.write_i2c_block_data(adr, inCMD, inlist)   

def ModeManuelON():
    bus.write_i2c_block_data(adr,ManuelON,[0,0,0,0,0,0,0,0])

def ModeManuelOFF():
    bus.write_i2c_block_data(adr,ManuelOFF,[0,0,0,0,0,0,0,0])


bus = SMBus(1)
adr = 0x44

#time.sleep(0.010)
#test = TransformeIntEnMSBLSB(330,330,100,0)
#print(test)

#EnvoyerCoord(0xA7, test)
#print("coliss")

