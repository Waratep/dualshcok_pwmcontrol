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

avg_motor1 = []
avg_motor2 = []


def map( x,  in_min,  in_max,  out_min,  out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def initQueue():
    for i in range(10):
        avg_motor1.append(0)
        avg_motor2.append(0)

def calavg(data):
    x = 0
    for i in range(10):
        x += data[i]
    x = x / 10
    return x

def motor1(x,y):
    avg_motor1.pop(0)
    avg_motor1.append(x)
    if y < 0:
        x = int(map(calavg(avg_motor1),0,255,0,100) - abs(y))
    else:
        x = int(map(calavg(avg_motor1),0,255,0,100))
    if x > 100: 
        x = 100
    if x < 0:
        x = 0

    p.ChangeDutyCycle(x)

def motor2(x,y):
    avg_motor2.pop(0)
    avg_motor2.append(x)

    if y > 0:
        x = int(map(calavg(avg_motor2),0,255,0,100) - abs(y))
    else:
        x = int(map(calavg(avg_motor1),0,255,0,100))

    if x > 100: 
        x = 100
    if x < 0:
        x = 0
    p2.ChangeDutyCycle(x)
    

if __name__ == "__main__":
    
    initQueue()
    m1 = m2 = m3 = 0
    
    try:
        while 1:
            for event in dev.read_loop():
                motor1(m2,m3)
                motor2(m2,m3)
                if (event.type == ecodes.EV_ABS):
                    if event.code == 3: 
                        m1 = event.value
        
                    if event.code == 4: 
                        m2 = event.value

                    if event.code == 0: 
                        m3 = map(event.value,0,255,-100,100)



    except KeyboardInterrupt:
        print("ERROR")
        



















