import asyncio
import pyautogui
from time import sleep
import random
import vgamepad as vg
gamepad = vg.VX360Gamepad()

control_chance = 0

single_presses = {
    'left': 'a',
    'l':'a',
    'right':'d',
    'r':'d',
    'forward':'w',
    'up':'w',
    'w':'w',
    'walk':'walk',
    'back':'s',
    'down':'s',
    's':'s',
    'jump':'space',
    'left jump':'a space',
    'jump left':'a space',
    'lump':'a space',
    'right jump':'d space',
    'jump right':'d space',
    'rump':'d space',
    'forawrd jump':'w space',
    'jump forward':'w space',
    'fump':'w space',
    'back jump':'s space',
    'jump back':'s space',
    'bump':'s space',
    'tablet':'q',
    'q':'q',
    'empty':'f',
    'f':'f',
    'swap':'e',
    'e':'e',
    'voice':'t',
    't':'t',
    'close eyes': 'x c',
    'open eyes': 'x' 
}

hold_down = {
    'run':'shiftleft',
    'sprint':'shiftleft',
    'sneak':'ctrlleft',
    'crouch':'ctrlleft',
    'close left':'x',
    'close right':'c',
    'wink left':'x',
    'wink right':'c',
    
}

let_go = {
    'unrun':'shiftleft',
    'unsneak':'ctrlleft',
    'open left':'x',
    'open right':'c',
}

mouse_controls = {
    'mouse left':'l',
    'look left': 'l',
    'turn left': 'l',
    'ml':'l',
    'look right': 'r',
    'turn right': 'r',
    'mouse right':'r',
    'mr':'r',
    'look up': 'u',
    'turn up': 'u',
    'mouse up':'u',
    'mu':'u',
    'look down': 'd',
    'mouse down':'d',
    'turn down': 'd',
    'md':'d',
    
}

click_controls = {
    'left click':'left',
    'click left':'left',
    'lclick':'left',
    'lmb':'left',
    'right click':'right',
    'click right':'right',
    'rclick':'right',
    'rmb':'right' 
}

macros = {
    'throw':'throw',
    'swivel':'swivel',
    'spin':'spin',
    'ram':'ram',
    'jozu':'jozu',
    'boom bunny':'boom',
    'good noodle':'noddle',
    'gn folks':'noodle',
}

class KeyboardBot:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.task: asyncio.Task | None = None
        self.running = False

        self.single: dict = single_presses
        self.hold_down: dict = hold_down
        self.let_go:dict = let_go
        self.mouse_move: dict = mouse_controls
        self.mouse_click: dict = click_controls
        self.macros: dict = macros

    async def start(self):
        self.running = True
        self.task = asyncio.create_task(self._run())

    async def stop(self):
        self.running = False
        if self.task:
            self.task.cancel()

    async def submit(self, msg: str):
        await self.queue.put(msg)

    async def _run(self):
        while self.running:
            if random.random() > control_chance:
                msg:str = await self.queue.get()
                time = -1
                if msg.find('walk') > -1:
                    print("found walkies")
                    msg = msg.replace('walk', '').strip()
                    time = 2.5
                elif msg.find('light') > -1:
                    key = self.single.get(msg.replace('light', '').strip())
                    await asyncio.to_thread(pressandrelease, key, 0.01)
                elif msg.find('hard') > -1:
                    key = self.single.get(msg.replace('hard', '').strip())
                    await asyncio.to_thread(pressandrelease, key, 0.8)
                elif self.single.get(msg):
                    key = self.single.get(msg) 
                    if time > -1:
                        await asyncio.to_thread(pressandrelease, key, time)
                    else:
                        await asyncio.to_thread(pressandrelease, key)
                elif self.hold_down.get(msg):
                    key = self.hold_down.get(msg)
                    await asyncio.to_thread(holdkey, key) 
                elif self.let_go.get(msg):
                    key = self.let_go.get(msg)
                    await asyncio.to_thread(releasekey, key)
                elif self.mouse_move.get(msg):
                    key = self.mouse_move.get(msg)
                    if time > -1:
                        await asyncio.to_thread(movemouse, key, time)
                    else:
                        await asyncio.to_thread(movemouse, key)
                elif self.mouse_click.get(msg):
                    key = self.mouse_click.get(msg)
                    await asyncio.to_thread(clickmouse, key)
                elif self.macros.get(msg):
                    key = self.macros.get(msg)
                    await asyncio.to_thread(execute_macros, key)


def look(key):
    match key:
        case 'l':
            gamepad.right_joystick_float(x_value_float=-1, y_value_float=0)
        case 'r':
            gamepad.right_joystick_float(x_value_float=1, y_value_float=0)
        case 'u':
            gamepad.right_joystick_float(x_value_float=0, y_value_float=1)
        case 'd':
            gamepad.right_joystick_float(x_value_float=0, y_value_float=-1)
    gamepad.update()
    
def pressandrelease(key: str, time: float = 0.1):
    
    
    if key.find(" ") > -1:
        pressesandreleasees(key.split(" "), time)
    else:
        pyautogui.keyDown(key)
        sleep(time)
        pyautogui.keyUp(key)

def pressesandreleasees(keys: list[str], time: float = 0.1):
    for key in keys:
        print("pressing: " + key)
        pyautogui.keyDown(key)
    sleep(time)
    for key in keys:
        pyautogui.keyUp(key)


def holdkey(key: str):
    pyautogui.keyDown(key)
    

def releasekey(key: str):
    pyautogui.keyUp(key)
  

def movemouse(dir: str, time: float = 0.05):
    gamepad.reset()
    gamepad.update()
    look(dir)
    sleep(time)
    gamepad.reset()
    gamepad.update()

def clickmouse(button: str):
    pyautogui.mouseDown(button=button)
    pyautogui.sleep(0.05)
    pyautogui.mouseUp(button=button)

def execute_macros(key: str):
    match key:
        case 'throw':
            throw()
        case 'swivel':
            swivel()
        case 'spin':
            swivel()
        case 'ram':
            ram()
        case 'jozu':
            jozu()
        case 'boom':
            boom()
        case 'noddle':
            noodle()

def throw():
    pyautogui.mouseDown(button='right')
    pyautogui.sleep(0.1)
    pyautogui.mouseDown(button='left')
    pyautogui.sleep(0.1)
    pyautogui.mouseUp(button='left')
    pyautogui.mouseUp(button='right')

def swivel():
    gamepad.reset()
    gamepad.update()
    look('l')
    sleep(5)
    gamepad.reset()
    gamepad.update()
    
def ram():
    pressandrelease('w', 5)
        

def jozu():
    pressandrelease('s', 5)

def boom():
    for i in range(random.randint(2,10)):
        pyautogui.mouseDown(button='left')
        pyautogui.sleep(0.05)
        pyautogui.mouseUp(button='left')
        pyautogui.sleep(0.05)

def noodle():
    for x in range(random.randint(2,10)):
        gamepad.reset()
        gamepad.update()
        look('u')
        sleep(0.5)
        gamepad.reset()
        gamepad.update()
        look('d')
        sleep(0.5)
    gamepad.reset()
    gamepad.update()