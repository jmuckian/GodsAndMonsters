import pygame
import string
from pygame.locals import *
from gamedata import Display


class Menu:
    """Creates various menus for use throughout the game"""
    
    def __init__(self):
        self.display = Display()
        self.startrow = 0
        self.endrow = 0
        self.currentrow = 0
        self.startcol = 0
        self.endcol = 0
        self.currentcol = 0
        self.choices = []
        self.index = 0
    
    def singlelist(self, choices, row, col, screen):
        """Creates simple single column list populated by (choices) and
        positioned at (row) and (col).
        
        """
        self.screen = screen
        self.startrow = row
        self.endrow = len(choices) + self.startrow
        self.currentrow = self.startrow
        self.currentcol = col
        self.choices = choices
        self.index = self.currentrow - self.startrow
        
        for choice in self.choices:
            text = self.display.FONT.render(choice.upper(), True,
                                            self.display.BRIGHT_GREEN)
            self.screen.blit(text, (col * self.display.CH_SPACE,
                               self.currentrow * self.display.CH_SPACE))
            self.currentrow += 1
        self.currentrow = self.startrow
        self.select(0)
        pygame.display.update()
        while True:
            event = pygame.event.wait()
            if event.type == KEYDOWN:
                if event.key == K_DOWN:
                    self.select(1)
                elif event.key == K_UP:
                    self.select(-1)
                elif event.key == K_RETURN:
                    return self.choices[self.index]
            pygame.display.update()

    def skills(self, choices, row, col, screen):
        """Creates two column list populated by (choices) and
        positioned at (row) and (col).  Allows for point attribution.
        
        """
        self.screen = screen
        self.startrow = row
        self.endrow = []
        self.currenrow = self.startrow
        self.startcol = col
        self.endcol = 0

    def select(self, increment):
        """Checks to ensure movement is within bounds and if so
        highlights the newly selected item.
        
        """
        row = self.currentrow + increment
        if row < self.startrow or row >= self.endrow:
            pass
        else:
            self.index = self.currentrow - self.startrow
            self.deselect()
            self.currentrow += increment
            self.index += increment
            choice = self.choices[self.index]
            text = self.display.FONT.render(choice.upper(), True,
                                            self.display.WHITE)
            self.screen.blit(text, (self.currentcol * self.display.CH_SPACE,
                                    self.currentrow * self.display.CH_SPACE))
    
    def deselect(self):
        """Unhighlights the current item"""
        choice = self.choices[self.index]
        text = self.display.FONT.render(choice.upper(), True,
                                        self.display.BRIGHT_GREEN)
        self.screen.blit(text, (self.currentcol * self.display.CH_SPACE,
                                self.currentrow * self.display.CH_SPACE))
        
    def textinput(self, prompt, screen):
        self.screen = screen
        current_input = []
        while True:
            bg = pygame.image.load(self.display.BG_FULL).convert()
            screen.blit(bg, (0, 0))
            current_string = string.join(current_input, "")
            row = 24
            col = 0
            text = self.display.FONT.render(prompt.upper(), True,
                                            self.display.BRIGHT_MAGENTA)
            self.screen.blit(text, (col * self.display.CH_SPACE,
                                    row * self.display.CH_SPACE))
            col = len(prompt) + 1
            text = self.display.FONT.render(current_string.upper(), True,
                                            self.display.WHITE)
            self.screen.blit(text, (col * self.display.CH_SPACE,
                                    row * self.display.CH_SPACE))
            pygame.display.update()
            inkey = self.get_key()
            if inkey == K_BACKSPACE:
                current_input = current_input[0: -1]
            elif inkey == K_RETURN:
                break
            elif inkey <= 127:
                current_input.append(chr(inkey))
        return current_string
                
    def get_key(self):
        while True:
            event = pygame.event.poll()
            if event.type == KEYDOWN:
                return event.key
            else:
                pass
    