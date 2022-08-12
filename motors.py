#!/usr/bin/env python3
# We need proper keyboard library to detect keypresses

import RPi.GPIO as GPIO
from datetime import datetime
import time

#used for print statement to debug
debug = True

#to use with sensor driven:manual or ai driven:auto
modes = ["manual","auto"]
mode = modes[0]

def setup():
    # Set PWM Pin with frequency of 1khz
    frequency = 5000
    
    GPIO.setmode(GPIO.BCM)
    
    # For Right Motor
    Right_CW = 13
    Right_CCW = 6
    ENRight = 20
    
    # For Left Motor
    Left_CW = 26
    Left_CCW = 19
    ENLeft = 21
    
    # IR Sensors
    sensor_1 = 4
    sensor_2 = 17

    
    # Pin Setup
    # Setup for right motors
    GPIO.setup(Right_CW,GPIO.OUT)
    GPIO.setup(Right_CCW,GPIO.OUT)
    GPIO.setup(ENRight,GPIO.OUT)
    
    # Setup for left motors
    GPIO.setup(Left_CW,GPIO.OUT)
    GPIO.setup(Left_CCW,GPIO.OUT)
    GPIO.setup(ENLeft,GPIO.OUT)
    
    # Setup for Sensors
    GPIO.setup(sensor_1,GPIO.IN)
    GPIO.setup(sensor_2,GPIO.IN)
    
    # PWM Configurations 
    Right_PWM = GPIO.PWM(ENRight,frequency)
    Left_PWM = GPIO.PWM(ENLeft,frequency)
    
    # Intialise with 0
    # One time initialisation for PWM, .start(), used to set an intial PWM value
    Right_PWM.start(0)
    Left_PWM.start(0)
    
    GPIO.setwarnings(False)
        
    return Right_PWM, Right_CW, Right_CCW, Left_PWM, Left_CCW, Left_CW, sensor_1, sensor_2


def movement(move_direction, Right_PWM, Left_PWM, Right_CW, Left_CW,Right_CCW,Left_CCW,R_PWM_value = 0,L_PWM_value=0):
    
    # Used technique: All GPIO pins false, conditionally we will make GPIO pins True according to our convenience 
    GPIO.output(Left_CW,False)
    GPIO.output(Right_CW,False)
    GPIO.output(Left_CCW,False)
    GPIO.output(Right_CCW,False)
    
    if(move_direction == "STOP"):
            Right_PWM.ChangeDutyCycle(R_PWM_value)
            Left_PWM.ChangeDutyCycle(L_PWM_value)
            
    elif(move_direction == "RIGHT"):
        
            # Set Right PWM to 0 and Left PWM to 30
            # Enable left motors on
            Right_PWM.ChangeDutyCycle(R_PWM_value)
            Left_PWM.ChangeDutyCycle(L_PWM_value)
            GPIO.output(Right_CW,True)
            GPIO.output(Left_CCW,True)      
            
            
    elif(move_direction == "LEFT"):
            # Set Right PWM to 0 and Left PWM to 30
            # Enable left motors on
            Right_PWM.ChangeDutyCycle(R_PWM_value)
            Left_PWM.ChangeDutyCycle(L_PWM_value)
            
            GPIO.output(Left_CW,True)
            GPIO.output(Right_CCW,True)
            
    elif(move_direction == "FORWARD"):
        
            Left_PWM.ChangeDutyCycle(L_PWM_value)
            Right_PWM.ChangeDutyCycle(R_PWM_value)
            GPIO.output(Left_CW,True)
            GPIO.output(Right_CW,True)
        
        
    # match move_direction:
    #     case "STOP":
    #         # Set Both PWMs to 0 to stop
    #         Right_PWM.ChangeDutyCycle(R_PWM_value)
    #         Left_PWM.ChangeDutyCycle(L_PWM_value)

    #     case "RIGHT":
    #         # Set Right PWM to 0 and Left PWM to 30
    #         # Enable left motors on
    #         Right_PWM.ChangeDutyCycle(R_PWM_value)
    #         Left_PWM.ChangeDutyCycle(L_PWM_value)
    #         GPIO.output(Left_CW,True)
        
    #     case "LEFT":
    #         # Set Left PWM to 0 and Right PWM to 30
    #         # Enable right motors on
    #         Right_PWM.ChangeDutyCycle(R_PWM_value)
    #         Left_PWM.ChangeDutyCycle(L_PWM_value)
    #         GPIO.output(Right_CW,True)

    #     case "FORWARD":
    #         # Set Both PWMs to 30 for forward
    #         Left_PWM.ChangeDutyCycle(L_PWM_value)
    #         Right_PWM.ChangeDutyCycle(R_PWM_value)
    #         GPIO.output(Left_CW,True)
    #         GPIO.output(Right_CW,True)
       
        
        
        
    



