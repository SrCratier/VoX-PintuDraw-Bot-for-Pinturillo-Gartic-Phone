import ctypes
import time
import math
import os
import json
import cv2
import numpy as np
import keyboard
from PIL import Image, ImageGrab
from ctypes import wintypes

INPUT_MOUSE = 0
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_ABSOLUTE = 0x8000

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", wintypes.LONG),
                ("dy", wintypes.LONG),
                ("mouseData", wintypes.DWORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", ctypes.c_ulonglong)]

class INPUT(ctypes.Structure):
    _fields_ = [("type", wintypes.DWORD),("mi", MOUSEINPUT)]

SendInput = ctypes.windll.user32.SendInput
GetSystemMetrics = ctypes.windll.user32.GetSystemMetrics
SCREEN_WIDTH = GetSystemMetrics(0)
SCREEN_HEIGHT = GetSystemMetrics(1)

def win32_move(x, y):
    norm_x = int(x * 65535 / SCREEN_WIDTH)
    norm_y = int(y * 65535 / SCREEN_HEIGHT)
    mi = MOUSEINPUT(norm_x, norm_y, 0, MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE, 0, 0)
    inp = INPUT(INPUT_MOUSE, mi)
    SendInput(1, ctypes.pointer(inp), ctypes.sizeof(inp))

def win32_click_down():
    mi = MOUSEINPUT(0, 0, 0, MOUSEEVENTF_LEFTDOWN, 0, 0)
    inp = INPUT(INPUT_MOUSE, mi)
    SendInput(1, ctypes.pointer(inp), ctypes.sizeof(inp))

def win32_click_up():
    mi = MOUSEINPUT(0, 0, 0, MOUSEEVENTF_LEFTUP, 0, 0)
    inp = INPUT(INPUT_MOUSE, mi)
    SendInput(1, ctypes.pointer(inp), ctypes.sizeof(inp))

def get_mouse_pos_win32():
    pt = wintypes.POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return [pt.x, pt.y]

class HiFiBot:
    def __init__(self):
        self.config_file = "config.json"
        self.config = {
            'tl': None, 
            'br': None,
            'keys': {
                'start': None,
                'stop': None,
                'pause': None,
                'calibrate': None
            }
        }
        self.INTERPOLATION_STEP = 2  
        self.INPUT_DELAY = 0.002     

    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f: 
                    loaded = json.load(f)
                    self.config.update(loaded)
                    if 'keys' not in loaded or not all(k in loaded['keys'] for k in ['start', 'stop', 'pause', 'calibrate']):
                        return False
                return True
            except: return False
        return False

    def save_config(self):
        with open(self.config_file, 'w') as f: json.dump(self.config, f)

    def configure_keys(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("╔════════════════════════════════════════════════════════╗")
        print("║           ⚙  KEYBOARD CONFIGURATION                    ║")
        print("╠════════════════════════════════════════════════════════╣")
        print("║  Please press the key you want to use for each action  ║")
        print("╚════════════════════════════════════════════════════════╝")
        
        actions = [
            ('start', 'START Drawing'),
            ('stop', 'STOP / EMERGENCY'),
            ('pause', 'PAUSE / RESUME'),
            ('calibrate', 'CALIBRATE Screen')
        ]

        new_keys = {}
        for action_code, action_name in actions:
            print(f"\n>> Press key for: [ {action_name} ] ...")
            key = keyboard.read_key()
            time.sleep(0.3) 
            print(f"   Selected: {key.upper()}")
            new_keys[action_code] = key
        
        self.config['keys'] = new_keys
        self.save_config()
        print("\n[OK] Configuration Saved!")
        time.sleep(1)

    def calibrate(self):
        key_calib = self.config['keys']['calibrate']
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n--- SCREEN CALIBRATION ---")
        print(f"1. Move mouse to TOP-LEFT corner -> Press [{key_calib.upper()}]")
        keyboard.wait(key_calib)
        time.sleep(0.2)
        self.config['tl'] = get_mouse_pos_win32()
        print(f"   Saved: {self.config['tl']}")

        print(f"\n2. Move mouse to BOTTOM-RIGHT corner -> Press [{key_calib.upper()}]")
        keyboard.wait(key_calib)
        time.sleep(0.2)
        self.config['br'] = get_mouse_pos_win32()
        print(f"   Saved: {self.config['br']}")
        self.save_config()
        print("\nConfiguration saved.")
        time.sleep(1)

    def get_canvas_coords(self, rx, ry, logic_w, logic_h):
        tl, br = self.config['tl'], self.config['br']
        screen_w = br[0] - tl[0]
        screen_h = br[1] - tl[1]
        sx = int(tl[0] + (rx * (screen_w / logic_w)))
        sy = int(tl[1] + (ry * (screen_h / logic_h)))
        return sx, sy

    def interpolate_line(self, x1, y1, x2, y2):
        dist = math.hypot(x2 - x1, y2 - y1)
        if dist == 0: return []
        steps = int(dist / self.INTERPOLATION_STEP)
        if steps < 1: steps = 1
        return zip(np.linspace(x1, x2, steps), np.linspace(y1, y2, steps))

    def process_image(self):
        img_grab = ImageGrab.grabclipboard()
        if not img_grab: return None, 0, 0
        if isinstance(img_grab, list): img_grab = Image.open(img_grab[0])
        
        img = np.array(img_grab.convert('RGB'))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        
        target_w = 600 
        h, w = img.shape[:2]
        ratio = target_w / w
        target_h = int(h * ratio)
        img = cv2.resize(img, (target_w, target_h), interpolation=cv2.INTER_CUBIC)
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0) 
        edges = cv2.Canny(blurred, 50, 150)
        
        contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
        optimized_paths = []
        for cnt in contours:
            if cv2.arcLength(cnt, False) < 20: continue 
            epsilon = 0.001 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, False)
            optimized_paths.append(approx.reshape(-1, 2).tolist())
            
        return optimized_paths, target_w, target_h

    def draw(self, paths, w, h):
        k_stop = self.config['keys']['stop']
        k_pause = self.config['keys']['pause']
        
        print(f"\n>> Drawing {len(paths)} paths...")
        
        if len(paths) > 0:
            paths.sort(key=lambda x: len(x), reverse=True)

        for path in paths:
            if keyboard.is_pressed(k_stop): return

            # Pause Logic
            if keyboard.is_pressed(k_pause):
                print(f"\n[||] PAUSED. Press [{k_pause.upper()}] to resume...")
                time.sleep(0.5)
                keyboard.wait(k_pause)
                print(">> Resuming...")
                time.sleep(0.5)

            start = path[0]
            sx, sy = self.get_canvas_coords(start[0], start[1], w, h)
            
            win32_click_up()
            win32_move(sx, sy)
            time.sleep(0.02)
            
            win32_click_down()
            time.sleep(0.02)
            
            last_x, last_y = sx, sy
            
            for i in range(1, len(path)):
                if keyboard.is_pressed(k_stop): 
                    win32_click_up()
                    return
                
                p_next = path[i]
                tx, ty = self.get_canvas_coords(p_next[0], p_next[1], w, h)
                
                for ix, iy in self.interpolate_line(last_x, last_y, tx, ty):
                    win32_move(int(ix), int(iy))
                    time.sleep(self.INPUT_DELAY) 
                
                last_x, last_y = tx, ty

            win32_move(last_x, last_y)
            time.sleep(0.02)
            win32_click_up()
            time.sleep(0.02)

    def run(self):
        if not self.load_config():
            self.configure_keys()

        os.system('cls' if os.name == 'nt' else 'clear')
        
        k = self.config['keys']
        k_start = k['start'].upper()
        k_stop = k['stop'].upper()
        k_pause = k['pause'].upper()
        k_calib = k['calibrate'].upper()

        print("╔════════════════════════════════════════════════════════╗")
        print("║          🎨 PINTURILLO HI-FI BOT v1.0                  ║")
        print("║           Developed by SrCratier                       ║")
        print("╠════════════════════════════════════════════════════════╣")
        print(f"║   [{k_start:<6}]   ▶ START DRAWING (Clipboard)               ║")
        print(f"║   [{k_stop:<6}]   ■ STOP / EMERGENCY                        ║")
        print(f"║   [{k_pause:<6}]   II PAUSE / RESUME                         ║")
        print(f"║   [{k_calib:<6}]   ⚙ CALIBRATE SCREEN                        ║")
        print("╠════════════════════════════════════════════════════════╣")
        print("║   💰 SUPPORT THIS PROJECT                              ║")
        print("║   Binance ID: 851390091                                ║")
        print("╚════════════════════════════════════════════════════════╝")
        
        if not self.config['tl']: 
            print(f"\n[!] WARNING: Calibration needed. Press {k_calib} to configure.")

        while True:
            if keyboard.is_pressed(k['calibrate']):
                self.calibrate()
                self.run()
            
            if keyboard.is_pressed(k['start']):
                paths, w, h = self.process_image()
                if paths:
                    self.draw(paths, w, h)
                    print("\n>> Done.")
                else:
                    print("\n[!] Error: Clipboard empty or invalid image.")
                    time.sleep(1)
            
            if keyboard.is_pressed(k['stop']):
                win32_click_up()
            
            time.sleep(0.01)

if __name__ == "__main__":
    try: 
        HiFiBot().run()
    except KeyboardInterrupt: 
        pass