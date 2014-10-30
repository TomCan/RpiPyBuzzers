###############################
# buzzers.py
###############################
# author: Tom Cannaerts
#         mot @ tom . be
###############################
# This little python script can be used to turn a Raspberry PI
#   into a gameshow/quiz button system for all your howe quizzing needs
# 
# In my particular setup, there were 9 input buttons (1 reset button + 8 player buttons)
#   together with a 7 LED single digit numeric output screen and a sound buzzer, but you
#   should be able to tailor it to your needs quite easily.
#
#   pinButtons are the GPIO pins that serve as input buttons. The first pin in the array
#     is always the reset button
#
#   pinSignals are the output pins that need to be set to true is a given button has won
#     There is no reset button in there, so the first element of the array corresponds to
#     the second element of the pinButtons array
#
#   pinBUzzer and sleepBuzzer controls the pin and duration of the signal on that pin.  
#

import RPi.GPIO as GPIO
import time

# pin configuration
pinButtons = [23,3,5,7,11,13,15,19,21]
pinSignals = [8,10,12,16,18,22,24]
pinBuzzer = 26

# buzzer time
sleepBuzzer = 0.5


def getStatus():
    s = 0
    for i in range(len(pinButtons)):
        s += (2 ** i) * GPIO.input(pinButtons[i])
    return s

def setOutput(c):
    for pin in pinSignals:
        GPIO.output(pin, 0)
    for pin in btnOutput[c]:
        GPIO.output(pin, 1)

def soundBuzzer(sleep):
    if pinBuzzer > 0:
        GPIO.output(pinBuzzer, 1)
        time.sleep(sleep)
        GPIO.output(pinBuzzer, 0)

btnOutput = {
    '0': [8,24,18,16,12,10],
    '1': [24,18],
    '2': [8,24,22,12,16],
    '3': [8,24,22,18,16],
    '4': [10,24,22,18],
    '5': [8,10,22,18,16],
    '6': [8,10,22,12,18,16],
    '7': [8,24,18],
    '8': [8,24,18,16,12,10,22],
    '9': [8,24,18,16,10,22],
    'R': [8,24,18,12,10,22],
    '-': [22]
}


bMustReset = True

GPIO.setmode(GPIO.BOARD)

# GPIO.setup(btnReset, GPIO.IN)
for pin in pinButtons:
    print "Setting pin INPUT " + str(pin)
    GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

for pin in pinSignals:
    print "Setting pin OUTPUT " + str(pin)
    GPIO.setup(pin, GPIO.OUT)

if pinBuzzer > 0:
    GPIO.setup(pinBuzzer, GPIO.OUT)

status = getStatus()
setOutput('R')

print "Press reset button to continue"
for t in range(3):
    soundBuzzer(0.1)
    time.sleep(0.1)


while True:
    time.sleep(0.01)
    sts = getStatus()
    if sts != status:

        print "Status changed from " + str(status) + " to " + str(sts) + " (" + str(status ^ sts) + ")"

        if bMustReset:
            if (sts & 1) == 0:
                # reset pressed
		print "Reset button pressed"
		setOutput('-')
		soundBuzzer(sleepBuzzer)
		bMustReset = False
	else:

		for i in range(1, len(pinButtons)):
        	    if (sts & (2 ** i)) == 0:
                	print "Button " + str(i) + " pressed"
			print "Press reset button to continue"
                        setOutput(str(i))
                        soundBuzzer(sleepBuzzer)
			bMustReset = True

	status = sts
