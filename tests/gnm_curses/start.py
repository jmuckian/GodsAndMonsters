#!/usr/bin/python

"""Curses interface for Gods & Monsters"""

import curses
import traceback
import char
from display import Color

class Startup:

    
    def intro(self, stdscr):
        stdscr.clear()
        color = Color()
        text0 = "Gods & Monsters.  Copyright (C) 2007 G&M Development Team."
        text1 = "This program comes with ABSOLUTELY NO WARRANTY."
        text2 = "This is free software, and you are welcome to redistribute it"
        text3 = "under certain conditions; for details, see LICENSE.TXT"
        text4 = "Press any key to continue."
        stdscr.addstr(4, 4, text0, color.GREEN)
        stdscr.addstr(5, 4, text1, color.GREEN)
        stdscr.addstr(6, 4, text2, color.GREEN)
        stdscr.addstr(7, 4, text3, color.GREEN)
        stdscr.addstr(10, 4, text4, color.MAGENTA)
        stdscr.refresh()
        ch = None
        while ch == None:
            ch = stdscr.getch()
            
    def menu(self, stdscr):
        stdscr.clear()
        color = Color()
        text0 = "Create new character"
        text1 = "New game"
        text2 = "Quit"
        stdscr.addch(4, 4, text0[0], curses.A_BOLD)
        stdscr.addstr(4, 5, text0[1:], color.GREEN)
        stdscr.addch(5, 4, text1[0], curses.A_BOLD)
        stdscr.addstr(5, 5, text1[1:], color.GREEN)
        stdscr.addch(6, 4, text2[0], curses.A_BOLD)
        stdscr.addstr(6, 5, text2[1:], color.GREEN)
        stdscr.refresh()
        ch = None
        while ch == None:
            ch = stdscr.getch()
            if ch == ord('C') or ch == ord('c'):
                self.newcharacter(stdscr)
            elif ch == ord('N') or ch == ord('n'):
                self.newgame(stdscr)
            elif ch == ord('Q') or ch == ord('q'):
                break
            else:
                ch = None
                
    def newcharacter(self, stdscr):
        character = char.CreateCharacter()
        character.createcharacter(stdscr)
        
    def newgame(self, stdscr):
        pass
    
def main(screen):
    curses.curs_set(0)
    stdscr = screen.subwin(24, 80, 0, 0)
    start = Startup()
    start.intro(stdscr)
    start.menu(stdscr)

    
    
if __name__ == "__main__":
    curses.wrapper(main)
    traceback.print_exc()