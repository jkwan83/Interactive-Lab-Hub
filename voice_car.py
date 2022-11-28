#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer
import sys
import os
import wave
import json

def TextResults(self):
    res = json.loads(self.Result())
    return res['text']

if not os.path.exists("model"):
    print ("Please download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack as 'model' in the current folder.")
    exit (1)

wf = wave.open(sys.argv[1], "rb")
if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    print ("Audio file must be WAV format mono PCM.")
    exit (1)

model = Model("model")
# You can also specify the possible word list
rec = KaldiRecognizer(model, wf.getframerate(), '["oh one two three four five six seven eight nine zero jason", "[unk]"]')

while True:
    data = wf.readframes(1000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        #print(rec.Result())
        #test = rec.Result()
        test = rec.Result()
        print(f"' {test[14:-3]} '")
        if res == 'one':
            print("success")
    else:
        #print(rec.PartialResult())
        print("fail")
        test = rec.PartialResult()
        test = 
print(rec.FinalResult())
print("end")

