import pygame
import pynput.keyboard
import threading
from pynput.keyboard import Controller as keyboard_controller
from pynput.mouse import Controller as mouse_controller
from PyQt6.QtCore import QTimer
import json


class Shortcuts:

    def __init__(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)

        self.joystick = pygame.joystick.Joystick(0)
        self.joystick_name = self.joystick.get_name()
        print(f"Ma numesc {self.joystick_name}")

        self.key_controller = keyboard_controller()
        self.mouse_controller = mouse_controller()
        self.cl = []


        self.buttons = [
            "X","O","SQ","TR","SHAR","PSB","OPT","L_ST","R_ST",
            "L1","R1","D-UP","D-DN","D-LF","D-RG","TCH_P"
        ]
        self.load_json()

        self.timer.start(1)

    def verify_list(self) -> bool:
        for buttons in self.buttons:
            if self.commands[self.joystick_name][buttons] != "undefined":
                comanda = self.commands[self.joystick_name][buttons].split("+")
                if len(comanda) == 1:
                    try:
                        key = getattr(pynput.keyboard.Key,comanda[0]) if len(comanda[0]) != 1 else None
                        print(self.commands[self.joystick_name][buttons])
                    except AttributeError:
                        print("The key you entered is wrong \n"
                              "Check the help button to see the correct name of the key you want to enter")
                        return False
                elif len(comanda) == 2:
                    try:
                        key = getattr(pynput.keyboard.Key, comanda[0]) if len(comanda[0]) != 1 else None
                        key1 = getattr(pynput.keyboard.Key, comanda[1]) if len(comanda[1]) != 1 else None
                        print(self.commands[self.joystick_name][buttons])
                    except AttributeError:
                        print("One of the arguments separated by the + sign is not correct \n"
                              "Check the Help button to see the correct name of the key you want to enter")
                        return False

        return True

    def load_json(self):
        print(self.buttons[5])
        with open('shortcuts.json') as fr:
            self.commands = json.load(fr)
        for i in range(16):
            self.cl.append(json.dumps(self.commands[self.joystick_name][self.buttons[i]]))

        print(self.cl[4])
        print(json.dumps(self.commands["PS4 Controller"][self.buttons[5]]))       # example for taking out the command out of the file
        self.commands["PS4 Controller"][self.buttons[5]] = "alt_l+tab"                      # example for overwriting commands or asigning them one
        print(json.dumps(self.commands["PS4 Controller"],indent= 2))

    def key_press(self,key1,key2):
        self.key_controller.press(key1)
        print(f"Am apasat tasta {key1}")

        if key2 != None:
            self.key_controller.press(key2)
            print(f"Am apasat tasta {key2}")

            self.key_controller.release(key2)
            print(f"Am lasat tasta {key2}")

        self.key_controller.release(key1)
        print(f"Am lasat tasta {key1}")

    def mouse_move(self,dx,dy):
        self.mouse_controller.move(dx * 10,dy * 10)
        print(f"Am mutat mouse-ul cu {dx} pe axa OX si cu {dy} pe axa OY")

    def mouse_click(self):
        self.mouse_controller.press(pynput.mouse.Button.left)
        self.mouse_controller.release(pynput.mouse.Button.left)
        print(f"Am apasat mouse ul")

    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                if self.commands[self.joystick_name][self.buttons[event.button]].split("+")[0] != "undefined":
                    try :
                        arg2 = getattr(pynput.keyboard.Key, self.commands[self.joystick_name][self.buttons[event.button]].split("+")[1])
                    except IndexError:
                        arg2 = None
                    print(arg2)
                    t = threading.Thread(target=self.key_press, args=(getattr(pynput.keyboard.Key,self.commands[self.joystick_name][self.buttons[event.button]].split("+")[0]),
                                                                      arg2))
                    t.start()
                    t.join()
            if event.type == pygame.JOYAXISMOTION:          #Left Stick - mouse movement
                        t = threading.Thread(target=self.mouse_move,args=(self.joystick.get_axis(0),
                                                                          self.joystick.get_axis(1)))
                        t.start()
                        t.join()