import os
import sys
import signal
import subprocess
import multiprocessing
import pyclip
from time import sleep
from os.path import dirname as up

path = up(up(os.path.abspath(__file__)))
sys.path.append(path)

from src.keymouse import KeyMouse
from pylayout import Layout

keymouse = KeyMouse()
layout = Layout()


def start(editor: list, q):
    p = subprocess.Popen(editor)
    q.put(p.pid)


def test(editor=["gedit"]):
    q = multiprocessing.Queue()
    p = multiprocessing.Process(
        target=start,
        args=(
            editor,
            q,
        ),
    )
    p.start()
    pid = q.get()
    sleep(5)
    keymouse.click(1000, 500)
    print(keymouse.layout.get())
    # keymouse.layout.set("us")
    sleep(1)
    print(keymouse.layout.get())
    pyclip.copy("Hello world")
    keymouse.hotkey("ctrl", "v")
    sleep(0.5)
    pyclip.copy("Nonsense")
    keymouse.hotkey("ctrl", "a")
    sleep(0.5)
    text = pyclip.paste().decode()
    assert text == "Nonsense", text
    keymouse.hotkey("ctrl", "x")
    sleep(0.5)
    os.kill(pid, signal.SIGTERM)
    p.kill()
    text = pyclip.paste().decode()

    assert text == "Hello world", text
    print("Finish")
    exit()


if __name__ == "__main__":
    if os.name == "nt":
        test(["notepad.exe", "file.txt"])
    elif os.name == "posix":
        test()
