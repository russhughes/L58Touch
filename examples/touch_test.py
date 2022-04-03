from time import sleep
from machine import Pin, SoftI2C
import l58_touch

tp = l58_touch.L58Touch(SoftI2C(Pin(14), Pin(15)), 90)
while True:
    for _ in range(tp.scan_point()):
        if touch_point := tp.get_point():
            print(touch_point)
    sleep(0.1)
