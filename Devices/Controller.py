'''
Emulates a standard controller with 2 joysticks, bumpers, triggers, 8 buttons and 2 joystick buttons.
'''

import usb_hid
import time

##################################################################################################
    
class ControllerInterface:
    def __init__(self):
        self.gamepad = None
        self.buttons = 0
        self.LEFT_X = 'lx'
        self.LEFT_Y = 'ly'
        self.RIGHT_X = 'rx'
        self.RIGHT_Y = 'ry'
        self.x = 0 # left x?
        self.y = 0 # left y?
        self.z = 0 # right x?
        self.rz = 0 # right y?
    
    def getGamepad(self) -> None:
        for device in usb_hid.devices:
            if device.usage_page == 0x01 and device.usage == 0x05:  # Generic Desktop, Gamepad
                self.gamepad = device
                break
        if not self.gamepad: raise RuntimeError("Gamepad HID device not found")
        return
    
    def setButton(self, button: int, value: int) -> None:
        '''
        Sets the button to either on (1) or off (0).
        '''
        if value: self.buttons |= (1 << button)
        else: self.buttons &= ~(1 << button)
        return
    
    # TODO
    def setJoystick(self, joystick: str, value: int) -> None:
        pass
    
    # TODO
    def moveJoystickBy(self, joystick: str, value: int) -> None:
        pass
    
    def resetButtons(self):
        '''
        Resets all of the buttons to off (0).
        '''
        self.buttons = 0
    
    def sendReport(self) -> None:
        '''
        Sends the report of the inputs to the connected device.
        '''
        report = bytearray(6)
        report[0] = self.buttons & 0xFF        # low byte  (buttons 1–8)
        report[1] = (self.buttons >> 8) & 0xFF # high byte (buttons 9–16)
        report[2] = self.x
        report[3] = self.y
        report[4] = self.z
        report[5] = self.rz
        self.gamepad.send_report(report, 4)
        return
