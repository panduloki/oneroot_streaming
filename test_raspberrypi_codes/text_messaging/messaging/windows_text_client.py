import socket

"""
  2.Windows PC (Client) Code:
    This script will run on the Windows PC,
    acting as the client that connects to the Raspberry Pi and
    sends/receives messages interactively.
"""

def start_client(server_ip = None, server_port = None):
    try:
        if server_ip is None:
            print("server ip should not be empty")
        elif server_port is None:
            print("server port should not be empty")
        else:
            # Create a socket object to connect to the server
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect to the Raspberry Pi server
            client.connect((server_ip, server_port))
            print(f"Connected to server at {server_ip}:{server_port}")

            while True:
                try:
                    # Get input message from the user (client side)
                    message = input("You(*windows): ")
                    client.send(message.encode())  # Send message to the server

                    # Receive server's response and print it
                    response = client.recv(1024).decode()
                    print(f"Server: {response}")

                except Exception as e:
                    print(f"Error occurred: {e}")
                    break

    except Exception as e:
        print(f"Error occurred while connecting: {e}")
    finally:
        client.close()


# Replace "raspberry_ip" with the Raspberry Pi's IP address
if __name__ == "__main__":
    raspberry_pi_ip = "100.126.63.67"
    port1 = 5005
    start_client(raspberry_pi_ip, port1)  # Replace raspberry_ip with the IP of the Raspberry Pi
