'''
Emulates a standard controller with 2 joysticks, bumpers, triggers, 8 buttons and 2 joystick buttons.
'''

import usb_hid

##################################################################################################
    
class ControllerInterface:
    def __init__(self):
        self.gamepad = None
        self.buttons = 0
        self.lx = 'lx'
        self.ly = 'ly'
        self.rx = 'rx'
        self.ry = 'ry'
        self.js_map = {
            self.lx: 0,
            self.ly: 0,
            self.rx: 0,
            self.ry: 0
        }
    
    def getGamepad(self) -> None:
        '''
        Gets the gamepad device established in boot.py.
        '''
        for device in usb_hid.devices:
            if device.usage_page == 0x01 and device.usage == 0x05:  # Generic Desktop, Gamepad
                self.gamepad = device
                break
        if not self.gamepad: raise RuntimeError("Gamepad HID device not found")
        return
    
    def setButton(self, button: int, value: int) -> None:
        '''
        Sets the button to either on (1) or off (0).
        The button can be acquired from your chosen file in ButtonMaps/
        '''
        if value: self.buttons |= (1 << button)
        else: self.buttons &= ~(1 << button)
        return
    
    def getButton(self, button: int) -> int:
        '''
        Gets the value of the inputted button, either on (1) or off (0).
        The button value can be acquired from your chosen file in ButtonMaps/
        '''
        return self.buttons & (1 << button)
    
    def getJoystick(self, joystick: str) -> int:
        '''
        Gets the value of the inputted joystick.
        '''
        value = self.js_map[joystick]
        if value >= 128 and value <= 255: value -= 255
        return value
    
    def modelInput(val: float) -> int:
        '''
        Takes in a number from 0-1 as an input, and converts it to -127 to 127.
        This just makes visualizing inputs easier, as opposed to doing the range from -127 to  127.
        '''
        return round(val * 127)
    
    def moveJoystick(self, joystick: str, value: int) -> None:
        '''
        Takes a value from -127 to 127 and moves the joystick respectively.
        '''
        # clamp value from -127 to 127
        if value < -127: value = -127
        elif value > 127: value = 127
        # if value negative (going left)
        if value < 0:
            # next, add 255 (since 255 + (negative) is range of 128 - 255, which is left -> middle)
            value = value + 255
            # next, make sure value stays below 255
            if value > 255: value = 255
        self.js_map[joystick] = value
        return
    
    def moveJoystickBy(self, joystick: str, value: int) -> None:
        '''
        Moves the joystick by the inputted amount, as opposed to fully setting it.
        Takes a value from -127 to 127.
        '''
        current = self.getJoystick(joystick)
        current += value
        self.moveJoystick(joystick, current)
        return 
    
    def resetJoysticks(self):
        for key in self.js_map.keys():
            self.js_map[key] = 0
        self.sendReport()
        return
        
    def resetButtons(self):
        '''
        Resets all of the buttons to off (0).
        '''
        self.buttons = 0
        self.sendReport()
    
    def sendReport(self) -> None:
        '''
        Sends the report of the inputs to the connected device.
        '''
        report = bytearray(6)
        
        # buttons - 2 bytes
        report[0] = self.buttons & 0xFF        # low byte  (buttons 1–8)
        report[1] = (self.buttons >> 8) & 0xFF # high byte (buttons 9–16)
        
        # joysticks - 4 bytes
        report[2] = self.js_map[self.lx]  # left X
        report[3] = self.js_map[self.ly]  # left Y
        report[4] = self.js_map[self.rx]  # right X
        report[5] = self.js_map[self.ry] # right Y
        
        # send report
        self.gamepad.send_report(report, 4)
        return
