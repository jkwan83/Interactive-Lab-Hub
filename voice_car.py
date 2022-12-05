from vosk import Model, KaldiRecognizer
import sys
import os
import wave
import json
import RPi.GPIO as GPIO          
from time import sleep
import subprocess

in1 = 5 #change me to actual GPIO physical pin number
in2 = 6 #change me to actual GPIO physical pin number

in3 = 16 #change me to actual GPIO physical pin number
in4 = 20 #change me to actual GPIO physical pin number

#Set the intended pins as inputs/outputs for the GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)

GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)

#Set the initial outputs to be low so the motors are not in motion prematurely
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)

GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)

print("device is prepared to run")

if not os.path.exists("model"):
    print ("Please download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack as 'model' in the current folder.")
    exit (1)

wf = wave.open(sys.argv[1], "rb")
if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    print ("Audio file must be WAV format mono PCM.")
    exit (1)

model = Model("model")
# You can also specify the possible word list
rec = KaldiRecognizer(model, wf.getframerate(), '["sleep", "go", "back", "left", "right"]')
                      
while True:
    data = wf.readframes(3000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        print("success")
        
    test = rec.Result()
    voice = test[14:-3]
    print(test)
    print(voice)

    if voice == "go":
        print("go")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.HIGH)
        sleep(5)

    elif voice == "back":
        print("backward")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)
        sleep(5)

    elif voice == "left":
        print("left turn")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)
        sleep(3)

    elif voice == "right":
        print("right turn")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.HIGH)
        sleep(3)
    elif voice == "sleep":
        print("dont")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)
        exit()
    
print("done")
print("Say your next command")
#subprocess.call(['sh', './vosk_demo_mic.sh']) 