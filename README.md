# l58_touch.py - L58 Multi-Touch MicroPython Module

Tested on LilyGo-EPD47 T5 E-Paper 4.7" running MicroPython v1.18

## Class L58Touch

### L58Touch(bus, address):

    Initialize the L58Touch controller.

    Parameters:
        bus: SoftI2C object
        address: I2C address of the touch controller

### Private Methods

#### _cmd_read(self, write, nbytes):

    Write bytearray `write` to the controller then read `nbytes` bytes from the controller
    and return the bytearray result.

    Parameters:
        write: bytearray to write to the controller
        nbytes: number of bytes to read from the controller

    Returns:
        bytearray: result of the read operation


#### _clear_flags(self):

    Clear the touch controller flags


#### _append_point(self, point, point_data):

    Parse `point` from `point_data` and append it to the touch_data list as a tuple.

    Parameters:
        point: point number
        point_data: list of bytes from the controller

    Format of `touch_data`: (finger, x, y, weight, status)
        finger: order of the point touched
        x: x coordinate of the point touched
        y: y coordinate of the point touched
        weight: weight/pressure of the point touched (1-15)
        status: status of the point touched (3 pressed, 0 released)
            Not all points will report released status during multi-touch.

### Public Methods

#### scan_point(self):

    scan the touch controller for touch points and update the touch_data list

    Returns:
        int: number of points touched


#### get_point(self):

    Return the last point in the touch_data list.

    Point Format: (finger, x, y, weight, status)
        finger: order of the point touched
        x: x coordinate of the point touched
        y: y coordinate of the point touched
        weight: weight/pressure of the point touched (1-15)
        status: status of the point touched (3 pressed, 0 released)
            Not all points will report released status during multi-touch.


#### sleep(self):

    Put the touch controller to sleep


#### wakeup(self):

    Wake up the touch controller.
        Must be called to wake up the controller after sleep.


## Example

```python
from time import sleep
from machine import Pin, SoftI2C
import l58_touch

tp = l58_touch.L58Touch(SoftI2C(Pin(14), Pin(15)), 90)
while True:
    for _ in range(tp.scan_point()):
        if touch_point := tp.get_point():
            print(touch_point)
    sleep(0.1)
```