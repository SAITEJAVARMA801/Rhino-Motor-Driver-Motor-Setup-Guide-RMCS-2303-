import serial

def calc_lrc(data_bytes):
    lrc = 0
    for b in data_bytes:
        lrc = (lrc + b) & 0xFF
    lrc = ((-lrc) & 0xFF)
    return lrc

def make_frame(slave, func, reg, value):
    payload = bytes([slave, func, (reg >> 8) & 0xFF, reg & 0xFF,
                     (value >> 8) & 0xFF, value & 0xFF])
    lrc = calc_lrc(payload)
    return ":" + payload.hex().upper() + f"{lrc:02X}" + "\r\n"

PORT = '/dev/ttyUSB0'
BAUD = 9600
speed_counts = 9000
accel_counts = 17500

frames = [
    make_frame(0x09, 0x06, 0x0010, accel_counts),  # Accel
    make_frame(0x09, 0x06, 0x000E, speed_counts),  # Speed
    make_frame(0x09, 0x06, 0x0002, 0x0101),        # Enable CW
]

ser = serial.Serial(PORT, BAUD, bytesize=8, parity='N', stopbits=1, timeout=0.5)
for f in frames:
    ser.write(f.encode())
    print("Reply:", ser.read_until(b'\n'))

input("Press Enter to stop...")
stop_frame = make_frame(0x09, 0x06, 0x0002, 0x0100)
ser.write(stop_frame.encode())
ser.close()
