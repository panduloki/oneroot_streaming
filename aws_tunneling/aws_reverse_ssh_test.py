import subprocess
import os
import time
import paramiko  # SSH client library to manage SSH connections

# AWS EC2 instance details
EC2_IP = "myec2instance.yourdomain.com"  # Use your Route 53 domain name or Elastic IP here
EC2_USER = "ubuntu"  # The default user for an Ubuntu EC2 instance (or ec2-user for Amazon Linux)
PRIVATE_KEY_PATH = "<Path-to-your-private-key>.pem"  # Path to your EC2 private key file

# Local and remote port configurations for GStreamer
LOCAL_PORT = 8484  # Local port to forward from the local machine for GStreamer
REMOTE_PORT = 8484  # Port on the EC2 instance to forward to

def reverse_port_forward():
    """
    Establish reverse port forwarding from the local machine to the EC2 instance.
    This function sets up a reverse SSH tunnel, forwarding traffic from EC2's remote port to the local machine's port.
    """
    try:
        # Ensure the private key has the correct permissions
        os.chmod(PRIVATE_KEY_PATH, 0o400)  # Secure the private key file permissions

        # Set up the reverse SSH port forwarding using subprocess
        ssh_command = [
            "ssh",
            "-i", PRIVATE_KEY_PATH,  # Path to the private key file
            f"{EC2_USER}@{EC2_IP}",  # EC2 instance login (use domain name or EIP)
            "-R", f"{REMOTE_PORT}:localhost:{LOCAL_PORT}",  # Reverse port forwarding configuration
            "-N",  # Do not execute any commands, just forward the port
            "-f"  # Run in background
        ]

        # Run the SSH command to establish the reverse port forwarding
        print(f"Setting up reverse port forwarding from local port {LOCAL_PORT} to {REMOTE_PORT} on EC2...")
        subprocess.run(ssh_command, check=True)
        print(f"Reverse port forwarding set up. Access the local service on EC2 instance {EC2_IP}:{REMOTE_PORT}")

    except subprocess.CalledProcessError as e:
        print("Error occurred while setting up reverse port forwarding:", e)
        return False
    except PermissionError:
        print("Permission error: Ensure the private key file permissions are set correctly (chmod 400).")
        return False
    except Exception as e:
        print(f"Unexpected error during port forwarding setup: {e}")
        return False

    return True

def check_ssh_connection():
    """
    Check SSH connection to the EC2 instance to ensure the port is forwarded.
    This function establishes a simple SSH connection to verify connectivity.
    """
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically add the server's host key

        # Connect to the EC2 instance using SSH
        client.connect(EC2_IP, username=EC2_USER, key_filename=PRIVATE_KEY_PATH)
        print(f"Connected to {EC2_IP} successfully!")
        client.close()
        return True

    except paramiko.AuthenticationException:
        print("Authentication failed: Please check your SSH key and username.")
        return False
    except paramiko.SSHException as sshException:
        print(f"SSH connection failed: {sshException}")
        return False
    except Exception as e:
        print(f"Unexpected error while connecting to EC2 instance: {e}")
        return False

def main():
    """
    Main function to execute reverse port forwarding.
    Verifies the SSH connection and sets up port forwarding if the connection succeeds.
    """
    # Ensure SSH connection is working before setting up port forwarding
    if not check_ssh_connection():
        print("Unable to connect to EC2 instance. Exiting...")
        return

    # Set up the reverse port forwarding
    if reverse_port_forward():
        print(f"Service is now accessible on EC2 at {EC2_IP}:{REMOTE_PORT}")
    else:
        print("Failed to set up reverse port forwarding. Please check your configuration and try again.")

    # Keep the script running to maintain the port forwarding
    print("Press Ctrl+C to stop the reverse port forwarding.")
    try:
        while True:
            time.sleep(60)  # Keep the process alive, you can replace it with other logic if needed
    except KeyboardInterrupt:
        print("\nReverse port forwarding stopped by user.")

if __name__ == "__main__":
    main()
