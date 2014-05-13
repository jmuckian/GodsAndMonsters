#!/usr/bin/python
"""Gods & Monsters"""

import os
import pygame
from pygame.locals import *
from sys import exit
from gamedata import *
import char


class Intro:
    
    
    def __init__(self):
        pygame.init()
        self.display = Display()
        self.screen = pygame.display.set_mode((640, 400), 0, 32)
        pygame.display.set_caption("Gods & Monsters")
    
    def start(self):
        bg = pygame.image.load(self.display.BG_TITLE).convert()
        self.screen.blit(bg, (0, 0))
        prompt = ["GODS & MONSTERS", "(C) 2007 G&M DEV TEAM",
                  "BASED ON PEN & PAPER GAME", "CREATED BY JERRY STRATTON",
                  "HTTP://WWW.GODSMONSTERS.COM"]
        row = 16
        col = 2
        for line in prompt:
            text = self.display.FONT.render(line, True, self.display.BRIGHT_GREEN)
            self.screen.blit(text, (col * self.display.CH_SPACE,
                                    row * self.display.CH_SPACE))
            row += 1
        pygame.display.update()
        while True:
            event = pygame.event.wait()
            if event.type == KEYDOWN:
                self.menu()

    def menu(self):
        bg = pygame.image.load(self.display.BG_FULL).convert()
        self.screen.blit(bg, (0, 0))
        prompt = ["CREATE NEW CHARACTER", "NEW GAME", "QUIT GAME"]
        row = 16
        col = 2            
        for line in prompt:
            ch = self.display.FONT.render(line[0], True, self.display.WHITE)
            text = self.display.FONT.render(line[1:], True, self.display.BRIGHT_GREEN)
            self.screen.blit(ch, (col * self.display.CH_SPACE,
                                  row * self.display.CH_SPACE))
            self.screen.blit(text, ((col + 1) * self.display.CH_SPACE,
                                    row * self.display.CH_SPACE))
            row += 1            
        pygame.display.update() 
        while True:
            event = pygame.event.wait()
            if event.type == KEYDOWN:
                if event.key == K_q:
                    exit()
                if event.key == K_c:
                    self.newcharacter()
                if event.key == K_n:
                    pass

    def newcharacter(self):
        character = char.CreateCharacter()
        character.createcharacter(self.screen)
        
        
if __name__ == "__main__":
    startup = Intro()
    startup.start()
