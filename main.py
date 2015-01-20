import RPi.GPIO as GPIO
import time
import Voting

cycle_delay = 0.5
bounce_time = 1000

led_pin = 18
buzzer_pin = 23
green_button_pin = 24
yellow_button_pin = 17
red_button_pin = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(buzzer_pin, GPIO.OUT)

def buzz(pitch, duration):
    period = 1.0 / pitch
    delay = period / 2
    cycles = int(duration * pitch)
    for i in range(cycles):
        GPIO.output(buzzer_pin, True)
        time.sleep(delay)
        GPIO.output(buzzer_pin, False)
        time.sleep(delay)

def led_on():
    GPIO.output(led_pin, True)

def led_off():
    GPIO.output(led_pin, False)

def green_pressed(channel):
    button_pressed(1)

def yellow_pressed(channel):
    button_pressed(0)

def red_pressed(channel):
    button_pressed(-1)

def button_pressed(rating):
    print('Button pressed: ' + str(rating))
    try:
        led_on()
        Voting.vote(rating)
    finally:
        buzz(500, 0.3)
        buzz(1000, 0.3)
        led_off()

GPIO.setup(green_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(green_button_pin, GPIO.FALLING, callback=green_pressed, bouncetime=bounce_time)
GPIO.setup(yellow_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(yellow_button_pin, GPIO.FALLING, callback=yellow_pressed, bouncetime=bounce_time)
GPIO.setup(red_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(red_button_pin, GPIO.FALLING, callback=red_pressed, bouncetime=bounce_time)

try:
    while (True):
        time.sleep(cycle_delay)
finally:
    GPIO.cleanup()

