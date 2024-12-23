import os
import shutil

def check_espeak_installed():
    # Check if espeak is installed
    if shutil.which("espeak") is None:
        print("Error: espeak is not installed. Please install it and try again.")
        return True
    else:
        print("espeak is not installed. install using: sudo apt-get install espeak")
        return False

def read_text_using_gtts(message):  
    """
    Use Google Text-to-Speech (gtts) to read the given message aloud.
    Check if gtts is installed before attempting to use it.
    """
    # Check if gtts is installed
    if shutil.which("gtts-cli") is None:
        print("Error: gtts-cli is not installed. Please install it and try again. sudo apt-get install gtts-cli")
        return

    # Speak the message using gtts
    os.system(f'gtts-cli "{message}" --output /tmp/speech.mp3')
    os.system('mpg123 /tmp/speech.mp3')


def read_text_using_espeak(message):
    """
    Use espeak to read the given message aloud.
    Check if espeak is installed before attempting to use it.
    """
    if check_espeak_installed():
        return
    # Speak the message using espeak
    os.system(f'espeak "{message}"')


def play_audio_file_using_pydub(file_path):
    """
    Play an audio file (MP3 or WAV) using pydub and simpleaudio.
    """
    def check_pydub_installed():
        try:
            import pydub
            import pydub.playback
            from pydub import AudioSegment
            from pydub.playback import play
            return True
        except ImportError:
                print("Error: pydub is not installed. Please install it using: pip3 install pydub --break-system-packages")
                #return False


    if not check_pydub_installed():
        return

    try:
        audio = AudioSegment.from_file(file_path)
        play(audio)
    except Exception as e:
        print(f"Error playing audio file: {e}")

def play_audio_file_using_simpleaudio(file_path):
    """
    Play an audio file (WAV) using simpleaudio.
    """
    def check_simpleaudio_installed():
        try:
            import simpleaudio as sa
            return True
        except ImportError:
            print("Error: simpleaudio is not installed. Please install it using: pip install simpleaudio")
            return False

    if not check_simpleaudio_installed():
        return

    try:
        #TODO check file path exists
        wave_obj = sa.WaveObject.from_wave_file(file_path)
        play_obj = wave_obj.play()
        play_obj.wait_done()
    except Exception as e:
        print(f"Error playing audio file with simpleaudio: {e}")

