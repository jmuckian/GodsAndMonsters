"""Module for displaying various elements"""

import curses

class Color:
    
    
    def __init__(self):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)
        self.RED = curses.color_pair(1)
        self.GREEN = curses.color_pair(2)
        self.YELLOW = curses.color_pair(3)
        self.BLUE = curses.color_pair(4)
        self.MAGENTA = curses.color_pair(5)
        self.CYAN = curses.color_pair(6)
        self.WHITE = curses.color_pair(7)
        
class Menu:
    
    
    def __init__(self):
        self.color = Color()
        self.scrn = None
        self.choices = None
        self.startrow = 2
        self.endrow = 0
        self.currentrow = 0
        self.startcol = 0
        self.endcol = 0
        self.currentcol = 0
        
    def list(self, prompt, choices, quit, position):
        """Single column menu positioned on right.  Width is 40 and
        limited to 36 characters across.  Height is variable but limited
        to 22 rows.  Requires four arguments: prompt, choices, quit and
        position.
        
        (prompt) is a choices of formatted entries making up the question
        presented to the player.
        
        (choices) is a choices of items to select from.  When selected, the
        choices item will be passed back to the calling function.
        
        (quit) is a toggle for whether a quit function is enabled or not.
        If (quit) is 1, input of "Q" or "q" will close the window.  If
        (quit) is 0, the quit function is not enabled and only a
        selection will close the window.
        
        (position) determines what side of the screen the menu will
        appear on.  Takes "left" or "right" and positions accordingly.
        
        """
        rows = len(prompt) + len(choices) + 5
        if position == "left":
            col = 2
        elif position == "right":
            col = 40
        else:
            col = 2 # To error out if wrong input
        self.scrn = curses.newwin(rows, 38, 1, col)
        self.scrn.keypad(1)
        self.choices = choices
        for line in prompt:
            self.scrn.addstr(self.startrow, 2, line, self.color.MAGENTA)
            self.startrow += 1
        self.startrow += 1
        self.endrow = self.startrow + len(self.choices)
        self.currentrow = self.startrow
        for item in choices:
            self.scrn.addstr(self.currentrow, 2, item, self.color.GREEN)
            self.currentrow += 1
        self.select(self.startrow)
        self.scrn.box()
        self.scrn.refresh()
        ch = None
        while ch == None:
            ch = self.scrn.getch()
            if ch == curses.KEY_UP:
                self.updown(-1)
            elif ch == curses.KEY_DOWN:
                self.updown(1)
            elif ch == curses.KEY_ENTER or ch == 10:
                self.scrn.keypad(0)
                self.scrn.erase()
                return choices[self.currentrow - self.startrow]
            elif quit == 1 and ch == ord("Q") or \
                 quit == 1 and ch == ord("q"):
                return False
            ch = None
            
    def updown(self, inc):
        row = self.currentrow + inc
        if row >= self.startrow and row < self.endrow:
            self.deselect()
            self.select(row)
            
    def deselect(self):
        deselect = self.choices[self.currentrow - self.startrow]
        self.scrn.addstr(self.currentrow, 2, deselect, self.color.GREEN)
        self.scrn.refresh()
        
    def select(self, row):
        self.currentrow = row
        select = self.choices[self.currentrow - self.startrow]
        self.scrn.addstr(self.currentrow, 2, select, curses.A_BOLD)
        self.scrn.refresh()