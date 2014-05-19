import random
import sys
import pygame
import string
import re
import xml.dom.minidom
from pygame.locals import *
from gamedata import *
from menu import Menu


class CreateCharacter:
    """Creates a new character for Gods & Monsters based on the rules
    defined in the Rule Book beginning on page 6.
    
    """
    def __init__(self):
        self.display = Display()
        self.gamedata = GameData()
        self.chardata = CharacterData().chardata
        
    def createcharacter(self, screen):
        """Initiates the creation of a new character."""
        self.screen = screen
        # Set new character's level to 1
        self.chardata["Level"] = 1
        self.sheet = DisplayCharacter()
        self.generateabilites(screen)
        self.assignabilities(screen)
        self.selectspecies(screen)
        self.setspeciesabilities()
        self.selectgender(screen)
        self.selectarchetype(screen)
        self.selectmoralcode(screen)
        self.setexperience()
        self.setskillpoints()
        self.setsurvival()
        self.setweapons()
        self.setinitialgold()
        self.setsaves()
        self.setsurprise()
        self.setadvantage()
        self.setdefense()
        self.setattackbonus()
        self.setphysicaltraits()
        self.setmovement()
        self.setmojo()
        self.setname(screen)
        # self.chooseskills(screen)
        
        
        self.sheet.printcharactersheet(self.chardata, self.screen)

        while True:
            event = pygame.event.wait()
            if event.type == KEYDOWN:
                if event.key == K_q:
                    exit()
                    
    def generateabilites(self, screen):
        """Rolls six scores at 4d6, discarding the lowest die roll and
        checks to see that at least one is a 9 or higher.  If none are
        at least 9, passes the scores on to give the player the option
        of rolling six more or changing lowest to 18.
        
        """
        scores = []
        # Generate six ability scores
        for i in range(6):
            scores.append(self.rollability())
        # Checks to ensure at least one is 9 or higher.
        # Allows player to roll 6 more or assign 18 if not.
        if max(scores) < 9:
            scores = self.changeprime(scores, screen)
        # Attached modifiers to ability scores for later reference.
        # self.chardata[ability][-1] is set to original value to 
        # account for temporary increases or decreases (curses,
        # magic, etc).
        i = 0
        for score in scores:
            scores[i] = [score, 
                         self.gamedata.ABIL_MODIFIERS[score][0],
                         self.gamedata.ABIL_MODIFIERS[score][1],
                         self.gamedata.ABIL_MODIFIERS[score][2],
                         score
                         ]
            i += 1
        # Assigns scores (temporarily) to abilities
        i = 0
        for ability in self.gamedata.ABIL_NAMES:
            self.chardata[ability] = scores[i]
            i += 1
            
    def rollability(self):
        """Rolls one score at 4d6, discarding lowest and passing it back
        to calling function.
        
        """
        roll = []
        for i in range(4):
            roll.append(random.randint(1, 6))
        return sum(roll) - min(roll)
    
    def changeprime(self, scores, screen):
        """If no abilities are at least 9, gives the player the option
        to roll six more scores, taking the highest of the twelve, or to
        raise the lowest of the six scores to 18.  Then passes them back
        to the calling function.
        
        --Page 11--
        
        """
        prompt = ["Your character's ability scores are",
                  "too low for an archetype selection.",
                  "You may roll six more and take the",
                  "highest of all twelve rolls, or",
                  "increase your lowest score to 18."
                  ]
        choices = ["Roll", "Increase"]
        bg = pygame.image.load(self.display.BG_FULL).convert()
        screen.blit(bg, (0, 0))
        element = "ABILITY SCORES:"
        value = str(scores[0]) + ", " + str(scores[1]) + ", " + \
              str(scores[2]) + ", " + str(scores[3]) + ", " + \
              str(scores[4]) + ", " + str(scores[5])
        row = 14
        col = 2
        text = self.display.FONT.render(element, True,
                                        self.display.WHITE)
        screen.blit(text, (col * self.display.CH_SPACE,
                           row * self.display.CH_SPACE))
        text = self.display.FONT.render(value, True,
                                        self.display.BRIGHT_GREEN)
        screen.blit(text, ((col + 16) * self.display.CH_SPACE,
                           row * self.display.CH_SPACE))
        row += 3
        for line in prompt:
            text = self.display.FONT.render(line.upper(), True,
                                            self.display.BRIGHT_GREEN)
            screen.blit(text, (col * self.display.CH_SPACE,
                               row * self.display.CH_SPACE))
            row += 1
        row = 24
        col = 0
        for item in choices:
            ch = self.display.FONT.render(item[0].upper(), True,
                                          self.display.WHITE)
            screen.blit(ch, (col * self.display.CH_SPACE,
                               row * self.display.CH_SPACE))
            text = self.display.FONT.render(item[1:].upper(), True,
                                            self.display.BRIGHT_GREEN)
            screen.blit(text, ((col + 1) * self.display.CH_SPACE,
                               row * self.display.CH_SPACE))
            col += len(item) + 1
        pygame.display.update()
        while True:
            event = pygame.event.wait()
            if event.type == KEYDOWN:
                if event.key == K_r:
                    for i in range(6):
                        scores.append(self.rollability())
                    for i in range(6):
                        scores.remove(min(scores))
                    return scores
                elif event.key == K_i:
                    lowest = scores.index(min(scores))
                    scores[lowest] = 18
                    return scores
    
    def assignabilities(self, screen):
        """Initiates assignment of ability scores and swaps
        scores a player request.
        
        """
        while True:
            prompta = ["You may customize your character's",
                       "abilities.",
                       "",
                       "Select the first ability to swap, or",
                       "'f' to finish."
                       ]
            promptb = ["You may customize your character's",
                       "abilities.",
                       "",
                       "Select the second ability to swap,",
                       "or 'f' to finish."
                       ]
            while True:
                bg = pygame.image.load(self.display.BG_FULL).convert()
                screen.blit(bg, (0, 0))                
                self.sheet.selectabilities(self.chardata, self.screen)
                row = 24
                col = 0
                ch = self.display.FONT.render("F", True,
                                              self.display.WHITE)
                screen.blit(ch, (col * self.display.CH_SPACE,
                                 row * self.display.CH_SPACE))
                text = self.display.FONT.render("INISH", True,
                                                self.display.BRIGHT_GREEN)
                screen.blit(text, ((col + 1) * self.display.CH_SPACE,
                                   row * self.display.CH_SPACE))
                row = 17
                col = 2
                for line in prompta:
                    text = self.display.FONT.render(line.upper(), True,
                                                    self.display.BRIGHT_GREEN)
                    screen.blit(text, (col * self.display.CH_SPACE,
                                       row * self.display.CH_SPACE))
                    row += 1
                pygame.display.update()
                event = pygame.event.wait()
                if event.type == KEYDOWN:
                    if event.key == K_a:
                        a = "Agility"
                        break
                    elif event.key == K_c:
                        a = "Charisma"
                        break
                    elif event.key == K_e:
                        a = "Endurance"
                        break
                    elif event.key == K_i:
                        a = "Intelligence"
                        break
                    elif event.key == K_w:
                        a = "Wisdom"
                        break
                    elif event.key == K_s:
                        a = "Strength"
                        break
                    elif event.key == K_f:
                        return
            while True:
                bg = pygame.image.load(self.display.BG_FULL).convert()
                screen.blit(bg, (0, 0))                
                self.sheet.selectabilities(self.chardata, self.screen, a)
                row = 24
                col = 0
                ch = self.display.FONT.render("F", True,
                                              self.display.WHITE)
                screen.blit(ch, (col * self.display.CH_SPACE,
                                 row * self.display.CH_SPACE))
                text = self.display.FONT.render("INISH", True,
                                                self.display.BRIGHT_GREEN)
                screen.blit(text, ((col + 1) * self.display.CH_SPACE,
                                   row * self.display.CH_SPACE))
                row = 17
                col = 2
                for line in promptb:
                    text = self.display.FONT.render(line.upper(), True,
                                                    self.display.BRIGHT_GREEN)
                    screen.blit(text, (col * self.display.CH_SPACE,
                                       row * self.display.CH_SPACE))
                    row += 1
                pygame.display.update()
                event = pygame.event.wait()
                if event.type == KEYDOWN:
                    if event.key == K_a:
                        b = "Agility"
                        break
                    elif event.key == K_c:
                        b = "Charisma"
                        break
                    elif event.key == K_e:
                        b = "Endurance"
                        break
                    elif event.key == K_i:
                        b = "Intelligence"
                        break
                    elif event.key == K_w:
                        b = "Wisdom"
                        break
                    elif event.key == K_s:
                        b = "Strength"
                        break
                    elif event.key == K_f:
                        return
            self.chardata[a], self.chardata[b] = \
                self.chardata[b], self.chardata[a]
    
    def selectspecies(self, screen):
        """Allows the player to select a species for their character.
        This deviates somewhat from the rule set, as this would be
        selected as a 'specialty'.  As it is here, this will 'cost' the
        player their specialty, thus only humans will get to select a
        specialty to begin with.
        
        """
        bg = pygame.image.load(self.display.BG_FULL).convert()
        screen.blit(bg, (0, 0))
        menu = Menu()
        self.chardata["Species"] = menu.singlelist(self.gamedata.SPECIES_NAMES,
                                                   2, 2, screen)

    def setspeciesabilities(self):
        """Modifies ability scores based on selected species.  Must be
        done prior to archetype selection in order for proper filtering
        to occur.
        
        """
        species = self.chardata["Species"]
        for i in range(len(self.gamedata.ABIL_NAMES)):
            ability = self.gamedata.ABIL_NAMES[i]
            score = self.chardata[ability][0]
            modifier = self.gamedata.SPECIES[species][0][i]
            self.chardata[ability][0] = self.chardata[ability][-1] = \
                score + modifier
        

    def selectgender(self, screen):
        """Allows the player to select a gender for their character."""
        bg = pygame.image.load(self.display.BG_FULL).convert()
        screen.blit(bg, (0, 0))
        menu = Menu()
        gender = ["Female", "Male"]
        self.chardata["Gender"] = menu.singlelist(gender, 2, 2,screen)
        
    def selectarchetype(self, screen):
        """Checks ability scores and allows player to select from
        available archetype based on primary ability.
        
        --Page 14--
        
        """
        bg = pygame.image.load(self.display.BG_FULL).convert()
        screen.blit(bg, (0, 0))
        choices = []
        # Checks character ability scores against archetype prime
        # ability and appends to the available list if prime is 9 or
        # greater for that archetype
        for archetype in self.gamedata.ARCH:
            prime = self.gamedata.ARCH_ATTRIBUTES[archetype][0]
            if self.chardata[prime][0] > 8:
                choices.append(archetype)
        menu = Menu()
        self.chardata["Archetype"] = menu.singlelist(choices, 2, 2, screen)
        if self.chardata["Archetype"] == "Thief":
            self.chardata["Thief Skill Points"] = 12
        
    def selectmoralcode(self, screen):
        """Checks ability scores and allows player to select from
        available archetype based on primary ability.
        
        --Page 14--
        
        """
        bg = pygame.image.load(self.display.BG_FULL).convert()
        screen.blit(bg, (0, 0))
        menu = Menu()
        self.chardata["Moral Code"] = menu.singlelist(self.gamedata.MORAL_CODES,
                                                      2, 2, screen)

    def setexperience(self):
        """If archetypal ability is 16 or greater, assigns 200 starting
        experience points.  Assigns 0 if not.
        
        --Page 14--
        
        """
        prime = self.gamedata.ARCH_ATTRIBUTES[self.chardata["Archetype"]][0]
        if self.chardata[prime][0] > 15:
            self.chardata["Experience"] = 200
        else:
            self.chardata["Experience"] = 0
            
    def setsurvival(self):
        """Checks archetype for base survival points and then adds that
        to Endurance Major Modifier.
        
        --Page 14 & 35--
        
        """
        survival = self.gamedata.ARCH_ATTRIBUTES[self.chardata["Archetype"]][2]
        modifier = self.chardata["Endurance"][1]
        self.chardata["Survival"] = survival + modifier
        
    def setweapons(self):
        """Checks archetype for initial weapons and type, adding Charisma
        Minor modifier and assigns.
        
        --Page 14 & 33--
        
        """
        weapons = self.gamedata.ARCH_ATTRIBUTES[self.chardata["Archetype"]][5]
        modifier = self.chardata["Charisma"][2]
        self.chardata["Weapon Slots"] = weapons + modifier
        self.chardata["Weapon Type"] = \
            self.gamedata.ARCH_ATTRIBUTES[self.chardata["Archetype"]][6]
        
    def setskillpoints(self):
        """Checks archetype for initial skills and adds Intelligence
        Major, Wisdom Minor and Charisma Minor modifiers.  Assigns the
        total to available skill points.
        
        --Page 14 & 33--
        
        """
        skills = self.gamedata.ARCH_ATTRIBUTES[self.chardata["Archetype"]][4]
        modifier = self.chardata["Intelligence"][1] + \
                 self.chardata["Wisdom"][2] + \
                 self.chardata["Charisma"][2]
        self.chardata["Skill Points"] = skills + modifier
        
    def setinitialgold(self):
        """Checks archetype for number of dice to roll and bonus (+10
        for Monks).  Multiplies dice by 10 and adds bonus plus
        Intelligence, Wisdom and Charisma Major modifiers.
        
        --Page 14 (also archetype description)--
        
        """
        archetype = self.chardata["Archetype"]
        dice = self.gamedata.GOLD_START[archetype][0]
        bonus = self.gamedata.GOLD_START[archetype][1]
        modifier = self.chardata["Intelligence"][1] + \
                 self.chardata["Wisdom"][1] + \
                 self.chardata["Charisma"][1]
        roll = []
        for i in range(dice):
            roll.append(random.randint(1, 6))
        gold = (sum(roll) * 10) + bonus + modifier
        self.chardata["Gold"] = gold
        
    def setsaves(self):
        """Assigns Saving Roll values using 4 as a base and adding Major
        modifier, Minor modifier, Archetype bonus and Species modifiers
        where appropriate.
        
        --Page 35--
        
        """
        for save in self.gamedata.SAVES:
            base = 4
            majorattribute = self.gamedata.SAVES_ATTRIBUTES[save][0]
            major = self.chardata[majorattribute][1]
            minorattribute = self.gamedata.SAVES_ATTRIBUTES[save][1]
            minor = self.chardata[minorattribute][2]
            archetype = self.gamedata.SAVES_ATTRIBUTES[save][2]
            if archetype == self.chardata["Archetype"]:
                bonus = 1
            else:
                bonus = 0
            species = self.chardata["Species"]
            index = self.gamedata.SAVES.index(save)
            specmod = self.gamedata.SPECIES[species][6][index]
            roll = base + major + minor + bonus + specmod
            self.chardata[save] = roll
            
    def setsurprise(self):
        """Assigns Surprise using Perception plus Agility Minor
        modifier.
        
        --Page 36--
        
        """
        perception = self.chardata["Perception"]
        minor = self.chardata["Agility"][2]
        self.chardata["Surprise"] = perception + minor
        
    def setadvantage(self):
        """Assigns Advantage as a sum of Agility Major and Charisma
        Minor modifiers.
        
        --Page 36--
        
        """
        major = self.chardata["Agility"][1]
        minor = self.chardata["Charisma"][2]
        self.chardata["Advantage"] = major + minor

    def setdefense(self):
        """Assigns Defense as Agility Major modifier.
        
        --Page 36--
        
        """
        self.chardata["Defense"] = self.chardata["Agility"][1]
                
    def setattackbonus(self):
        """Close Combat Bonus (Hand Atk) assigned as Strength Minor;
        damage bonus is Strength Major.  Thrown Attack (Thrown Atk) is
        Agility Minor; damage bonus is Strength Minor; range penalty is
        reduced by Strength Minor.  Propelled Attack (Prop Atk) is
        Agility Minor, with no damage bonus.
        
        --Page 36--
        
        """
        str_major = self.chardata["Strength"][1]
        str_minor = self.chardata["Strength"][2]
        agi_minor = self.chardata["Agility"][2]
        # Close Combat Attack: {"Hand Atk": [Attack, Damage]}
        self.chardata["Hand Atk"] = [str_minor, str_major]
        # Thrown Attack: {"Thrown Atk": [Attack, Damage, Range]}
        self.chardata["Thrown Atk"] = [agi_minor, str_minor, str_minor]
        # Propelled Attack: {"Prop Atk": Attack}
        self.chardata["Prop Atk"] = agi_minor
        
    def setphysicaltraits(self):
        """Assigns physical attributes:
            Age = 15 * species modifier plus 1d6 rolled for mod value
            Height = species base + species dice + Str Maj + End Min
            Weight = species base + ((5d6 + Str Maj + End Min) *
                                     species modifier)
        If Age >= 20 then bonus skill points are applied per
        SKILLAGEBONUS.
        
        --Page 36--
        
        """
        # Age
        species = self.chardata["Species"]
        specmod = self.gamedata.SPECIES[species][3]
        if species == "Half-Orc":
            age = int(round(15 + random.randint(1, 6)) * specmod)
            self.chardata["Age"] = age
        else:
            base = 15 * specmod
            dice = specmod
            rolls = 0
            for i in range(dice):
                rolls += random.randint(1, 6)
            age = base + rolls
            self.chardata["Age"] = age
            bonus = 8
            for skillage in self.gamedata.SKILLAGEBONUS:
                if age < skillage:
                    bonus -= 1
                else:
                    break
            self.chardata["Skill Points"] += bonus
        # Height
        base = self.gamedata.SPECIES[species][2][0]
        dice = self.gamedata.SPECIES[species][2][2]
        rolls = 0
        for i in range(dice):
            rolls += random.randint(1, 6)
        height = base + rolls + self.chardata["Strength"][1] + \
               self.chardata["Endurance"][2]
        self.chardata["Height"] = height
        # Weight
        base = self.gamedata.SPECIES[species][2][1]
        dice = 5
        specmod = self.gamedata.SPECIES[species][2][3]
        rolls = 0
        for i in range(dice):
            rolls += random.randint(1, 6)
        weight = base + ((rolls + self.chardata["Endurance"][1] + \
                          self.chardata["Strength"][2]) * specmod)
        self.chardata["Weight"] = weight
        
    def setmovement(self):
        """Assigns movement rate based on species base move modified by
        Agility Major and Strength Minor.  Also assigns Lift and Carry
        according to the character's Strength and multiplying their
        weight against the Lift and Carry values in the table on page
        37.
        
        --Page 37--
        
        """
        # Movement rate
        species = self.chardata["Species"]
        base = self.gamedata.SPECIES[species][4]
        str_major = self.chardata["Strength"][1]
        agi_minor = self.chardata["Agility"][2]
        self.chardata["Movement"] = base + str_major + agi_minor
        # Lift and Carry
        weight = self.chardata["Weight"]
        strength = self.chardata["Strength"][0]
        end_major = self.chardata["Endurance"][1]
        self.chardata["Lift"] = \
            int(round(weight * self.gamedata.LIFTANDCARRY[strength][0]))
        self.chardata["Carry"] = \
            int(round(weight * self.gamedata.LIFTANDCARRY[strength][1] + \
                      (end_major * 10)))
        
    def setmojo(self):
        """Assigns mojo as 10 + Level."""
        level = self.chardata["Level"]
        mojo = 10 + level
        self.chardata["Mojo"] = mojo
        
    def setname(self, screen):
        namegen = NameGenerator()
        name = namegen.generatename(self.chardata)
        prompt = "NAME:"
        while True:
            bg = pygame.image.load(self.display.BG_FULL).convert()
            screen.blit(bg, (0, 0))
            row = 2
            col = 2
            text = self.display.FONT.render(prompt, True, self.display.WHITE)
            self.screen.blit(text, (col * self.display.CH_SPACE,
                                    row * self.display.CH_SPACE))
            col = col + len(prompt) + 1
            text = self.display.FONT.render(name.upper(), True,
                                            self.display.BRIGHT_GREEN)
            self.screen.blit(text, (col * self.display.CH_SPACE,
                                    row * self.display.CH_SPACE))
            row = 24
            col = 0
            ch = self.display.FONT.render("K", True,
                                          self.display.WHITE)
            screen.blit(ch, (col * self.display.CH_SPACE,
                             row * self.display.CH_SPACE))
            text = self.display.FONT.render("EEP", True,
                                            self.display.BRIGHT_GREEN)
            screen.blit(text, ((col + 1) * self.display.CH_SPACE,
                               row * self.display.CH_SPACE))
            col = 5
            ch = self.display.FONT.render("N", True,
                                          self.display.WHITE)
            screen.blit(ch, (col * self.display.CH_SPACE,
                             row * self.display.CH_SPACE))
            text = self.display.FONT.render("EW", True,
                                            self.display.BRIGHT_GREEN)
            screen.blit(text, ((col + 1) * self.display.CH_SPACE,
                               row * self.display.CH_SPACE))
            col = 9
            ch = self.display.FONT.render("C", True,
                                          self.display.WHITE)
            screen.blit(ch, (col * self.display.CH_SPACE,
                             row * self.display.CH_SPACE))
            text = self.display.FONT.render("USTOM", True,
                                            self.display.BRIGHT_GREEN)
            screen.blit(text, ((col + 1) * self.display.CH_SPACE,
                               row * self.display.CH_SPACE))
            pygame.display.update()
            event = pygame.event.wait()
            if event.type == KEYDOWN:
                if event.key == K_k:
                    self.chardata["Name"] = name
                    break
                elif event.key == K_n:
                    name = namegen.generatename(self.chardata)
                elif event.key == K_c:
                    prompt = "CHARACTER NAME:"
                    nameinput = Menu()
                    name = nameinput.textinput(prompt, self.screen)
                    self.chardata["Name"] = name
                    break
                
    def chooseskills(self, screen):
        """Allows player to choose skills for the character.
        
        --Page 35--
        
        """
        selectskills = Skills()
        skills, bonus, points = selectskills(self.chardata, screen)
        self.chardata["Skills"] = skills
        self.chardata["Bonus Skill"] = bonus
        self.chardata["Skill Points"] = points
        self.sheet.printcharactersheet(self.chardata, self.screen)
        
    
