# -*- coding: utf-8 -*-

from __future__ import print_function
import time
from dronekit import *
import dronekit_sitl #Dronekit simulator
import argparse


#------------------------------------------------------------- Connect to drone
parser = argparse.ArgumentParser(description='commands')
parser.add_argument('--connect')
args = parser.parse_args()

connection_string = args.connect
sitl = None


if not connection_string: #Start Simulator if not already started
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()


print('Connecting to vehicle on: %s' % connection_string) #Connect to virtual aircraft
vehicle = connect(connection_string, wait_ready=True)


#-------------------------------------------------------------- Arm drone & Takeoff
def arm_and_takeoff(aTargetAltitude): 
    while not vehicle.is_armable: #Block until drone is armed
        print("waiting for vehicle to arm...")
        time.sleep(1) 
        
    #Guided Mode
    vehicle.mode = VehicleMode("GUIDED") #Switch drone to guided mode (waits for commands)   
    while vehicle.mode!="GUIDED": #Block until vehicle enters guided mode
        print("Waiting for vehicle to enter GUIDED mode")
        time.sleep(1)
    
    #Armed
    vehicle.armed=True
    
    #NOT Armed
    while vehicle.armed==False: #Block until secondary arming phase is complete
        print("waiting for vehicle to arm...")
        time.sleep(1) 
    
    #Takeoff
    vehicle.simple_takeoff(aTargetAltitude) #Built in simple takeoff function
    
    #Showing Current Altitude
    while True:
        print("Current altitude: %d"%vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt>aTargetAltitude*.95:
            break
        time.sleep(1)
    
    #Reached Target Altitude
    print("Target altitude attained!")
    return None


#----------------------------------------------------------------- Mission Code
arm_and_takeoff(10)

#setting speed
print("Setting target airspeed")
vehicle.airspeed = 5

#1st waypoint:right side of the river
print("Going to first waypoint... ")
waypoint1 = LocationGlobalRelative(-45.5, 149.1, 20)
vehicle.simple_goto(waypoint1)
time.sleep(30)

#2nd waypoint:leftside of the river
print("Heading to second waypoint... ")
waypoint2 = LocationGlobalRelative(-40.5, 149.2, 20)
vehicle.simple_goto(waypoint2, groundspeed=5)
time.sleep(30)

#Return Home: The Skillet
print("Returning to homepoint...")
vehicle.mode = VehicleMode("RTL") #Returns vehicle to take-off/home point

#Closing 
print("Closing vehicle object...")
vehicle.close()

#Shut down simulator
if sitl:
    sitl.stop()
