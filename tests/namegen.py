import random
import re

renonterminal = re.compile(r"<(\w+)>")

def namegen(namegrammar):
    namestr = random.choice(namegrammar["name"])
    matchnonterminal = renonterminal.search(namestr)
    while matchnonterminal:
        substr = random.choice(namegrammar[matchnonterminal.group(1)])
        namestr = renonterminal.sub(substr, namestr, 1)
        matchnonterminal = renonterminal.search(namestr)
    return namestr

elf = {"name": ["<start><middle><end>"],
          "start": ["An", "Bel", "Cel", "El", "Elr", "Elv", "Eow", "Ear", "F",
                    "G", "Gal", "Gl", "Is", "Leg", "Lom", "N", "S", "T", "Thr",
                    "Tin"],
          "middle": ["a", "adrie", "ara", "e", "ebri", "i", "io", "ithra",
                     "ilma", "il-Ga", "o", "orfi", "u", "y"],
          "end": ["l", "", "las", "lad", "ldor", "ldur", "linde", "lith",
                  "mir", "n", "nd", "ndel", "ndil", "ndir", "nduil", "ng",
                  "mbor", "r", "rith", "ril", "riand", "rion", "thien", "viel",
                  "wen", "wyn"]
          }

halforc = {"name": ["<start><middle><end>"],
           "start": ["B", "C", "D", "Er", "F", "G", "Gr", "H", "K", "L", "M",
                     "N", "P", "Pr", "R", "S", "T", "V", "Vr"],
           "middle": ["a", "i", "o", "u"],
           "end": ["dak", "dash", "dish", "dush", "gak", "gar", "gor", "gdush",
                   "hai", "l", "lo", "lok", "gdish", "k", "kar", "kor", "lg",
                   "mak", "nak", "nai", "ng", "nk", "rag", "rbag", "rg", "rk",
                   "rt", "ruk", "shnak"]
           }

goblin = {"name": ["<start><end>"],
          "start": ["Big", "Bo", "Dof", "Gim", "Gof", "It", "Kim", "Leb", "Lib",
                    "Luk", "Mor", "Nif", "Nog", "Nuf", "Rat", "Rub", "Shek",
                    "Shim", "Skar", "Tid", "Tip", "Tob", "Top", "Zib", "Zig"],
          "end": ["bez", "bit", "ess", "fen", "gash", "gin", "git", "glum",
                  "ink", "itz", "iz", "let", "lid", "lik", "lob", "mink", "rak",
                  "rut", "sham", "snik", "sub", "sus", "wig", "zag", "zib"]
          }

dwarf = {"name": ["<start><middle><end>"],
         "start": ["B", "D", "F", "G", "Gl", "H", "K", "L", "M", "N", "R", "S",
                   "T", "V"],
         "middle": ["a", "e", "i", "o", "oi", "u"],
         "end": ["bur", "fur", "gan", "gnus", "gnar", "li", "lin", "lir", "mli",
                 "nar", "nus", "rin", "ran", "sin", "sil", "sur"]
         }
         
gnome = {"name": ["<start><middle><end>"],
         "start": ["Aeth", "Addr", "Bl", "C", "Car", "D", "G", "Gl", "Gw", "L",
                   "M", "Ow", "R", "Rh", "S", "T", "V", "Yr"],
         "middle": ["a", "ae", "e", "eo", "i", "o", "u", "y"],
         "end": ["bryn", "c", "cyn", "dd", "ddry", "ddyn", "doc", "dry", "gwyn",
                 "llyn", "myr", "n", "nnyn", "nry", "nvan", "nyc", "r", "rcyn",
                 "rraent", "ran", "ryn"]
         }

