from enum import Enum
import numpy as np
file = "Default_Deck.txt"

class Color(Enum):
    SPELLS = 1
    PLAYABAL_HANDS = 2
    GAMBA_EFFECTS = 3

def read_decklist(file):
    ignored_names = ["Monster", "Spell", "Trap"]
    reading_step = Color.SPELLS

    deck = []
    id_to_cards = {}
    card_groups = {}
    id = 0
    with open(file) as f:
        for line in f:

            if line.strip(" \n") in ignored_names:
                line_list = line.split(" ")
                try:
                    amount = int(line_list[0])
                    card_name_and_group = line_list[1]
                except ValueError:
                    amount = 0
                    card_name_and_group = line
                except IndexError as e:
                    print(f"Error while reading amount: {e}")
                    continue
                
            if reading_step == Color.SPELLS:
                continue
            elif reading_step == Color.PLAYABAL_HANDS:
                continue
            elif reading_step == Color.GAMBA_EFFECTS:
                break

def main():
    print("Hello World!")

if __name__ == "__main__":
    main()