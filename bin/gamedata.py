import os
import pygame

class Display:
    """Defines constants relating to the display of the game: colors,
    fonts, images, etc.
    
    """
    def __init__(self):
        # Set colors based on default 16 color EGA palette
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 0, 170)
        self.GREEN = (0, 170 , 0)
        self.CYAN = (0, 170, 170)
        self.RED = (170, 0, 0)
        self.MAGENTA = (170, 0, 170)
        self.BROWN = (170, 85, 0)
        self.LIGHT_GRAY = (170, 170, 170)
        self.DARK_GRAY = (85, 85, 85)
        self.BRIGHT_BLUE = (85, 85, 255)
        self.BRIGHT_GREEN = (85, 255, 85)
        self.BRIGHT_CYAN = (85, 255, 255)
        self.BRIGHT_RED = (255, 85, 85)
        self.BRIGHT_MAGENTA = (255, 85, 255)
        self.BRIGHT_YELLOW = (255, 255, 85)
        self.WHITE = (255, 255, 255)
        self.DATA_PATH = os.curdir + os.sep + "data"
        # Set system font: Old school Gold Box font
        FONTFILE = os.path.join("data", "goldbox.ttf")
        self.FONT = pygame.font.Font(FONTFILE, 16)
        # Set character spacing
        self.CH_SPACE = 16
        # Set background images
        self.BG_FULL = os.path.join("data", "bg_full.png")
        self.BG_MAIN = os.path.join("data", "bg_main.png")
        self.BG_BATTLE = os.path.join("data", "bg_battle.png")
        self.BG_CHAR = os.path.join("data", "bg_full.png")
        self.BG_TITLE = os.path.join("data", "bg_title.png")


class CharacterData:
    """Defines character data to be used within the game."""
    
    def __init__(self):
        self.chardata = {"Agility": [""],
                         "Charisma": [""],
                         "Endurance": [""],
                         "Intelligence": [""],
                         "Wisdom": [""],
                         "Strength": [""],
                         "Archetype": "",
                         "Survival": "",
                         "Weapons": [""],
                         "Weapon Slots": "",
                         "Weapon Type": "",
                         "Skill Points": "",
                         "Skills": {},
                         "Bonus Skill": "",
                         "Specialties": "",
                         "Moral Code": "",
                         "Gold": "",
                         "Evasion": "",
                         "Fortitude": "",
                         "Health": "",
                         "Learning": "",
                         "Perception": "",
                         "Willpower": "",
                         "Surprise": "",
                         "Advantage": "",
                         "Defense": "",
                         "Hand Atk": ["", ""],
                         "Thrown Atk": ["", "", ""],
                         "Prop Atk": "",
                         "Age": "",
                         "Gender": "",
                         "Name": "",
                         "Height": "",
                         "Weight": "",
                         "Movement": "",
                         "Lift": "",
                         "Carry": "",
                         "Species": "",
                         "Mojo": "",
                         "Level": "",
                         "Experience": "",
                         "Thief Skill Points": "",
                         "Thief Skills": {},
                         "Psychic Points": "",
                         "Fatigue Points": "",
                         "Psychic Powers": {}
                         }
        