human_m2 = {"name": ["<start><end>"],
            "start": ["A", "Ab", "Ac", "Ad", "Af", "Agr", "Ast", "As", "Al",
                      "Adw", "Adr", "Ar", "B", "Br", "C", "C", "C", "Cr", "Ch",
                      "Cad", "D", "Dr", "Dw", "Ed", "Eth", "Et", "Er", "El",
                      "Eow", "F", "Fr", "G", "Gr", "Gw", "Gw", "Gal", "Gl", "H",
                      "Ha", "Ib", "Jer", "K", "Ka", "Ked", "L", "Loth", "Lar",
                      "Leg", "M", "Mir", "N", "Nyd", "Ol", "Oc", "On", "P",
                      "Pr", "R", "Rh", "S", "Sev", "T", "Tr", "Th", "Th", "V",
                      "Y", "Yb", "Z", "W", "W", "Wic"],
            "end": ["a", "ae", "ae", "au", "ao", "are", "ale", "ali", "ay",
                       "ardo", "e", "ei", "ea", "ea", "eri", "era", "ela",
                       "eli", "enda", "erra", "i", "ia", "ie", "ire", "ira",
                       "ila", "ili", "ira", "igo", "o", "oa", "oi", "oe", "ore",
                       "u", "y"]
            }
            
human_m3 = {"name": ["<start><middle><end>"],
            "start": ["A", "Ab", "Ac", "Ad", "Af", "Agr", "Ast", "As", "Al",
                      "Adw", "Adr", "Ar", "B", "Br", "C", "C", "C", "Cr", "Ch",
                      "Cad", "D", "Dr", "Dw", "Ed", "Eth", "Et", "Er", "El",
                      "Eow", "F", "Fr", "G", "Gr", "Gw", "Gw", "Gal", "Gl", "H",
                      "Ha", "Ib", "Jer", "K", "Ka", "Ked", "L", "Loth", "Lar",
                      "Leg", "M", "Mir", "N", "Nyd", "Ol", "Oc", "On", "P",
                      "Pr", "R", "Rh", "S", "Sev", "T", "Tr", "Th", "Th", "V",
                      "Y", "Yb", "Z", "W", "W", "Wic"],
            "middle": ["a", "ae", "ae", "au", "ao", "are", "ale", "ali", "ay",
                       "ardo", "e", "ei", "ea", "ea", "eri", "era", "ela",
                       "eli", "enda", "erra", "i", "ia", "ie", "ire", "ira",
                       "ila", "ili", "ira", "igo", "o", "oa", "oi", "oe", "ore",
                       "u", "y"],
            "end": ["a", "and", "b", "bwyn", "baen", "bard", "c", "ctred",
                    "cred", "ch", "can", "d", "dan", "don", "der", "dric",
                    "dfrid", "dus", "f", "g", "gord", "gan", "l", "li", "lgrin",
                    "lin", "lith", "lath", "loth", "ld", "ldric", "ldan", "m",
                    "mas", "mos", "mar", "mond", "n", "nydd", "nidd", "nnon",
                    "nwan", "nyth", "nad", "nn", "nnor", "nd", "p", "r", "ron",
                    "rd", "s", "sh", "seth", "sean", "t", "th", "th", "tha",
                    "tlan", "trem", "tram", "v", "vudd", "w", "wan", "win",
                    "win", "wyn", "wyn", "wyr", "wyr", "wyth"]
            }
human_f2 = {"name": ["<start><end>"],
             "start": ["A", "Ab", "Ac", "Ad", "Af", "Agr", "Ast", "As", "Al",
                       "Adw", "Adr", "Ar", "B", "Br", "C", "C", "C", "Cr", "Ch",
                       "Cad", "D", "Dr", "Dw", "Ed", "Eth", "Et", "Er", "El",
                       "Eow", "F", "Fr", "G", "Gr", "Gw", "Gw", "Gal", "Gl",
                       "H", "Ha", "Ib", "Jer", "K", "Ka", "Ked", "L", "Loth",
                       "Lar", "Leg", "M", "Mir", "N", "Nyd", "Ol", "Oc", "On",
                       "P", "Pr", "Q", "R", "Rh", "S", "Sev", "T", "Tr", "Th",
                       "Th", "Ul", "Um", "Un", "V", "Y", "Yb", "Z", "W", "W",
                       "Wic"],
             "end": ["a", "a", "a", "ae", "ae", "au", "ao", "are", "ale",
                        "ali", "ay", "ardo", "e", "e", "e", "ei", "ea", "ea",
                        "eri", "era", "ela", "eli", "enda", "erra", "i", "i",
                        "i", "ia", "ie", "ire", "ira", "ila", "ili", "ira",
                        "igo", "o", "oa", "oi", "oe", "ore", "u", "y"]
             }

