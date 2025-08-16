import usb_hid
import time

##################################################################################################
    
class ControllerInterface:
    def __init__(self):
        self.gamepad = None
        self.buttons = 0
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
        if value: self.buttons |= (1 << button)
        else: self.buttons &= ~(1 << button)
        return
        
    def resetButtons(self): self.buttons = 0
    
    def sendReport(self) -> None:
        report = bytearray(6)
        report[0] = self.buttons & 0xFF        # low byte  (buttons 1–8)
        report[1] = (self.buttons >> 8) & 0xFF # high byte (buttons 9–16)
        report[2] = self.x
        report[3] = self.y
        report[4] = self.z
        report[5] = self.rz
        self.gamepad.send_report(report, 4)
        return