if __name__ == "__main__":
    
    delay_in_turn = 0.05  #Delay produced for coarse correction of track
    
    Right_PWM, Right_CW, Right_CCW, Left_PWM, Left_CCW, Left_CW, sensor_1, sensor_2 = setup()
    
    try:
        while True:
            time.sleep(0.05) #Delay produced to eliminate random zero values of sensors
            
            #read and print sensor data in manual mode
            if mode == "manual":
                sensor_1_data = GPIO.input(sensor_1)
                sensor_2_data = GPIO.input(sensor_2)
                print(f"Sensor 1 Data : {sensor_1_data}") if debug else None
                print(f"Sensor 2 Data : {sensor_2_data}") if debug else None

            #for now vehicle can be in two modes i.e auto or manual   
            if(mode == "manual"):
                if(sensor_1_data == 0 and sensor_2_data == 0):
                        movement("STOP",Right_PWM,Left_PWM,Right_CW,Left_CW,Right_CCW,Left_CCW,R_PWM_value = 0,L_PWM_value=0)
                elif(sensor_1_data == 1 and sensor_2_data == 0):
                        movement("RIGHT",Right_PWM,Left_PWM,Right_CW,Left_CW,Right_CCW,Left_CCW,R_PWM_value = 80,L_PWM_value=80)
                        time.sleep(delay_in_turn*2)
                elif(sensor_1_data == 0 and sensor_2_data == 1):
                        movement("LEFT",Right_PWM,Left_PWM,Right_CW,Left_CW,Right_CCW,Left_CCW,R_PWM_value = 80,L_PWM_value=80)
                        time.sleep(delay_in_turn*2)
                else:
                        movement("FORWARD",Right_PWM,Left_PWM,Right_CW,Left_CW,Right_CCW,Left_CCW,R_PWM_value = 35,L_PWM_value=35)
            elif(mode == "auto"):
                pass
                
            # match mode:
            #     #in manual mode : forward left right stop condition can exit , later backward can be implemented
            #     case "manual":
            #         if(sensor_1_data == 0 and sensor_2_data == 0):
            #             movement("STOP",Right_PWM,Left_PWM,Right_CW,Left_CW,R_PWM_value = 0,L_PWM_value=0)
            #         elif(sensor_1_data == 1 and sensor_2_data == 0):
            #             movement("RIGHT",Right_PWM,Left_PWM,Right_CW,Left_CW,R_PWM_value = 0,L_PWM_value=30)
            #         elif(sensor_1_data == 0 and sensor_2_data == 1):
            #             movement("LEFT",Right_PWM,Left_PWM,Right_CW,Left_CW,R_PWM_value = 30,L_PWM_value=0)
            #         else:
            #             movement("FORWARD",Right_PWM,Left_PWM,Right_CW,Left_CW,R_PWM_value = 30,L_PWM_value=30)
                
            #     case "auto":
            #         pass

            # On keyboard press, safely exit the program
                
    except Exception as e:
        print(e)
        GPIO.cleanup()
        
    finally:
        print("Program exits successfully")