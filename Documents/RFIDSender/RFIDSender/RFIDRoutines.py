
"""
RFID Reader Routines to get the data from the tag.
"""


import wiringpi2
import time
import sys

# set for GPIO Pin to use based on the jumper connection
# GPIO_PIN = 1 # Jumper 1, also known as GPIO18
GPIO_PIN = 0 # Jumper 2, also known as GPIO17
# GPIO_PIN = 2 # Jumper 3, also known as GPIO21 (Rv 1) or GPIO27 (Rv 2)
# GPIO_PIN = 3 # Jumper 4, also known as GPIO22

def WaitForCTS():
    # continually monitor the selected GPIO pin and wait for the line to go low
    print ("Waiting for CTS") # Added for debug purposes
    while wiringpi2.digitalRead(GPIO_PIN):
        # do nothing
        time.sleep(0.1)   # was 0.001
    return

def ReadText(fd):
    # read the data back from the serial line and return it as a string to the calling function
    qtydata = wiringpi2.serialDataAvail(fd)
    print ("Amount of data: %d bytes" % qtydata) # Added for debug purposes
    response = ""
    while qtydata > 0:
        # while there is data to be read, read it back
        print ("Reading data back %d" % qtydata) #Added for Debug purposes
        response = response + chr(wiringpi2.serialGetchar(fd))
        qtydata = qtydata - 1   
    return response
    
def ReadInt(fd):
    # read a single character back from the serial line
    qtydata = wiringpi2.serialDataAvail(fd)
    print ("Amount of data: %s bytes" % qtydata)  # Added for debug purposes
    response = 0
    if qtydata > 0:
        print ("Reading data back %d" % qtydata) #Added for Debug purposes
        response = wiringpi2.serialGetchar(fd)
    return response

def RFIDSetup():
    # setup up the serial port and the wiringpi software for use
    # call setup for the wiringpi2 software
    response = wiringpi2.wiringPiSetup()
    # set the GPIO pin for input
    wiringpi2.pinMode(GPIO_PIN, 0)
    # open the serial port and set the speed accordingly
    fd = wiringpi2.serialOpen('/dev/ttyAMA0', 9600)

    # clear the serial buffer of any left over data
    wiringpi2.serialFlush(fd)
    
    if response == 0 and fd >0:
        # if wiringpi is setup and the opened channel is greater than zero (zero = fail)
        print ("PI setup complete on channel %d" %fd)      # Added for Debug purposes
    else:
        print ("Unable to Setup communications")
        sys.exit()
        
    return fd
    
def ReadTagStatus(fd):
    # read the RFID reader until a tag is present
    notag = True
    while notag:
        WaitForCTS()
        print ("Sending Tag Status Command") #Added for Debug purposes
        wiringpi2.serialPuts(fd,"S")
        time.sleep(0.1)
        ans = ReadInt(fd)
        print ("Tag Status: %s" % hex(ans)) # Added for Debug purposes
        if ans == int("0xD6", 16):
            # D6 is a positive response meaning tag present and read
            notag = False
    return

def ReadTagPageZero(fd):
    # read the tag page 00 command and return the value from the tag
    tag = False
    while not(tag):
        WaitForCTS()
        print ("Sending Tag Read Page Command") #Added for Debug purposes
        wiringpi2.serialPutchar(fd, 0x52)
        wiringpi2.serialPutchar(fd, 0x00)
        time.sleep(0.1)
        ans = ReadInt(fd)
        print ("Tag Status: %s" % hex(ans)) #Added for Debug purposes
        if ans == int("0xD6", 16):
            # Tag present and read
            tag = True
            print ("Tag Present") #Added for Debug purposes
            ans = ReadText(fd)
        else:
            ans = ""

    return tag, ans
