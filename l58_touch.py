""""
l58_touch.py - L58 Multi-Touch MicroPython Module
"""

_CLEAR = 0xab
_CLEAR_FLAGS = b'\xd0\x00\xab'
_READ_TOUCH = b'\xd0\x00'
_READ_MULTI = b'\xd0\x07'
_GOTO_SLEEP = b'\xd1\x05'
_WAKE_UP = b'\xd1\x06'

class L58Touch():
    """
    Class L58Touch
    """
    def __init__(self, bus, address):
        """
        Initialize the L58Touch controller.

        Parameters:
            bus: SoftI2C object
            address: I2C address of the touch controller
        """
        self.bus = bus
        self.address = address
        self.touch_data = []
        self.wakeup()
        self._clear_flags()

    def _cmd_read(self, write, nbytes):
        """
        Write bytearray `write` to the controller then read `nbytes` bytes from the controller
        and return the bytearray result.

        Parameters:
            write: bytearray to write to the controller
            nbytes: number of bytes to read from the controller

        Returns:
            bytearray: result of the read operation
        """
        self.bus.writeto(self.address, write)
        return self.bus.readfrom(self.address, nbytes)

    def _clear_flags(self):
        """
        Clear the touch controller flags
        """
        self.bus.writeto(self.address, _CLEAR_FLAGS)

    def _append_point(self, point, point_data):
        """
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
        """
        idx = point * 5
        s = (point_data[idx] &0x0f) >> 1
        f = (point_data[idx] >> 4) & 0x0f
        y = ((point_data[idx + 1] << 4) | (point_data[idx + 3] >> 4))
        x = ((point_data[idx + 2] << 4) | (point_data[idx + 3] & 0x0f))
        w = point_data[idx + 4]
        self.touch_data.append((f, x, y, w, s))

    def scan_point(self):
        """
        scan the touch controller for touch points and update the touch_data list

        Returns:
            int: number of points touched
        """
        point_data = []

        buffer = self._cmd_read(_READ_TOUCH, 7)
        if buffer[0] == _CLEAR:
            self._clear_flags()
            return 0

        point_data.extend(buffer[:5])

        point = buffer[5] & 0x0f
        buffer = self._cmd_read(_READ_MULTI, 5 * (point - 1) + 3 if point >1 else 2)
        self._clear_flags()

        point_data.extend(buffer)

        if point > 1:
            for i in range(point):
                self._append_point(i, point_data)
        else:
            self._append_point(0, point_data)
            point = 1

        return point

    def get_point(self):
        """
        Return the last point in the touch_data list.

        Point Format: (finger, x, y, weight, status)
            finger: order of the point touched
            x: x coordinate of the point touched
            y: y coordinate of the point touched
            weight: weight/pressure of the point touched (1-15)
            status: status of the point touched (3 pressed, 0 released)
                Not all points will report released status during multi-touch.
        """
        return self.touch_data.pop()

    def sleep(self):
        """
        Put the touch controller to sleep
        """
        self.bus.writeto(self.address, _GOTO_SLEEP)

    def wakeup(self):
        """
        Wake up the touch controller.
            Must be called to wake up the controller after sleep.

        """
        self.bus.writeto(self.address, _WAKE_UP)
