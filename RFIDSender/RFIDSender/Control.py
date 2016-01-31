#! /usr/bin/env python3
"""
Bostin Technology  (see www.BostinTechnology.com)

For use with the RFIDReader module
Use the Android Application to read values

"""

from RFIDSender import DataAccessor
from RFIDSender import RFIDRoutines
from datetime import datetime
import time

sensor_acroynm = "PirFlx"
sensor_description = "RFID Tag Reader"


def GetSerialNumber():
    """
    Get the System Serial number to be used as the Device ID
    returns the Serial Number or '0000000000000000'
    """
    try:
        f = open('/proc/cpuinfo')
        for line in f:
            if line[0:6] == "Serial":
                cpuserial = line[10:26]
        f.close
    except:
        cpuserial = '0000000000000000'
    print ("CPU Serial Number : %s" % cpuserial)    #Added for Debug Purposes
    return int(cpuserial, 16)


def GenerateTimeStamp():
    """
    Generate a timestamp in the correct format
    dd-mm-yyyy hh:mm:ss.sss
    datetime returns a object so it needs to be converted to a string and then redeuced to 23 characters to meet format
    """
    now = str(datetime.now())
    #print ('Timestamp: %s' % now[:23]) #Debug
    return now[:23]
    

def Start():
    device_id = GetSerialNumber()
    print("Bostin Technology\nRFID Reader")
    print("\nDevice ID: %s" % device_id)
    print("\nTo Exit, CTRL-c\n\n")
    dbconn = DataAccessor.DynamodbConnection()

    serconn = RFIDRoutines.RFIDSetup()

    while True:
        # Read the tag
        tag_num = RFIDRoutines.ReadTagPageZero(serconn)
        
        if tag_num[0]:
            DataAccessor.WriteValues(dbconn, tag_num[1], GenerateTimeStamp(), device_id, "0001", sensor_acroynm, sensor_description)

# Only call the Start routine is the module is being called directly.
if __name__ == "__main__":
    Start()




