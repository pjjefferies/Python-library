# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 21:51:36 2020

@author: PaulJ
"""


import time


# millis = lambda: int(round(time.time() * 1000))
millis = lambda: time.time() * 1000

lasttime = 0
interval = 2000  # 20 ms = 0.02 s
total_duration = 10  # seconds
start_time = time.time()  # seconds
last_time = start_time

while time.time() - start_time < total_duration:
    if ((millis() - lasttime) >= interval):
        lasttime = millis()
        time_exec = time.time()
        time_delt = time_exec - last_time
        last_time = time_exec
        error = (time_delt*1000-interval)/interval*100
        print('Now is the time, dur, err:', round(time_exec, 5),
              round(time_delt, 5), round(error,3))
