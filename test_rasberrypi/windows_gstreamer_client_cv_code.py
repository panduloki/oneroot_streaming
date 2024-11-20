import cv2
import socket
import numpy as np


def udp_stream_client(host: str, port: int):
    buffer_size = 65536  # UDP packets can carry up to 65536 bytes
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print(f"Listening for UDP packets on {host}:{port}")

    try:
        while True:
            packet, _ = sock.recvfrom(buffer_size)
            if packet:
                # Decode the image from the received packet
                frame = cv2.imdecode(np.frombuffer(packet, np.uint8), cv2.IMREAD_COLOR)
                if frame is not None:
                    cv2.imshow("Received Video Stream", frame)
                # Break loop on 'q' key press
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Closing the client...")
        sock.close()
        cv2.destroyAllWindows()


# Example usage
udp_stream_client("0.0.0.0", 5000)  # Listen on all interfaces on port 5000
