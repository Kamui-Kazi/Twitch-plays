import pyautogui
from time import sleep


def pressandrelease(key: str, time: float = 0.5):
    if key.find(" ") > -1:
        pressesandreleasees(key.split(" "), time)
    else:
        pyautogui.keyDown(key)
        sleep(time)
        pyautogui.keyUp(key)


def pressesandreleasees(keys: list[str], time: float = 0.5):
    for key in keys:
        pyautogui.keyDown(key)
    sleep(time)
    for key in keys:
        pyautogui.keyUp(key)


def movemouse(dir: str, x: int = 100, y: int = 100):
    if dir.find("l") > -1:
        pyautogui.move(-1 * x, 0)
    if dir.find("r") > -1:
        pyautogui.move(x, 0)
    if dir.find("u") > -1:
        pyautogui.move(0, -1 * y)
    if dir.find("d") > -1:
        pyautogui.move(0, y)


def mouseclick(button: str):
    if button == "left":
        pyautogui.click(button="left")
    if button == "right":
        pyautogui.click(button="right")
