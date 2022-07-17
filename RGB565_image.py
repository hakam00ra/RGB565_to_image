from ctypes.wintypes import RGB
from itertools import count
import serial
import cv2
import numpy as np
from PIL import Image 
serialPort = serial.Serial(port = "COM14", baudrate=115200,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
length = 76800 # 320*240
i = -1
s = ""      
def wait():
    global i
    while(1):
        if(serialPort.in_waiting > 0):    
            i += 1        
            s = serialPort.readline()
            s = s.split(b'\n')        
            if (s[0]==b'*'):
                i = -1
                return   
              
list = [None] * length
while(1):
    print("waiting\n")
    wait()
    while(i<length):
        if(serialPort.in_waiting > 0):    
            i += 1        
            s = serialPort.readline()
            s = s.split(b'\n')
            list[i] = s[0]

            if (i==length-1):                
                xdim = 320
                ydim = 240
                im = Image.new("RGB",(xdim,ydim))
                for y in range(ydim):
                    for x in range(xdim):
                        px = int.from_bytes(list[x*y], "big")
                        print(px)
                        im.putpixel((x,y),((px&0xF800) >> 8, (px&0x07E0) >> 3, (px&0x001F) <<3))                                                                
                im.show()
                break
