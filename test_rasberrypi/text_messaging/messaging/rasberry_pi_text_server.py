import socket
import threading
import os

"""
  1.Raspberry Pi (Server) Code:
    This script will run on the Raspberry Pi, acting as the server.
    It will wait for a connection from the Windows PC and
    exchange messages interactively.
"""
def read_text_aloud(message):
    # Use espeak to directly speak the message
    os.system(f'espeak "{message}"')
    
# Function to handle the communication with the client
def handle_client(client_socket):
    while True:
        try:
            # Receive and decode the message from the client
            message = client_socket.recv(1024).decode()

            if not message:
                print("Client disconnected.")
                break

            # Print the received message
            print(f"Client(*nano): {message}")
            read_text_aloud(message)

            # Send a reply to the client
            response = input("You(*rasberry_pi): ")
            client_socket.send(response.encode())
        except Exception as e:
            print(f"Error occurred: {e}")
            break

    # Close the client socket when done
    client_socket.close()


# Main function to start the server
def start_server(host="0.0.0.0", port=None):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        if port is None:
            print("server port should not be empty")
        else:
            server.bind((host, port))
            server.listen(1)

            print(f"Server listening on {host}:{port}")

            while True:
                # Accept incoming connections from clients
                client_socket, client_address = server.accept()
                print(f"Client connected from {client_address}")

                # Start a new thread to handle the client
                client_handler = threading.Thread(target=handle_client, args=(client_socket,))
                client_handler.start()

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        server.close()


# Run the server
if __name__ == "__main__":
    raspberry_pi_ip = "100.65.5.95"
    host_ip_default = "127.0.0.1"   # if you want to host on raspberry pi itself
    port1 = 5005
    start_server(host_ip_default, port1)  # Replace raspberry_ip with the IP of the Raspberry Pi
