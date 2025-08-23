import socket
import struct
import time

HOST = "127.0.0.1"
PORT = 5765
MSP_SET_RAW_RC = 200
RATE_HZ = 10

def build_msp_v1(cmd: int, payload_bytes: bytes) -> bytes:
    pre = b"$M<"
    size = len(payload_bytes)
    hdr = bytes([size, cmd & 0xFF])
    cs = 0
    cs^=size
    cs^= (cmd & 0xFF)
    for b in payload_bytes:
        cs^= b
    return pre + hdr + payload_bytes + bytes([cs & 0xFF])

def open_conn():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)
    s.connect((HOST, PORT))
    s.settimeout(None)
    return s

def send_frame(sock, channels):
    frame = build_msp_v1(MSP_SET_RAW_RC, struct.pack("<8H", *channels))
    sock.sendall(frame)
    return frame

def main():
    
    sock = open_conn()

    roll = 1500
    pitch = 1500
    yaw = 2000 
    
    # сначала несколько prearm 
    ch = [roll, pitch, 1000, 1500, 1500, 1500, 1500, 1500]
    for _ in range(20):
        send_frame(sock, ch); time.sleep(1.0/RATE_HZ)
    # затем держим stickarm состояние (throttle=1000, yaw=2000)
    ch = [roll, pitch, 1000, yaw, 1500, 1500, 1500, 1500]
    t0 = time.time()
    
    while time.time() - t0 < 30.0:
        f = send_frame(sock, ch)
        time.sleep(1.0)

    # теперь плавно повышаем газ, но держим yaw=2000
    for th in range(1100, 1601, 50):
        ch = [roll, pitch, th, yaw, 1500, 1500, 1500, 1500]
        f = send_frame(sock, ch)
        time.sleep(0.5)
    ch = [roll, pitch, 1400, yaw, 1500, 1500, 1500, 1500]
    for _ in range(20):
        send_frame(sock, ch); time.sleep(0.5)

    # опускаем газ и yaw (disarm)
    ch = [roll, pitch, 1000, 1500, 1500, 1500, 1500, 1500]
    for _ in range(20):
        send_frame(sock, ch); time.sleep(0.1)

    time.sleep(15.0)


if __name__ == "__main__":
    main()