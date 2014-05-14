"""Gods & Monsters character generator"""

import random
import os
import curses
import xml.dom.minidom
from display import Color, Menu

class CreateCharacter:
    """Creates a new character for Gods & Monsters based on the rules
    outlined in the Player's Guide, beginning on page 6.
    
    """
    def __init__(self):
        self.data = {"Name": "",
                     "Agility": [""],
                     "Charisma": [""],
                     "Endurance": [""],
                     "Intelligence": [""],
                     "Wisdom": [""],
                     "Strength": [""],
                     "Archetype": "",
                     "Survival": ["", ""],
                     "Weapons": [],
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
                     "Close Combat Attack": ["", ""],
                     "Thrown Attack": ["", "", ""],
                     "Propelled Attack": "",
                     "Age": "",
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
                     "Psychic Points": 0,
                     "Fatigue Points": 0,
                     "Psychic Powers": {}
                     }
        
        self.abilitynames = ["Agility",
                             "Charisma",
                             "Endurance",
                             "Intelligence",
                             "Wisdom",
                             "Strength"
                             ]
        
        # {Ability: [Major, Minor, Special]}
        # --Page 13--
        self.abilitymodifiers = {1: [-5, -3, 0],
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
                                 22: [8, 3, 6],
                                 }
        
        self.archetypes = ["Warrior",
                           "Thief",
                           "Sorceror",
                           "Prophet",
                           "Monk"
                           ]
        
        # {Archetype: [Archetypal Ability, Archetypal Save, Base Survival,
        #              Attack Bonus, Skills, Weapons, Weapon Class]
        # Weapon Classes: 0 = Simple, 1 = Basic, 2 = Any
        # --Page 14--
        self.archetypeattr = {"Warrior": ["Strength", "Fortitude",
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
        
        self.moralcodes = ["Ordered Good", "Good", "Chaotic Good",
                           "Ordered", "Chaotic",
                           "Ordered Evil", "Evil", "Chaotic Evil"
                           ]
        
        # {Archetype: (#d, Modifier)}  Example: Monk = 1d+10
        # --Page 14--
        self.startinggold = {"Warrior": (4, 0),
                             "Thief": (2, 0),
                             "Sorceror": (1, 0),
                             "Prophet": (2, 0),
                             "Monk": (1, 10)
                             }
        
        self.savingrolls = ["Evasion",
                            "Fortitude",
                            "Health",
                            "Learning",
                            "Perception",
                            "Willpower"
                            ]
        
        # {Save: [Major Ability, Minor Ability, Archetype]}
        # --Page 34--
        self.savingrollattr = {"Evasion": ["Agility", "Intelligence", "Thief"],
                               "Fortitude": ["Strength", "Endurance",
                                             "Warrior"],
                               "Health": ["Endurance", "Strength", "None"],
                               "Learning": ["Intelligence", "Agility",
                                            "Sorceror"],
                               "Perception": ["Charisma", "Wisdom", "Monk"],
                               "Willpower": ["Wisdom", "Charisma", "Prophet"]
                               }
        
        # {Strength: [Lift Multiplier, Carry Multiplier]
        # --Page --
        self.liftandcarry = {1: [.01, .003],
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
        
        self.sheet = CharacterSheet()
        
    def createcharacter(self, stdscr):
        """Main method responsible for creating the different
        character attributes.
        
        """
        # Set starting character to Level 1
        self.data["Level"] = 1
        self.sheet.printcharacter(stdscr, self)
        self.generateabilities(stdscr)
        self.assignabilities(stdscr)
        self.selectarchetype(stdscr)
        self.startingexperience()
        self.assignsurvival()
        self.assignweapons()
        self.assignskillpoints()
        self.choosespecialty(stdscr)
        self.choosemoralcode(stdscr)
        self.initialgold()
        self.assignsaves()
        self.assignsurprise()
        self.assignadvantage()
        self.assigndefense()
        self.assignattackbonus()
        self.assignphysical()
        self.assignmove()
        self.sheet.printcharacter(stdscr, self)
        self.chooseskills(stdscr)
        
        
        ch = None
        while ch == None:
            ch = stdscr.getch()
            
    def generateabilities(self, stdscr):
        """Rolls six scores at 4d6, discarding the lowest die roll and
        checks to see that at least one is a 9 or higher.  If none are
        at least 9, passes the scores on to give the player the option
        of rolling six more or changing lowest to 18.
        
        --Page 11--
        
        """
        scores = []
        # Generates 6 ability scores
        for i in range(6):
            scores.append(self.rollability())
        # Checks to ensure at least one is 9 or higher.
        # Allows player to roll 6 more or assign 18 if not.
        if max(scores) < 9:
            scores = self.changeprime(scores)
        # Attaches modifiers to ability scores for later reference
        i = 0
        for score in scores:
            scores[i] = [score,
                         self.abilitymodifiers[score][0],
                         self.abilitymodifiers[score][1],
                         self.abilitymodifiers[score][2]
                         ]
            i += 1
        # Assigns scores (temporarily) to abilities
        i = 0
        for ability in self.abilitynames:
            self.data[ability] = scores[i]
            i += 1
            
    def rollability(self):
        """Rolls one score at 4d6, discarding lowest and passing it back
        to calling function.
        
        --Page 11--
        
        """
        roll = []
        for i in range(4):
            roll.append(random.randint(1,6))
        return sum(roll) - min(roll)
    
    def changeprime(self, scores):
        """If no abilities are at least 9, gives the player the option
        to roll six more scores, taking the highest of the twelve, or to
        raise the lowest of the six scores to 18.  Then passes them back
        to the calling function.
        
        --Page 11--
        
        """
        prompt = ["Your characters ability scores",
                  str(scores) + " are too low",
                  "for an archetype selection.",
                  "You may roll six more and take",
                  "the highest six of all twelve",
                  "rolls, or increase your lowest",
                  "score to 18."
                  ]
        choices = ["Roll six more scores",
                   "Increase lowest score to 18"
                   ]
        popup = Menu()
        choice = popup.list(prompt, choices, 0, "right")
        if choice[0] == "R":
            for i in range(6):
                scores.append(self.rollability())
            for i in range(6):
                scores.remove(min(scores))
            return scores
        elif choice[0] == "I":
            lowest = scores.index(min(scores))
            scores[lowest] = 18
            return scores
    
    def assignabilities(self, stdscr):
        """Initiates assignment of ability scores and swaps scores at
        player request.
        
        """
        while True:
            self.sheet.printcharacter(stdscr, self)
            prompta = ["You may customize your character's",
                       "abilities.",
                       "",
                       "Select first ability to swap, or",
                       "'q' to quit."
                       ]
            promptb = ["You may customize your character's",
                       "abilities.",
                       "",
                       "Select second ability to swap, or",
                       "'q' to quit."
                       ]
            choices = self.abilitynames
            popup = Menu()
            a = popup.list(prompta, choices, 1, "right")
            if a == False:
                break
            popup = Menu()
            b = popup.list(promptb, choices, 1, "right")
            if b == False:
                break
            self.data[a], self.data[b] = self.data[b], self.data[a]
        self.sheet.printcharacter(stdscr, self)
        
    def selectarchetype(self, stdscr):
        """Checks ability scores and allows player to select from
        available archetype based on primary ability.
        
        --Page 14--
        
        """
        prompt = ["You may select one of the",
                  "available archetypes based on your",
                  "ability scores."
                  ]
        choices = []
        for archetype in self.archetypes:
            prime = self.archetypeattr[archetype][0]
            if self.data[prime][0] > 8:
                choices.append(archetype)
        popup = Menu()
        choice = popup.list(prompt, choices, 0, "right")
        self.data["Archetype"] = choice
        if self.data["Archetype"] == "Thief":
            self.data["Thief Skill Points"] = 12
        self.sheet.printcharacter(stdscr, self)
        
    def startingexperience(self):
        """If archetypal ability is 16 or greater, assigns 200 starting
        experience.  Assigns 0 if not.
        
        --Page 14
        
        """
        prime = self.archetypeattr[self.data["Archetype"]][0]
        if self.data[prime][0] > 15:
            self.data["Experience"] = 200
        else:
            self.data["Experience"] = 0
    
    def assignsurvival(self):
        """Checks archetype for base survival points and then adds that
        to Endurance Major modifier.  The first value is full survival
        points.  The second value is current survival points.
        
        --Page 14 & 35--
        
        """
        base = self.archetypeattr[self.data["Archetype"]][2]
        modifier = self.data["Endurance"][1]
        survival = base + modifier
        self.data["Survival"] = [survival, survival]
        
    def assignweapons(self):
        """Checks archetype for initial weapons and type, adding Charisma
        Minor modifier and assigns.
        
        --Page 14 & 33---
        
        """
        weapons = self.archetypeattr[self.data["Archetype"]][5]
        modifier = self.data["Charisma"][2]
        self.data["Weapon Slots"] = weapons + modifier
        self.data["Weapon Type"] = \
            self.archetypeattr[self.data["Archetype"]][6]
        
    def assignskillpoints(self):
        """Checks archetype for initial skills and adds Intelligence
        Major, Wisdom Minor and Charisma Minor modifiers.  Assigns the
        total to available skill points.
        
        --Page 14 & 33---
        
        """
        skills = self.archetypeattr[self.data["Archetype"]][4]
        modifier = self.data["Intelligence"][1] + \
                 self.data["Wisdom"][2] + \
                 self.data["Charisma"][2]
        self.data["Skill Points"] = skills + modifier
        
    def choosespecialty(self, stdscr):
        """Placeholder for specialties.  Requires XML data."""
        pass
    
    def choosemoralcode(self, stdscr):
        """Allows player to choose a moral code for the character.
        
        --Page 29--
        
        """
        prompt = ["Select a moral code for your",
                  "character."
                  ]
        choices = self.moralcodes
        popup = Menu()
        choice = popup.list(prompt, choices, 0, "right")
        self.data["Moral Code"] = choice
        self.sheet.printcharacter(stdscr, self)
        
    def initialgold(self):
        """Check archetype for number of dice to roll and bonus (+10
        for Monks).  Multiplies dice by 10 and adds bonus plus
        Intelligence, Wisdom and Charisma Major modifiers.
        
        --Page 14 (also each archetype description)--
        
        """
        archetype = self.data["Archetype"]
        dice = self.startinggold[archetype][0]
        bonus = self.startinggold[archetype][1]
        modifiers = self.data["Intelligence"][1] + \
                  self.data["Wisdom"][1] + \
                  self.data["Charisma"][1]
        roll = []
        for i in range(dice):
            roll.append(random.randint(1,6))
        gold = (sum(roll) * 10) + bonus + modifiers
        self.data["Gold"] = gold
        
    def assignsaves(self):
        """Assign saving roll values using 4 as a base and adding Major
        modifier, Minor modifier, and archetype bonus where appropriate.
        
        --Page 35--
        
        """
        for save in self.savingrolls:
            base = 4
            majorattr = self.savingrollattr[save][0]
            major = self.data[majorattr][1]
            minorattr = self.savingrollattr[save][1]
            minor = self.data[minorattr][2]
            archetype = self.savingrollattr[save][2]
            if archetype == self.data["Archetype"]:
                bonus = 1
            else:
                bonus = 0
            roll = base + major + minor + bonus
            self.data[save] = roll
            
    def assignsurprise(self):
        """Assigns Surprise using Perception plus Agility Minor
        modifier.
        
        --Page 36--
        
        """
        perception = self.data["Perception"]
        minor = self.data["Agility"][2]
        self.data["Surprise"] = perception + minor
        
    def assignadvantage(self):
        """Assigns Advantage as a sum of Agility Major and Charisma
        Minor modifiers.
        
        --Page 36--
        
        """
        major = self.data["Agility"][1]
        minor = self.data["Charisma"][2]
        self.data["Advantage"] = major + minor
        
    def assigndefense(self):
        """Assigns Defense as Agility Major modifier.
        
        --Page 36--
        
        """
        self.data["Defense"] = self.data["Agility"][1]
        
    def assignattackbonus(self):
        """Close Combat assigned as Strength Minor/Damage Bonus is
        Strength Major.  Thrown Attack is Agility Minor/Damage Bonus is
        Strength Minor/Range Penalty are reduced by Strength Minor.
        Propelled Attack is Agility Minor, with no Damage Bonus.
        
        --Page 36--
        
        """
        str_major = self.data["Strength"][1]
        str_minor = self.data["Strength"][2]
        agi_minor = self.data["Agility"][2]
        # Close Combat Attack: [Attack, Damage]
        self.data["Close Combat Attack"] = [str_minor, str_major]
        # Thrown Attack: [Attack, Damage, Range]
        self.data["Thrown Attack"] = [agi_minor, str_minor, str_minor]
        # Propelled Attack: Attack
        self.data["Propelled Attack"] = agi_minor
        
    def assignphysical(self):
        """Assigns physical attributes:
            Age = 15 + 1d6
            Height = 54 + 5d6 + Strength Major + Endurance Major
            Weight = 48 + ((5d6 + Strength Minor + Endurance Major) * 7)
        If Age >= 20 then add 1 bonus Skill Point.
        
        --Page 36--
        
        """
        # Age
        age = 15 + random.randint(1, 6)
        self.data["Age"] = age
        if age >= 20:
            self.data["Skill Points"] += 1
        # Height
        base = 54
        roll = []
        for i in range(5):
            roll.append(random.randint(1, 6))
        height = base + sum(roll) + self.data["Strength"][1] + \
               self.data["Endurance"][2]
        self.data["Height"] = height
        # Weight
        base = 48
        roll = []
        for i in range(5):
            roll.append(random.randint(1, 6))
        weight = base + ((sum(roll) + self.data["Endurance"][1] + \
                          self.data["Strength"][2]) * 7)
        self.data["Weight"] = weight
        
    def assignmove(self):
        """Assigns Movement rate with a base of 10 modified by Agility
        Major and Strength Minor.  Also assigns Lift and Carry according
        to the character's Strength and multiplying their weight against
        the Lift and Carry values in the table on page 37.
        
        --Page 37--
        
        """
        # Movement rate
        movebase = 10
        movemajor = self.data["Agility"][1]
        moveminor = self.data["Strength"][2]
        self.data["Movement"] = movebase + movemajor + moveminor
        # Lift and Carry (rounded to the nearest whole number)
        weight = self.data["Weight"]
        strength = self.data["Strength"][0]
        endurancemajor = self.data["Endurance"][1]
        self.data["Lift"] = round(weight * self.liftandcarry[strength][0])
        self.data["Carry"] = round(weight * self.liftandcarry[strength][1] + \
                                   (endurancemajor * 10))
        
    def chooseskills(self, stdscr):
        popup = Skills()
        
        
class Skills:
    
    
    def __init__(self):
        self.skillnames =[]
        self.skills = {}
        skillfile = os.curdir + os.sep + "data" + os.sep + "skills.xml"
        self.doc = xml.dom.minidom.parse(skillfile)
        self.getvalues()
        
    def getvalues(self):
        """Parses the 'skills.xml' file and builds (self.skillname) and
        (self.skills).
        
        """
        for skill in self.doc.getElementsByTagName("skill"):
            desc = []
            arch = []
            abil = ""
            skillname = skill.childNodes[0].nodeValue.strip()
            self.skillnames.append(skillname)
            try:
                for description in skill.getElementsByTagName("description"):
                    desc.append(description.childNodes[0].nodeValue.strip())
            except:
                desc = [""]
            for archetype in skill.getElementsByTagName("archetype"):
                list = archetype.childNodes[0].nodeValue.aplit(',')
                for item in list:
                    arch.append(item.strip())
            for ability in skill.getElementsByTagName("ability"):
                abil = ability.childNodes[0].nodeValue.strip()
            self.skills[skillname] = [abil, arch, desc]
        self.skillnames.sort()
        
    def chooseskills(self, screen, character):
        """Main method for selecting skills.
        
        For new characters, allows player to select one skill outside
        their archetype to cost 1 point.  Then allows player to select
        skills for their character, reducing total skill points available
        by 1 or 2 depending on archetype.
        
        """
        self.archetype = character.data["Archetype"]
        self.points = character.data["Skill Points"]
        self.bonus = character.data["Bonus Skill"]
        if self.bonus == "":
            self.bonusset = 0
        else:
            self.bonusset = 1
        self.initial = character.data["Skills"]
        
            
        
        
        
class CharacterSheet:
    """Main class for displaying character information"""
    
    def printcharacter(self, screen, character):
        color = Color()
        screen.clear()
        screen.addstr(2, 4, character.data["Name"], color.WHITE)
        text = character.data["Moral Code"] + " " + character.data["Species"]
        screen.addstr(3, 4, text, color.WHITE)
        text = "Level " + str(character.data["Level"]) + " " + \
                              character.data["Archetype"]
        screen.addstr(4, 4, text, color.WHITE)
        screen.addstr(5, 4, "EXP: " + str(character.data["Experience"]),
                      color.WHITE)
        i = 7
        for ability in character.abilitynames:
            screen.addstr(i, 4, ability, color.WHITE)
            screen.addstr(i, 18, str(character.data[ability][0]), color.GREEN)
            i += 1
        i = 14
        for save in character.savingrolls:
            screen.addstr(i, 4, save, color.WHITE)
            screen.addstr(i, 18, str(character.data[save]), color.GREEN)
            i += 1
        screen.addstr(2, 30, "Height:", color.WHITE)
        screen.addstr(2, 44, str(character.data["Height"]), color.GREEN)
        screen.addstr(3, 30, "Weight:", color.WHITE)
        screen.addstr(3, 44, str(character.data["Weight"]), color.GREEN)
        screen.addstr(4, 30, "Age:", color.WHITE)
        screen.addstr(4, 44, str(character.data["Age"]), color.GREEN)
        screen.addstr(7, 30, "Survival:", color.WHITE)
        screen.addstr(7, 44, str(character.data["Survival"][1]), color.GREEN)
        screen.addstr(8, 30, "Defense:", color.WHITE)
        screen.addstr(8, 44, str(character.data["Defense"]), color.GREEN)
        screen.addstr(9, 30, "Advantage:", color.WHITE)
        screen.addstr(9, 44, str(character.data["Advantage"]), color.GREEN)
        screen.addstr(10, 30, "Surprise:", color.WHITE)
        screen.addstr(10, 44, str(character.data["Surprise"]), color.GREEN)
        handattack = str(character.data["Close Combat Attack"][0]) + "/" + \
                   str(character.data["Close Combat Attack"][1])
        screen.addstr(11, 30, "Hand Atk.:", color.WHITE)
        screen.addstr(11, 44, handattack, color.GREEN)
        thrownattack = str(character.data["Thrown Attack"][0]) + "/" + \
                     str(character.data["Thrown Attack"][1]) + "/" + \
                     str(character.data["Thrown Attack"][2])
        screen.addstr(12, 30, "Thrown Atk.:", color.WHITE)
        screen.addstr(12, 44, thrownattack, color.GREEN)
        screen.addstr(13, 30, "Prop. Atk.:", color.WHITE)
        screen.addstr(13, 44, str(character.data["Propelled Attack"]),
                      color.GREEN)
        screen.addstr(15, 30, "Movement:", color.WHITE)
        screen.addstr(15, 44, str(character.data["Movement"]), color.GREEN)
        screen.addstr(16, 30, "Carry:", color.WHITE)
        screen.addstr(16, 44, str(character.data["Carry"]), color.GREEN)
        screen.addstr(17, 30, "Lift:", color.WHITE)
        screen.addstr(17, 44, str(character.data["Lift"]), color.GREEN)
        screen.addstr(18, 30, "Mojo:", color.WHITE)
        screen.addstr(18, 44, str(character.data["Mojo"]), color.GREEN)
        screen.addstr(19, 30, "Gold:", color.WHITE)
        screen.addstr(19, 44, str(character.data["Gold"]), color.GREEN)
        screen.addstr(2, 51, "SKILLS:", color.WHITE)
        row = 3
        for skill in character.data["Skills"]:
            screen.addstr(row, 53, skill, color.WHITE)
            screen.addstr(row, 65, str(character.data["Skills"][skill]),
                          color.GREEN)
            row += 1
        screen.addstr(13, 51, "WEAPONS:", color.WHITE)
        row = 14
        for weapon in character.data["Weapons"]:
            screen.addstr(row, 53, weapon, color.WHITE)
            row += 1
        screen.addstr(20, 51, "SPECIALTIES:", color.WHITE)
        screen.addstr(21, 53, "<SPECIALTY", color.WHITE)
        screen.refresh()
            