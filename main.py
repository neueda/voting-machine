#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import sqlite3
from serial import SerialException
import rfIdReader
import os

cycle_delay = 0.5
bounce_time = 1000

led_pin = 18
buzzer_pin = 23
green_button_pin = 24
yellow_button_pin = 17
red_button_pin = 22

pressed = False

rf_id = ''
last_rf_id_read = time.time()
time_frame = 5

db_path = os.path.dirname(os.path.abspath(__file__)) + '/user_votes.db'

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

def save_to_db(rf_id, rating):
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        cur.execute("insert into user_votes(rf_id, vote) values (?, ?)", (rf_id, rating))
        conn.commit()
    except Exception as exception:
        print('Unexpected error during db insert! ' + exception.message)
        raise
    finally:
        conn.close()

def button_pressed(rating):
    global pressed
    global rf_id
    
    if pressed or not rf_id:
        return

    # checks if there was card code recently read.
    # time.time() returns time in seconds, time_frame defined in seconds as well
    if time.time() - last_rf_id_read > time_frame:
        rf_id = ''
        return

    pressed = True
    
    print('Button pressed: ' + str(rating))

    try:
        save_to_db(rf_id, rating)
        led_on()
    finally:
        rf_id = ''
        buzz(300, 0.1)
        buzz(500, 0.1)
        buzz(300, 0.1)
        buzz(500, 0.1)
        buzz(300, 0.1)
        buzz(500, 0.1)
        led_off()
        pressed = False

GPIO.setup(green_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(green_button_pin, GPIO.FALLING, callback=green_pressed, bouncetime=bounce_time)
GPIO.setup(yellow_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(yellow_button_pin, GPIO.FALLING, callback=yellow_pressed, bouncetime=bounce_time)
GPIO.setup(red_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(red_button_pin, GPIO.FALLING, callback=red_pressed, bouncetime=bounce_time)

try:
    while True:
        try:
            rf_id = rfIdReader.rf_id_input()
            last_rf_id_read = time.time()
        except SerialException as e:
            print('Error during rfId card read! ' + e.message)
            time.sleep(cycle_delay)
finally:
    GPIO.cleanup()

