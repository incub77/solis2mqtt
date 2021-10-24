import minimalmodbus

class Inverter(minimalmodbus.Instrument):
    def __init__(self, device, slave_address):
        super().__init__(device, slave_address)
        self.serial.baudrate = 9600
        self.serial.timeout = 0.35