class NameGenerator:
    """Generates a name based on the character's species and gender."""
    
    def __init__(self):
        self.NONTERMINAL = re.compile(r"<(\w+)>")
        self.ELF = {"name": ["<start><middle><end>"],
                    "start": ["An", "Bel", "Cel", "El", "Elr", "Elv", "Eow",
                              "Ear", "F", "G", "Gal", "Gl", "Is", "Leg", "Lom",
                              "N", "S", "T", "Thr", "Tin"],
                    "middle": ["a", "adrie", "ara", "e", "ebri", "i", "io",
                               "ithra", "ilma", "il-Ga", "o", "orfi", "u", "y"],
                    "end": ["l", "", "las", "lad", "ldor", "ldur", "linde",
                            "lith", "mir", "n", "nd", "ndel", "ndil", "ndir",
                            "nduil", "ng", "mbor", "r", "rith", "ril", "riand",
                            "rion", "thien", "viel", "wen", "wyn"]
                    }
        self.HALFORC = {"name": ["<start><middle><end>"],
                        "start": ["B", "C", "D", "Er", "F", "G", "Gr", "H", "K",
                                  "L", "M", "N", "P", "Pr", "R", "S", "T", "V",
                                  "Vr"],
                        "middle": ["a", "i", "o", "u"],
                        "end": ["dak", "dash", "dish", "dush", "gak", "gar",
                                "gor", "gdush", "hai", "l", "lo", "lok",
                                "gdish", "k", "kar", "kor", "lg", "mak", "nak",
                                "nai", "ng", "nk", "rag", "rbag", "rg", "rk", 
                                "rt", "ruk", "shnak"]
                        }
        self.GOBLIN = {"name": ["<start><end>"],
                       "start": ["Big", "Bo", "Dof", "Gim", "Gof", "It", "Kim",
                                 "Leb", "Lib", "Luk", "Mor", "Nif", "Nog",
                                 "Nuf", "Rat", "Rub", "Shek", "Shim", "Skar",
                                 "Tid", "Tip", "Tob", "Top", "Zib", "Zig"],
                       "end": ["bez", "bit", "ess", "fen", "gash", "gin", "git",
                               "glum", "ink", "itz", "iz", "let", "lid", "lik",
                               "lob", "mink", "rak", "rut", "sham", "snik",
                               "sub", "sus", "wig", "zag", "zib"]
                       }
        self.DWARF = {"name": ["<start><middle><end>"],
                      "start": ["B", "D", "F", "G", "Gl", "H", "K", "L", "M",
                                "N", "R", "S", "T", "V"],
                      "middle": ["a", "e", "i", "o", "oi", "u"],
                      "end": ["bur", "fur", "gan", "gnus", "gnar", "li", "lin",
                              "lir", "mli", "nar", "nus", "rin", "ran", "sin",
                              "sil", "sur"]
                      }
        self.GNOME = {"name": ["<start><middle><end>"],
                      "start": ["Aeth", "Addr", "Bl", "C", "Car", "D", "G",
                                "Gl", "Gw", "L", "M", "Ow", "R", "Rh", "S", "T",
                                "V", "Yr"],
                      "middle": ["a", "ae", "e", "eo", "i", "o", "u", "y"],
                      "end": ["bryn", "c", "cyn", "dd", "ddry", "ddyn", "doc",
                              "dry", "gwyn", "llyn", "myr", "n", "nnyn", "nry",
                              "nvan", "nyc", "r", "rcyn", "rraent", "ran",
                              "ryn"]
                      }
        self.HUMAN_M2 = {"name": ["<start><end>"],
                         "start": ["A", "Ab", "Ac", "Ad", "Af", "Agr", "Ast",
                                   "As", "Al", "Adw", "Adr", "Ar", "B", "Br",
                                   "C", "C", "C", "Cr", "Ch", "Cad", "D", "Dr",
                                   "Dw", "Ed", "Eth", "Et", "Er", "El", "Eow",
                                   "F", "Fr", "G", "Gr", "Gw", "Gw", "Gal",
                                   "Gl", "H", "Ha", "Ib", "Jer", "K", "Ka",
                                   "Ked", "L", "Loth", "Lar", "Leg", "M", "Mir",
                                   "N", "Nyd", "Ol", "Oc", "On", "P", "Pr", "R",
                                   "Rh", "S", "Sev", "T", "Tr", "Th", "Th", "V",
                                   "Y", "Yb", "Z", "W", "W", "Wic"],
                         "end": ["a", "ae", "ae", "au", "ao", "are", "ale",
                                 "ali", "ay", "ardo", "e", "ei", "ea", "ea",
                                 "eri", "era", "ela", "eli", "enda", "erra",
                                 "i", "ia", "ie", "ire", "ira", "ila", "ili",
                                 "ira", "igo", "o", "oa", "oi", "oe", "ore", 
                                 "u", "y"]
                         }
            
        self.HUMAN_M3 = {"name": ["<start><middle><end>"],
                         "start": ["A", "Ab", "Ac", "Ad", "Af", "Agr", "Ast",
                                   "As", "Al", "Adw", "Adr", "Ar", "B", "Br",
                                   "C", "C", "C", "Cr", "Ch", "Cad", "D", "Dr",
                                   "Dw", "Ed", "Eth", "Et", "Er", "El", "Eow",
                                   "F", "Fr", "G", "Gr", "Gw", "Gw", "Gal",
                                   "Gl", "H", "Ha", "Ib", "Jer", "K", "Ka",
                                   "Ked", "L", "Loth", "Lar", "Leg", "M", "Mir",
                                   "N", "Nyd", "Ol", "Oc", "On", "P", "Pr", "R",
                                   "Rh", "S", "Sev", "T", "Tr", "Th", "Th", "V",
                                   "Y", "Yb", "Z", "W", "W", "Wic"],
                         "middle": ["a", "ae", "ae", "au", "ao", "are", "ale",
                                    "ali", "ay", "ardo", "e", "ei", "ea", "ea",
                                    "eri", "era", "ela", "eli", "enda", "erra",
                                    "i", "ia", "ie", "ire", "ira", "ila", "ili",
                                    "ira", "igo", "o", "oa", "oi", "oe", "ore",
                                    "u", "y"],
                         "end": ["a", "and", "b", "bwyn", "baen", "bard", "c",
                                 "ctred", "cred", "ch", "can", "d", "dan",
                                 "don", "der", "dric", "dfrid", "dus", "f", "g",
                                 "gord", "gan", "l", "li", "lgrin", "lin",
                                 "lith", "lath", "loth", "ld", "ldric", "ldan",
                                 "m", "mas", "mos", "mar", "mond", "n", "nydd",
                                 "nidd", "nnon", "nwan", "nyth", "nad", "nn",
                                 "nnor", "nd", "p", "r", "ron", "rd", "s", "sh",
                                 "seth", "sean", "t", "th", "th", "tha", "tlan",
                                 "trem", "tram", "v", "vudd", "w", "wan", "win",
                                 "win", "wyn", "wyn", "wyr", "wyr", "wyth"]
                         }
        self.HUMAN_F2 = {"name": ["<start><end>"],
                         "start": ["A", "Ab", "Ac", "Ad", "Af", "Agr", "Ast",
                                   "As", "Al", "Adw", "Adr", "Ar", "B", "Br",
                                   "C", "C", "C", "Cr", "Ch", "Cad", "D", "Dr",
                                   "Dw", "Ed", "Eth", "Et", "Er", "El", "Eow",
                                   "F", "Fr", "G", "Gr", "Gw", "Gw", "Gal",
                                   "Gl", "H", "Ha", "Ib", "Jer", "K", "Ka",
                                   "Ked", "L", "Loth", "Lar", "Leg", "M", "Mir",
                                   "N", "Nyd", "Ol", "Oc", "On", "P", "Pr", "Q",
                                   "R", "Rh", "S", "Sev", "T", "Tr", "Th", "Th",
                                   "Ul", "Um", "Un", "V", "Y", "Yb", "Z", "W",
                                   "W", "Wic"],
                         "end": ["a", "a", "a", "ae", "ae", "au", "ao", "are",
                                 "ale", "ali", "ay", "ardo", "e", "e", "e",
                                 "ei", "ea", "ea", "eri", "era", "ela", "eli",
                                 "enda", "erra", "i", "i", "i", "ia", "ie",
                                 "ire", "ira", "ila", "ili", "ira", "igo", "o",
                                 "oa", "oi", "oe", "ore", "u", "y"]
                         }
        self.HUMAN_F3 = {"name": ["<start><middle><end>"],
                         "start": ["A", "Ab", "Ac", "Ad", "Af", "Agr", "Ast",
                                   "As", "Al", "Adw", "Adr", "Ar", "B", "Br",
                                   "C", "C", "C", "Cr", "Ch", "Cad", "D", "Dr",
                                   "Dw", "Ed", "Eth", "Et", "Er", "El", "Eow",
                                   "F", "Fr", "G", "Gr", "Gw", "Gw", "Gal",
                                   "Gl", "H", "Ha", "Ib", "Jer", "K", "Ka",
                                   "Ked", "L", "Loth", "Lar", "Leg", "M", "Mir",
                                   "N", "Nyd", "Ol", "Oc", "On", "P", "Pr", "Q",
                                   "R", "Rh", "S", "Sev", "T", "Tr", "Th", "Th",
                                   "Ul", "Um", "Un", "V", "Y", "Yb", "Z", "W",
                                   "W", "Wic"],
                         "middle": ["a", "a", "a", "ae", "ae", "au", "ao",
                                    "are", "ale", "ali", "ay", "ardo", "e", "e",
                                    "e", "ei", "ea", "ea", "eri", "era", "ela",
                                    "eli", "enda", "erra", "i", "i", "i", "ia",
                                    "ie", "ire", "ira", "ila", "ili", "ira", 
                                    "igo", "o", "oa", "oi", "oe", "ore", "u",
                                    "y"],
                         "end": ["beth", "cia", "cien", "clya", "de", "dia",
                                 "dda", "dien", "dith", "dia", "lind", "lith",
                                 "lia", "lian", "lla", "llan", "lle", "ma",
                                 "mma", "mwen", "meth", "n", "n", "n", "nna",
                                 "ndra", "ng", "ni", "nia", "niel", "rith",
                                 "rien", "ria", "ri", "rwen", "sa", "sien",
                                 "ssa", "ssi", "swen", "thien", "thiel", "viel",
                                 "via", "ven", "veth", "wen", "wen", "wen",
                                 "wen", "wia", "weth", "wien", "wiel"]
                         }
        self.HALFLING_M = {"name": ["<start><middle><end>"],
                           "start": ["B", "Dr", "Fr", "Mer", "Per", "R", "S"],
                           "middle": ["a", "e", "i", "ia", "o", "oi", "u"],
                           "end": ["bo", "do", "doc", "go", "grin", "m", "ppi",
                                   "rry"]
                           }
            
        self.HALFLING_F = {"name": ["<start><middle><end>"],
                           "start": ["Al", "Br", "C", "Cl", "D", "El", "Gw",
                                     "J", "L", "M", "N", "Mer", "S", "R", "Ys"],
                           "middle": ["a", "ae", "e", "ea", "i", "o", "u", "y",
                                      "w"],
                           "end": ["brylla", "cla", "dda", "ll", "lla", "llyra",
                                   "lonna", "lyan", "na", "ngwen", "niver",
                                   "noic", "ra", "rka", "ryan", "ssa", "vyan"]
                           }
        
    def generatename(self, chardata):
        species = chardata["Species"]
        gender = chardata["Gender"]
        namegrammar = self.definegrammar(species, gender)
        namestr = random.choice(namegrammar["name"])
        matchnonterminal = self.NONTERMINAL.search(namestr)
        while matchnonterminal:
            substr = random.choice(namegrammar[matchnonterminal.group(1)])
            namestr = self.NONTERMINAL.sub(substr, namestr, 1)
            matchnonterminal = self.NONTERMINAL.search(namestr)
        return namestr   
        
    def definegrammar(self, species, gender):
        if species == "Dwarf":
            return self.DWARF
        elif species == "Elf":
            return self.ELF
        elif species == "Gnome":
            return self.GNOME
        elif species == "Goblin":
            return self.GOBLIN
        elif species == "Halfling" and gender == "Female":
            return self.HALFLING_F
        elif species == "Halfling" and gender == "Male":
            return self.HALFLING_M
        elif species == "Half-Elf":
            roll = random.randint(1, 100)
            if roll < 50 and gender == "Female":
                return self.namehumanfemale()
            elif roll < 50 and gender == "Male":
                return self.namehumanmale()
            else:
                return self.ELF
        elif species == "Half-Orc":
            return self.HALFORC
        elif species == "Human" and gender == "Female":
            return self.namehumanfemale()
        elif species == "Human" and gender == "Male":
            return self.namehumanmale()
                            
    def namehumanfemale(self):
        roll = random.randint(1, 100)
        if roll < 50:
            namegrammar = self.HUMAN_F2
        else:
            namegrammar = self.HUMAN_F3
        return namegrammar
    
    def namehumanmale(self):
        roll = random.randint(1, 100)
        if roll < 50:
            namegrammar = self.HUMAN_M2
        else:
            namegrammar = self.HUMAN_M3
        return namegrammar
                
