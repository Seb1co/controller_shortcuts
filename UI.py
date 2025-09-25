from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QApplication, QHBoxLayout, QMainWindow
from shortcuts import Shortcuts
from example import TextPrint
import example
import sys
import pygame
import json
import io

class UI(QWidget):
    def __init__(self):
        super().__init__()
        self.shortcut = Shortcuts()
        self.name = self.shortcut.joystick_name
        self.command_list = self.shortcut.cl
        self.line_edits = []
        if self.name == "PS4 Controller":
            self.init_ps4()
        elif self.name == "XBOX Controller":
            self.init_xbox()


    def init_ps4(self):

        mainLayout = QVBoxLayout(self)


        topWidget = QWidget()
        topLayout = QHBoxLayout(topWidget)

        left_layout = QVBoxLayout()

        for button in self.shortcut.buttons:
            left_layout.addWidget(QLabel(button))


        middle_layout = QVBoxLayout()

        for i in range(16):
            self.line_edits.append(QLineEdit(self.command_list[i].strip("'\"")))
            self.line_edits[i].textChanged.connect(self.text_changed)
            middle_layout.addWidget(self.line_edits[i])

        topLayout.addLayout(left_layout)
        topLayout.addLayout(middle_layout)

        bottomWidget = QWidget()
        bottomLayout = QHBoxLayout(bottomWidget)

        save_button = QPushButton("Save")
        save_button.pressed.connect(self.save)

        help_button = QPushButton("Help")
        help_button.pressed.connect(self.help)

        bottomLayout.addWidget(save_button)
        bottomLayout.addWidget(help_button)

        mainLayout.addWidget(topWidget,stretch=11)
        mainLayout.addWidget(bottomWidget,stretch=5)

    def text_changed(self):
        for i in range(len(self.line_edits)):
            if self.line_edits[i].text() != self.command_list[i].strip("'\""):
                self.shortcut.commands[self.shortcut.joystick_name][self.shortcut.buttons[i]] = self.line_edits[i].text()
                print(self.shortcut.commands[self.shortcut.joystick_name][self.shortcut.buttons[i]])

    def save(self):
        if self.shortcut.verify_list():
            with open ("shortcuts.json","w") as fw:
                fw.write(json.dumps(self.shortcut.commands,indent=2))

    def help(self):
        self.help_window = Help()
        self.help_window.show()


    def init_xbox(self):
        ceva = 0

class Help(QWidget):
    def __init__(self):
        super().__init__()
        self.supported_keywords = [
            # Taste speciale
            ["alt", "alt_l", "alt_r", "alt_gr", "backspace", "caps_lock", "cmd", "cmd_l", "cmd_r"],
            ["ctrl", "ctrl_l", "ctrl_r", "delete", "down", "end", "enter", "esc"],
            ["f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10"],
            ["f11", "f12", "f13", "f14", "f15", "f16", "f17", "f18", "f19", "f20"],
            ["home", "left", "page_down", "page_up", "right", "shift", "shift_l", "shift_r"],
            ["space", "tab", "up"],
            ["media_play_pause", "media_volume_mute", "media_volume_down", "media_volume_up"],
            ["media_previous", "media_next"],
            ["insert", "menu", "num_lock", "pause", "print_screen", "scroll_lock"],
            # Litere a-z
            ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m"],
            ["n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"],
            # Cifre 0-9
            ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
            # Simboluri comune (de pe tastaturi standard QWERTY)
            ["`", "-", "=", "[", "]", "\\", ";", "'", ",", ".", "/"],
            # Alte taste posibile în anumite layouturi
            ["capslock", "numlock", "scrolllock", "escape"]
        ]
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(QLabel(f"Toate tastele care sunt acceptate:"))
        for i in range(len(self.supported_keywords)):
            sup_key = ""
            for j in range(len(self.supported_keywords[i])):
                sup_key += self.supported_keywords[i][j] + ", "
                if j == len(self.supported_keywords[i]) - 1:
                    main_layout.addWidget(QLabel(sup_key))

if __name__ == "__main__":
    pygame.init()
    app = QApplication(sys.argv)
    ui = UI()
    ui.show()
    sys.exit(app.exec())