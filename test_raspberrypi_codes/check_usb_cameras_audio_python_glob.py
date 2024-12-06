import glob
import subprocess


def check_usb_camera_using_python_glob():
    try:
        # Attempt to look for /dev/video* devices
        video_devices = glob.glob('/dev/video*')
    except Exception as e:
        # Handle any unexpected errors
        print(f"Error while checking USB cameras using command glob: {e}")
    else:
        # Execute if no exception occurs
        if video_devices:
            print("USB Camera(s) detected:")
            for device in video_devices:
                print(f" - {device}")
        else:
            print("No USB Camera detected.")


def list_video_devices_by_command_v4l2():
    try:
        # Run the v4l2-ctl command
        result = subprocess.run(['v4l2-ctl', '--list-devices'], text=True, capture_output=True, check=True)

        # Parse the command output
        output = result.stdout

        # Print the raw output
        print("Raw command output:")
        print(output)

        if output:
            devices = {}
            current_device = None
            for line in output.splitlines():
                if line.endswith(':'):  # Device name line
                    current_device = line[:-1]
                    devices[current_device] = []
                elif current_device and line.startswith('\t'):  # Associated video device
                    devices[current_device].append(line.strip())

            # Print the parsed devices
            if devices:
                print("\nParsed Video Devices:")
            for device_name, video_files in devices.items():
                print(f"{device_name}:")
                for video_file in video_files:
                    print(f"  - {video_file}")
            else:
                print("No video devices detected.")
            return devices
        else:
            print("v4l2 command output was null check again in terminal")
    except FileNotFoundError:
        print("v4l2-ctl is not installed. Please install it using 'sudo apt install v4l-utils'.")
    except subprocess.CalledProcessError as e:
        print(f"Error running v4l2-ctl: {e}")
    return None


def check_audio_devices_checking_proc_files():
    """
      The check_audio_devices function works by reading the /proc/asound/cards file,
      which contains information about sound cards recognized by the system.
      This approach works on Linux-based systems, including Raspberry Pi,
      as they follow a similar file system structure.
      The /proc/asound/cards file is not specifically tied to either input (microphones)
      or output (speakers/headphones). Instead, it provides a list of all sound cards
      recognized by the system, regardless of whether they are used for input or output.
      For example,
        0 [ALSA ]: bcm2835 - bcm2835 ALSA
                     bcm2835 ALSA - IEC958/HDMI
    """
    try:
        # Check audio devices using /proc/asound/cards
        with open('/proc/asound/cards', 'r') as f:
            audio_cards = f.read()
        if audio_cards.strip():
            print("Audio devices detected:")
            print(audio_cards)
        else:
            print("No audio devices detected.")
    except FileNotFoundError:
        print("Audio device information not available.")


def check_audio_with_pyaudio():
    """Installation (if needed only for raspberry pi):
	PyAudio: Install it via:
		sudo apt update
		sudo apt install python3-pyaudio
	Install via pip directly:
        python3 -m pip install pyaudio
	If additional setup is required, you can use:
		sudo apt-get install portaudio19-dev python3-pyaudio"""
    try:
        import pyaudio
        p = pyaudio.PyAudio()
        device_count = p.get_device_count()
        if device_count > 0:
            print("Audio devices detected via PyAudio:")
            for i in range(device_count):
                device_info = p.get_device_info_by_index(i)
                device_name = device_info['name']
                is_input = device_info['maxInputChannels'] > 0
                is_output = device_info['maxOutputChannels'] > 0
                print(f" - {device_name}:")
                print(f"   Input: {'Yes' if is_input else 'No'}")
                print(f"   Output: {'Yes' if is_output else 'No'}")
        else:
            print("No audio devices detected via PyAudio.")
        p.terminate()
    except ImportError:
        print("PyAudio is not installed.  Skipping PyAudio check.")
        print("sudo command: sudo apt install python3-pyaudio")
        print("python command: python3 -m pip install pyaudio")
    except Exception as e:
        print(f"Error checking audio devices with PyAudio: {e}")


def check_audio_with_a_record_and_aplay():
    try:
        # Check input (capture) devices
        arecord_output = subprocess.check_output(['arecord', '-l'], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        print("Error while checking input devices:")
        print(e.output)
    except FileNotFoundError:
        print("The 'arecord' command is not installed. Please install it using 'sudo apt install alsa-utils'.")
    else:
        print("Audio Capture (Input) Devices:")
        print(arecord_output.strip())

    print("\n-----------------------------------\n")

    try:
        # Check output (playback) devices
        aplay_output = subprocess.check_output(['aplay', '-l'], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        print("Error while checking output devices:")
        print(e.output)
    except FileNotFoundError:
        print("The 'aplay' command is not installed. Please install it using 'sudo apt install alsa-utils'.")
    else:
        print("Audio Playback (Output) Devices:")
        print(aplay_output.strip())

# Main execution
if __name__ == "__main__":
    print("Checking USB Camera using Python glob:")
    check_usb_camera_using_python_glob()
    print("\nChecking Video Devices using v4l2 command:")
    list_video_devices_by_command_v4l2()
    print("\nChecking Audio Devices from /proc filesystem:")
    check_audio_devices_checking_proc_files()
    print("\nChecking Audio Devices via PyAudio:")
    check_audio_with_pyaudio()
    print("\nChecking Audio Devices using arecord and aplay commands:")
    check_audio_with_a_record_and_aplay()