human_f3 = {"name": ["<start><middle><end>"],
             "start": ["A", "Ab", "Ac", "Ad", "Af", "Agr", "Ast", "As", "Al",
                       "Adw", "Adr", "Ar", "B", "Br", "C", "C", "C", "Cr", "Ch",
                       "Cad", "D", "Dr", "Dw", "Ed", "Eth", "Et", "Er", "El",
                       "Eow", "F", "Fr", "G", "Gr", "Gw", "Gw", "Gal", "Gl",
                       "H", "Ha", "Ib", "Jer", "K", "Ka", "Ked", "L", "Loth",
                       "Lar", "Leg", "M", "Mir", "N", "Nyd", "Ol", "Oc", "On",
                       "P", "Pr", "Q", "R", "Rh", "S", "Sev", "T", "Tr", "Th",
                       "Th", "Ul", "Um", "Un", "V", "Y", "Yb", "Z", "W", "W",
                       "Wic"],
             "middle": ["a", "a", "a", "ae", "ae", "au", "ao", "are", "ale",
                        "ali", "ay", "ardo", "e", "e", "e", "ei", "ea", "ea",
                        "eri", "era", "ela", "eli", "enda", "erra", "i", "i",
                        "i", "ia", "ie", "ire", "ira", "ila", "ili", "ira",
                        "igo", "o", "oa", "oi", "oe", "ore", "u", "y"],
             "end": ["beth", "cia", "cien", "clya", "de", "dia", "dda", "dien",
                     "dith", "dia", "lind", "lith", "lia", "lian", "lla",
                     "llan", "lle", "ma", "mma", "mwen", "meth", "n", "n", "n",
                     "nna", "ndra", "ng", "ni", "nia", "niel", "rith", "rien",
                     "ria", "ri", "rwen", "sa", "sien", "ssa", "ssi", "swen",
                     "thien", "thiel", "viel", "via", "ven", "veth", "wen",
                     "wen", "wen", "wen", "wia", "weth", "wien", "wiel"]
             }

halfling_m = {"name": ["<start><middle><end>"],
              "start": ["B", "Dr", "Fr", "Mer", "Per", "R", "S"],
              "middle": ["a", "e", "i", "ia", "o", "oi", "u"],
              "end": ["bo", "do", "doc", "go", "grin", "m", "ppi", "rry"]
              }
            
halfling_f = {"name": ["<start><middle><end>"],
              "start": ["Al", "Br", "C", "Cl", "D", "El", "Gw", "J", "L", "M",
                        "N", "Mer", "S", "R", "Ys"],
              "middle": ["a", "ae", "e", "ea", "i", "o", "u", "y", "w"],
              "end": ["brylla", "cla", "dda", "ll", "lla", "llyra", "lonna",
                      "lyan", "na", "ngwen", "niver", "noic", "ra", "rka",
                      "ryan", "ssa", "vyan"]
              }
              
print namegen(elf)
print namegen(halforc)
print namegen(dwarf)
print namegen(gnome)
print namegen(human_m2)
print namegen(human_m3)
print namegen(human_f2)
print namegen(human_f3)
print namegen(goblin)
print namegen(halfling_f)
print namegen(halfling_m)