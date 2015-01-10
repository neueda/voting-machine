import RPi.GPIO as GPIO
import time

cycle_delay = 0.5
led_pin = 18
buzzer_pin = 23
button_pin = 24

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

def button_callback(channel):
    print('Button pressed')
    led_on()
    buzz(500, 0.3)
    buzz(1000, 0.3)
    led_off()

GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=button_callback)

while (True):
    time.sleep(cycle_delay)

