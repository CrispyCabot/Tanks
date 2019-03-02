import time
import pyautogui as pag
from random import randint
time.sleep(5)
pos = pag.position()
num = 20

for i in range(0,181, 10):
    pag.click()
    time.sleep(.5)
    pag.click()
    time.sleep(1)
    pag.typewrite('10')
    time.sleep(2)
    pag.press('enter')
    time.sleep(1)
    pag.hotkey('ctrlleft', 'shift', 's')
    time.sleep(1)
    pag.typewrite('tank'+str(num))
    num += 1
    time.sleep(1)
    pag.press('enter')
    time.sleep(1)
    pag.press('enter')
    time.sleep(1)
    pag.moveTo(1560, 559)
    pag.click()
    time.sleep(1)
    pag.moveTo(1622, 754)
    pag.click()
    time.sleep(1)
    pag.moveTo(1912, 864)
