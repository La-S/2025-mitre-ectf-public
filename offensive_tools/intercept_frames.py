from scapy.all import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("hmm")
s.connect(("3.81.51.207", 2002))
print("HERE")
while True:
    # Get and decode frame
    print("HERE!")
    line = b""
    while not line.endswith(b"\n"):
        if (cur_byte := s.recv(1)) == b"":  # connection closed
            raise RuntimeError("Failed to receive from satellite")
        line += cur_byte
    frame = json.loads(line)
    channel = frame["channel"]
    timestamp = frame["timestamp"]
    print("encoded")
    encoded = binascii.a2b_hex(frame.pop("encoded"))
    print(encoded)
    # logger.debug(f"Received encoded ({channel}, {timestamp}): {encoded}")
