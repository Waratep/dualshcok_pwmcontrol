from asyncore import file_dispatcher, loop
from evdev import InputDevice, categorize, ecodes
import time
import RPi.GPIO as IO          

dev = InputDevice('/dev/input/event0')

IO.setwarnings(False)           
IO.setmode (IO.BCM)       

IO.setup(19,IO.OUT)     # inB 2      
IO.setup(13,IO.OUT)     # inB 1   
IO.setup(26,IO.OUT)     # PWM B

IO.setup(16,IO.OUT)     #inA 2   
IO.setup(20,IO.OUT)     #inA 1
IO.setup(21,IO.OUT)     # PWM A

IO.setup(12,IO.OUT)     #eneble motor

p = IO.PWM(26,100)          
p2 = IO.PWM(21,100)          

p.start(0)                              
p2.start(0)  

IO.output(12,1)


IO.output(19,0)
IO.output(13,1)
IO.output(16,0)
IO.output(20,1)


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
    

def revers(x):
    if x == 0:
        IO.output(19,0)
        IO.output(13,1)
        IO.output(16,0)
        IO.output(20,1)
    else:
        IO.output(19,1)
        IO.output(13,0)
        IO.output(16,1)
        IO.output(20,0)

if __name__ == "__main__":
    
    initQueue()
    m1 = m2 = m3 = 0
    revs = 0
    resv2 = 0

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

                if event.type == ecodes.EV_KEY:
                    btn = categorize(event).keycode
                    if btn == 'BTN_Z':
                        revs += 1
                    if revs % 2 == 0 and resv2 == 0:
                        resv2 = 1
                        revers(resv2)
                    elif revs % 2 == 0 and resv2 == 1:
                        resv2 = 0
                        revers(resv2)

    except KeyboardInterrupt:
        print("ERROR")
        
