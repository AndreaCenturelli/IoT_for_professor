from sensor_emulators.gps_emulator import GPSEmulator
from sensor_emulators.collisionDetector_emulator import CollisionDetectorEmulator
from sensor_emulators.speed_emulator import SpeedEmulator
from sensor_emulators.heartBeat_emulator import HeartBeatEmulator

import serial
import time
import msvcrt
import json

def makeSerialConnections(ports):
    serialConnections = []
    count = 0
    for port in ports:
        ser = serial.Serial(
            port,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
            )

        serialConnections.append(ser)

        if serialConnections[count].isOpen():
            print(serialConnections[count].name + 'is open..')
        count = count + 1
        
    return serialConnections

if __name__ == "__main__":
	gpsLoc = GPSEmulator()
	collisonDetector = CollisionDetectorEmulator()
	speed = SpeedEmulator()
	heartBeat = HeartBeatEmulator()

	ports = ['COM3', 'COM7', 'COM9', 'COM11']
	
	serialConnections = makeSerialConnections(ports)

	print("Cycle emulator started:\n")

	print('Type any of the following command:\n\
    	Press "W" to  increase the speed.\n\
    	Press "S" to decrease the speed\n\
    	Press "P" to park the bike\n\
    	Press "T" to trigger/swith off the simulated collison\n\
    	Press "Z to exit the emulator" ')

	start_time = time.time()

	while True:
		end_time = time.time()
		if msvcrt.kbhit():
			key_stroke = msvcrt.getch()
			print(key_stroke)   # will print which key is pressed
			char = ord(key_stroke)
			if char == 119 or char == 87:
				speed.increaseSpeed()
				heartBeat.increaseHeartBeat()
				print(speed.sendValue())
				print(heartBeat.sendValue())
			elif char == 115 or char == 83:
				speed.decreaseSpeed()
				heartBeat.decreaseHeartBeat()
				print(speed.sendValue())
				print(heartBeat.sendValue())
			elif char == 116 or char == 84:
				collisonDetector.changeValue(not collisonDetector.collision)
				speed.park()
				heartBeat.park()
				print(collisonDetector.sendValue())
			elif char == 112 or char == 80:
				speed.park()
				heartBeat.park()
			elif char == 122 or char == 90:
				break

		gpsData = gpsLoc.locationGenerator() + '\n'
		collisonData = collisonDetector.sendValue() + '\n'
		speedData = speed.sendValue() + '\n'
		heartRateData= heartBeat.sendValue() + '\n'
		
		serialConnections[0].write(gpsData.encode('ascii'))
		serialConnections[1].write(collisonData.encode('ascii'))
		serialConnections[2].write(speedData.encode('ascii'))
		serialConnections[3].write(heartRateData.encode('ascii'))
		
		if end_time - start_time >=6 and not collisonDetector.collision:
			gpsLoc.index = gpsLoc.index + 1
			start_time = time.time()

		time.sleep(0.5)
		

		


