# -*- coding: utf-8 -*-
"""
@author: Nicole
"""

from dronekit import *
import time
import socket
import exceptions
import argparse

#Flight & Pre-Flight

#--------------------------------------------- Connect to drone
def connectMyCopter(): 
    
    parser = argparse.ArgumentParser(description='commands')
    parser.add_argument('--connect')
    args = parser.parse_args()   
    
    connection_string = args.connect
    vehicle = connect(connection_string, wait_ready=True)
    
    return vehicle


#----------------------------------------------- Arm drone & Takeoff
def arm_and_takeoff(aTargetAltitude): 
    while not vehicle.is_armable: #Block until vehicle is armed
        print("waiting for vehicle to arm...")
        time.sleep(1) 
        
    #Switch drone to guided mode (waits for commands)   
    vehicle.mode = VehicleMode("GUIDED")
    while vehicle.mode!="GUIDED": #Block until vehicle enters guided mode
        print("Waiting for vehicle to enter GUIDED mode")
        time.sleep(1)
        
    vehicle.armed=True
    
    while vehicle.armed==False: #Block until secondary arming phase is complete
        print("waiting for vehicle to arm...")
        time.sleep(1) 
    
    vehicle.simple_takeoff(aTargetAltitude) #Built in simple takeoff function
    
    while True:
        print("Current altitude: %d"%vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt>aTargetAltitude*.95:
            break
        time.sleep(1)
    
    print("Target altitude attained!")
    return None

#-------------------------------------------------- Mission Code

vehicle = connectMyCopter()

print("Taking off...")

vehicle.mode=VehicleMode("GUIDED")
arm_and_takeoff(20) #Take off to 20 meters
time.sleep(3)

print("End of mission...")
print("Version: %a"%vehicle.Version)

while True:
    time.sleep(3)
    
vehicle.close()
    
            
    