#!/usr/bin/env python3

from breezycreate2 import Robot
import math
import time

# Triples: (note,duration,pause)
MELODY1 = [('C4', 10, 0.2),
         ('C4', 13, 0.26),
         ('C4', 15, 0.3),
         ('F4', 45, 0.9),
         ('C4', 45, 0.9),
         ('F4', 10, 0.2),
         ('C4', 13, 0.26),
         ('F4', 15, 0.3),
         ('A4', 45, 0.9),
         ('F4', 45, 0.9),
         ('A4', 10, 0.2),
         ('F4', 13, 0.26),
         ('A4', 15, 0.3),
         ('C5', 45, 0.9),
         ('C4', 45, 0.9),
         ('A4', 10, 0.2),
         ('F4', 13, 0.26),
         ('A4', 15, 0.3),
         ('C5', 45, 2.2)]

# Another popular melody
MELODY2 = [('C4', 11, 0.3),
            ('C4', 11, 0.3),
            ('C4', 11, 0.3),
            ('C4', 32, 0.7),
            ('G4', 32, 0.7),
            ('F4', 11, 0.3),
            ('E4', 11, 0.3),
            ('D4', 11, 0.3),
            ('C5', 64, 1.2),
            ('G4', 40, 0.7),
            ('F4', 11, 0.3),
            ('E4', 11, 0.3),
            ('D4', 11, 0.3),
            ('C5', 64, 1.2),
            ('G4', 40, 0.7),
            ('F4', 11, 0.3),
            ('E4', 11, 0.3),
            ('F4', 11, 0.3),
            ('D4', 64, 2)]

distance_left = 0
distance_right = 0
radius_change = 32757

# Create a Create2. This will automatically try to connect to your robot over serial
bot = Robot()

# Play the melody1
for triple in MELODY1:
    bot.playNote(triple[0], triple[1])
    time.sleep(triple[2])

for i in range(0, 6, 1):

    # Get the Create2 right wheel distance
    if bot.robot.get_packet(44) is True:
        right_wheel = bot.robot.sensor_state['right encoder counts'] - 10191
        distance_right = right_wheel * math.pi * 72.0 / 508.8

    # Get the Create2 left wheel distance
    if bot.robot.get_packet(43) is True:
        left_wheel = bot.robot.sensor_state['left encoder counts'] - 34877
        distance_left = left_wheel * math.pi * 72.0 / 508.8

    # Calculate the angle in radians
    create2_angle = (distance_right - distance_left) / 235.00

    # Introducing PID algorithm.
    angle_adjust = bot.robot.pid_adjust.update(create2_angle)

    # Calculate the radius
    if abs(create2_angle + angle_adjust) != 0:
        radius_change = max(distance_right, distance_left) / abs(create2_angle + angle_adjust) - 117.50

    # Tell the Create2 to go forward
    # if create2_angle > 0:
        # bot.robot.drive(50, -radius_change)
        # time.sleep(1)
    # elif create2_angle < 0:
        # bot.robot.drive(50, radius_change)
        # time.sleep(1)
    bot.robot.drive(50, 32767)
    time.sleep(5)

# Close the connection
bot.close()
