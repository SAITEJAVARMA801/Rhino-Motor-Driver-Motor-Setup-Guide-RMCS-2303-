import serial
import time

def calc_lrc(data_bytes):
    lrc = 0
    for b in data_bytes:
        lrc = (lrc + b) & 0xFF
    lrc = ((-lrc) & 0xFF)
    return lrc

def make_frame(slave, func, reg, value):
    payload = bytes([slave, func, (reg >> 8) & 0xFF, reg & 0xFF, (value >> 8) & 0xFF, value & 0xFF])
    lrc = calc_lrc(payload)
    return ":" + payload.hex().upper() + f"{lrc:02X}" + "\r\n"

PORT = '/dev/ttyUSB0'
BAUD = 9600

# Values from Rhino config
speed_counts = 9000
accel_counts = 17500

# Motor IDs for full robot
motor_ids = [3, 4, 7, 5]  # RF, RB, LF, LB

ser = serial.Serial(PORT, BAUD, bytesize=8, parity='N', stopbits=1, timeout=0.5)

print("=== Starting ALL motors ===")
for motor_id in motor_ids:
    print(f"--- Motor ID {motor_id} ---")
    frames = [
        make_frame(motor_id, 0x06, 0x0010, accel_counts),  # Accel
        make_frame(motor_id, 0x06, 0x000E, speed_counts),  # Speed
        make_frame(motor_id, 0x06, 0x0002, 0x0101),        # Enable CW
    ]
    for frame in frames:
        print(f"Sending: {frame.strip()}")
        ser.write(frame.encode())
        reply = ser.read_until(b'\n')
        print("Reply:", reply)
        time.sleep(0.1)

print("All motors running CW...")
input("Press Enter to stop all motors...")

print("=== Stopping ALL motors ===")
for motor_id in motor_ids:
    stop_frame = make_frame(motor_id, 0x06, 0x0002, 0x0100)
    print(f"Stopping motor {motor_id}: {stop_frame.strip()}")
    ser.write(stop_frame.encode())
    reply = ser.read_until(b'\n')
    print("Reply:", reply)
    time.sleep(0.1)

ser.close()
