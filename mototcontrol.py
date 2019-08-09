from asyncore import file_dispatcher, loop
from evdev import InputDevice, categorize, ecodes
import time
import RPi.GPIO as IO          

dev = InputDevice('/dev/input/event0')

IO.setwarnings(False)           
IO.setmode (IO.BCM)        
IO.setup(19,IO.OUT)           
IO.setup(13,IO.OUT)           

p = IO.PWM(19,100)          
p2 = IO.PWM(13,100)          

p.start(0)                              
p2.start(0)         


def map( x,  in_min,  in_max,  out_min,  out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


if __name__ == "__main__":

    try:
        while 1:
            for event in dev.read_loop():
                if (event.type == ecodes.EV_ABS):
                    if event.code == 3: #break_left_motor
                        print(event.value)
                        p.ChangeDutyCycle(int(map(event.value,0,255,0,100)))
        
                    if event.code == 4: #break_right_motor
                        print(event.value)
                        p2.ChangeDutyCycle(int(map(event.value,0,255,0,100)))

                    # if event.code == 1:  #forward-left_motor
                    #     if event.value < 120:
                    #         print(event.value)
                    #     if event.value > 140:
                    #         print(event.value)
        
                    # if event.code == 5:  #forward-right_motor
                    #     if event.value < 120:
                    #         print(event.value)
                        
                    #     if event.value > 140:
                    #         print(event.value)


    except KeyboardInterrupt:
        print("ERROR")
        



















