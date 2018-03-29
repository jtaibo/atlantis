#!/usr/bin/python3
#

import lcd_i2c
import time # TESTING

line_addr = [ lcd_i2c.LCD_LINE_1, lcd_i2c.LCD_LINE_2 ]

class Display:

    def __init__(self):
        lcd_i2c.lcd_init()

    def printMessage(self, text, line=0):
#        print(text)
        lcd_i2c.lcd_string(text, line_addr[line])

    def clear(self):
        lcd_i2c.lcd_byte(0x01,lcd_i2c.LCD_CMD)

    def setBacklight(self, on):
        lcd_i2c.lcd_backlight(on)


if __name__ == '__main__':     # Testing code
    dpy = Display()
    time.sleep(1)
    dpy.clear()
    time.sleep(1)
    dpy.printMessage("Backlight on", 0)
    dpy.setBacklight(True)
    time.sleep(1)
    dpy.printMessage("Backlight OFF", 0)
    dpy.setBacklight(False)
    time.sleep(1)
    