class GameData:
    """Defines game data to be used within the game.  This consists of
    skills, spells, tables and other such data to be referenced
    throughout the game.
    
    """
    def __init__(self):
        self.ABIL_NAMES = ["Agility",
                           "Charisma",
                           "Endurance",
                           "Intelligence",
                           "Wisdom",
                           "Strength"
                           ]
        self.ABIL_MODIFIERS = {1: [-5, -3, 0],
                               2: [-4, -2, 0],
                               3: [-3, -2, 0],
                               4: [-2, -1, 1],
                               5: [-2, -1, 1],
                               6: [-1, 0, 1],
                               7: [-1, 0, 2],
                               8: [-1, 0, 2],
                               9: [0, 0, 2],
                               10: [0, 0, 2],
                               11: [0, 0, 3],
                               12: [1, 0, 3],
                               13: [1, 0, 3],
                               14: [1, 0, 4],
                               15: [2, 1, 4],
                               16: [2, 1, 4],
                               17: [3, 2, 4],
                               18: [4, 2, 5],
                               19: [5, 2, 5],
                               20: [6, 3, 5],
                               21: [7, 3, 6],
                               22: [8, 3, 6]
                               }
        self.ARCH = ["Warrior",
                     "Thief",
                     "Sorceror",
                     "Prophet",
                     "Monk"
                     ]
        # {Archetype: [Archetypal Ability, Archetypal Save, Base Survival,
        #              Attack Bonus, Skills, Weapons, Weapon Class]
        #              (Weapon Classes: 0 = Simple, 1 = Basic, 2 = Any)
        # --Page 14--
        self.ARCH_ATTRIBUTES = {"Warrior": ["Strength", "Fortitude",
                                            10, 1, 3, 4, 2],
                                "Thief": ["Agility", "Evasion",
                                          6, 0, 5, 2, 1],
                                "Sorceror": ["Intelligence", "Learning",
                                             4, 0, 5, 1, 0],
                                "Prophet": ["Wisdom", "Willpower",
                                            6, 0, 4, 1, 0],
                                "Monk": ["Charisma", "Perception",
                                         6, 0, 4, 1, 0]
                                }
        self.MORAL_CODES = ["Ordered Good", "Good", "Chaotic Good",
                            "Ordered Neutral", "Chaotic Neutral",
                            "Ordered Evil", "Evil", "Chaotic Evil"
                            ]
        # {Archetype: (#d, modifier)  Example: Monk = 1d+10   
        # --Page 14--           
        self.GOLD_START = {"Warrior": (4, 0),
                           "Thief": (2, 0),
                           "Sorceror": (1, 0),
                           "Prophet": (2, 0),
                           "Monk": (1, 10)
                           }   
        self.SAVES = ["Evasion",
                      "Fortitude",
                      "Health",
                      "Learning",
                      "Perception",
                      "Willpower"
                      ]
        # {Save: [Major ability, Minor ability, Archetype]
        # --Page 35--
        self.SAVES_ATTRIBUTES = {"Evasion": ["Agility", "Intelligence",
                                             "Thief"],
                                 "Fortitude": ["Strength", "Endurance",
                                               "Warrior"],
                                 "Health": ["Endurance", "Strength",
                                            "None"],
                                 "Learning": ["Intelligence", "Agility",
                                              "Sorceror"],
                                 "Perception": ["Charisma", "Wisdom",
                                                "Monk"],
                                 "Willpower": ["Wisdom", "Charisma",
                                               "Prophet"]
                                 }
        # {Strength: [Lift multiplier, Carry multiplier]
        # --Page 37--
        self.LIFTANDCARRY = {1: [.01, .003],
                             2: [.04, .013],
                             3: [.09, .03],
                             4: [.16, .053],
                             5: [.25, .083],
                             6: [.36, .12],
                             7: [.49, .16],
                             8: [.64, .21],
                             9: [.81, .27],
                             10: [1.0, .33],
                             11: [1.21, .40],
                             12: [1.44, .48],
                             13: [1.69, .56],
                             14: [1.96, .65],
                             15: [2.25, .75],
                             16: [2.56, .85],
                             17: [2.89, .96],
                             18: [3.24, 1.08],
                             19: [3.61, 1.2],
                             20: [4.0, 1.33],
                             21: [4.41, 1.47],
                             22: [4.84, 1.61]
                             }
        # {Species: [[Agility, Charisma, Endurance, Intelligence, Wisdom,
        #            Strength], [Vision, Penalty], [Base Height, 
        #            Base Weight, Height Dice, Weight], Aging, Move Base,
        #            [Climb Walls, Hide, Move Silently, Locks & Traps,
        #            Understand Languages, Search, Tightrope], 
        #            [Evasion, Fortitude, Health, Learning, Perception,
        #             Willpower], [Species skills]]
        # --Pages 35-38--
        self.SPECIES = {"Dwarf": [[0, -1, 1, 0, 0, 0], ["Underground", -2],
                                  [41, 80, 2, 10], 8, 8, [1, 0, 0, 2, 0, 0, 0],
                                  [0, 0, 2, 0, 0, 0], ["Mountaineering",
                                                       "War Lore",
                                                       "Engineering"]],
                        "Elf": [[1, 0, -1, 0, 0, 0], ["Night", -1],
                                [52, 30, 6, 6], 6, 10, [0, 0, 1, 0, 2, 2, 0],
                                [0, 0, 0, 0, 2, 0], ["Ancient Languages",
                                                     "Herbalism", "Lore",
                                                     "Tracking"]],
                        "Gnome": [[0, 0, 0, 1, -1, 0], ["Night", -1],
                                  [33, 48, 1, 4], 4, 10, [1, 2, 2, 0, 0, 0, 1],
                                  [0, 0, 0, 0, 0, 0], ["Riddling", "Herbalism",
                                                       "Animal Lore", 
                                                       "Tracking"]],
                        "Goblin": [[0, 0, 1, 0, 0, -1], ["Night", -1],
                                   [32, 44, 2, 4], 3, 6, [1, 1, 1, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0], ["Riddling", "Survival",
                                                        "Mountaineering",
                                                        "Tracking",
                                                        "Spelunking"]],
                        "Halfling": [[1, 0, 0, 0, 0, 1], ["Night", -2],
                                     [35, 46, 2, 5], 5, 3, [0, 2, 2, 0, 0, 0, 0],
                                     [0, 0, 1, 0, 0, 0], ["Animal Lore",
                                                          "Local History",
                                                          "Survival"]],
                        "Half-Elf": [[0, 0, 0, 0, 0, 0], ["Night", -2],
                                     [54, 44, 4, 7], 6, 10,
                                     [0, 0, 0, 0, 1, 1, 0], [0, 0, 0, 0, 1, 0],
                                     [""]],
                        "Half-Orc": [[0, -1, 1, 0, 0, 1], ["Underground", -2],
                                     [56, 48, 5, 8], 0.9, 10,
                                     [0, 0, 0, 0, -1, 0, 0], [0, 0, 0, 0, 0, 0],
                                     [""]],
                        "Human": [[0, 0, 0, 0, 0, 0], ["", 0],
                                  [54, 48, 5, 7], 1, 10, [0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0], [""]]
                        }
        self.SPECIES_NAMES = ["Dwarf", "Elf", "Gnome", "Goblin", "Halfling",
                              "Half-Elf", "Half-Orc", "Human"]
        self.SKILLAGEBONUS = [300, 230, 170, 120, 80, 50, 30, 20]
        self.DATAPATH = os.path.join("data")
        self.SKILLFILE = os.path.join(self.DATAPATH, "skills.xml")
        self.SKILL_NAMES = []
        self.SKILLS = {}
        