class Skills:
    """
    This section to be removed
    """
    
    def __init__(self):
        self.gamedata = GameData()
        self.display = Display()
        self.menu = Menu()
        self.row = 2
        self.col = 2
        self.bonusset = 0
        
    def chooseskills(self, chardata, screen):
        self.archetype = chardata["Archetype"]
        self.species = chardata["Species"]
        self.points = chardata["Skill Points"]
        self.initialskills = chardata["Skills"]
        self.bonus = chardata["Bonus"]
        if self.bonus != "":
            self.bonus = 1
        self.setarchetypeskills()
        
    def setarchetypeskills(self):
        """Builds """
        
        
        
        
class DisplayCharacter:
    """Displays the various character sheet screens"""
    
    def __init__(self):
        self.display = Display()
        self.gamedata = GameData()
        
    def printcharactersheet(self, chardata, screen):
        bg = pygame.image.load(self.display.BG_CHAR).convert()
        screen.blit(bg, (0, 0))
        # Personal data
        row = 2
        col = 2
        elements = [chardata["Name"],
                    chardata["Gender"] + " " + chardata["Species"] + " AGE " + \
                    str(chardata["Age"]),
                    chardata["Moral Code"],
                    "LEVEL " + str(chardata["Level"]) + " " + \
                    chardata["Archetype"],
                    "EXP " + str(chardata["Experience"])
                    ]
        for element in elements:
            element = string.upper(element)
            text = self.display.FONT.render(element, True,
                                            self.display.WHITE)
            screen.blit(text, (col * self.display.CH_SPACE,
                               row * self.display.CH_SPACE))
            row += 1
        # Ability scores
        elements = []
        values = []
        for ability in self.gamedata.ABIL_NAMES:
            elements.append(ability)
            values.append(chardata[ability][-1])
        self.printscores(elements, values, (8, 2), 13, 2, screen)
        # Saving throws
        elements = []
        values = []
        for save in self.gamedata.SAVES:
            elements.append(save)
            values.append(chardata[save])
        self.printscores(elements, values, (15, 2), 13, 2, screen)
        # Gold and Mojo
        elements = ["Gold", "Mojo"]
        values = []
        for element in elements:
            values.append(chardata[element])        
        self.printscores(elements, values, (2, 28), 5, 5, screen)
        # Combat scores
        elements = ["Survival", "Defense", "Advantage", "Surprise"]
        values = []
        for element in elements:
            values.append(chardata[element])
        elements.append("Hand Atk")
        values.append(str(chardata["Hand Atk"][0]) + "/" + \
                      str(chardata["Hand Atk"][1]))
        elements.append("Thrown Atk")
        values.append(str(chardata["Thrown Atk"][0]) + "/" + \
                      str(chardata["Thrown Atk"][1]) + "/" + \
                      str(chardata["Thrown Atk"][2]))
        elements.append("Prop Atk")
        values.append(str(chardata["Prop Atk"]))
        self.printscores(elements, values, (8, 19), 11, 8, screen)
        # Movement
        elements = ["Movement", "Height", "Weight", "Lift", "Carry"]
        values = []
        for element in elements:
            values.append(chardata[element])
        self.printscores(elements, values, (16, 19), 11, 8, screen)
        pygame.display.update()
    
    def printscores(self, elements, values, coords, offset, justify, screen):
        """Prints scores block such as ability scores.  (labels) is
        a list of the labels for each of the scores and should match the
        keys contained in the character data.  (scores) is a list of the
        values corresponding to each element.  (coords) is a tuple
        containing (row, col) of the first character placement of the
        block.  (offset) is the column offset that will dictate where the
        first character of the score should be placed.  (justify) is the
        columns to right justify the scores.
        
        """
        row = coords[0]
        col = coords[1]
        for i in range(len(elements)):
            element = string.upper(elements[i])
            value = str(values[i]).rjust(justify)
            text = self.display.FONT.render(element, True,
                                            self.display.WHITE)
            screen.blit(text, (col * self.display.CH_SPACE,
                               row * self.display.CH_SPACE))
            text = self.display.FONT.render(value, True,
                                            self.display.BRIGHT_GREEN)
            screen.blit(text, ((col + offset) * self.display.CH_SPACE,
                               row * self.display.CH_SPACE))
            row += 1
            
    def printabilities(self, chardata, screen):
        """Prints ability scores alone.  Requires (chardata) to be passed
        as well as the (screen).
        
        
        """
        elements = []
        values = []
        for ability in self.gamedata.ABIL_NAMES:
            elements.append(ability)
            values.append(chardata[ability][0])
        self.printscores(elements, values, (8, 2), 13, 2, screen)
        
    def selectabilities(self, chardata, screen, select = ""):
        """Prints ability scores alone.  Requires (chardata) to be passed
        as well as the (screen).  (select) is optional and highlights the
        selected ability if passed.
        
        """
        elements = []
        values = []
        for ability in self.gamedata.ABIL_NAMES:
            elements.append(ability)
            values.append(chardata[ability][0])
        row = 8
        col = 2
        for i in range(len(elements)):
            element = string.upper(elements[i])
            value = str(values[i]).rjust(2)
            if select == elements[i]:
                text = self.display.FONT.render(element, True,
                                                self.display.WHITE)
                screen.blit(text, (col * self.display.CH_SPACE,
                                   row * self.display.CH_SPACE))
            else:
                ch = self.display.FONT.render(element[0], True,
                                              self.display.WHITE)
                screen.blit(ch, (col * self.display.CH_SPACE,
                                 row * self.display.CH_SPACE))
                text = self.display.FONT.render(element[1:], True,
                                                self.display.BRIGHT_MAGENTA)
                screen.blit(text, ((col + 1) * self.display.CH_SPACE,
                                   row * self.display.CH_SPACE))
            text = self.display.FONT.render(value, True,
                                            self.display.BRIGHT_MAGENTA)
            screen.blit(text, ((col + 13) * self.display.CH_SPACE,
                               row * self.display.CH_SPACE))
            row += 1
