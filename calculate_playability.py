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
    id_to_cards = []
    card_groups = {}
    id = 0
    with open(file) as f:
        for line in f:

            if line.strip(" \n") in ignored_names:
                continue
            if line.strip() == "\n":
                continue

            if reading_step == Color.SPELLS:
                line_list = line.split(" ", maxsplit=1)
                try:
                    amount = int(line_list[0])
                    card_name_and_group = line_list[1].split(";")
                except ValueError:
                    amount = 0
                    card_name_and_group = line.split(";")
                except IndexError as e:
                    print(f"Error while reading amount: {e}")
                    continue
                card_name = card_name_and_group[0]
                group_list = card_name_and_group[1:]
                id_to_cards.insert(id, card_name)
                assert id_to_cards[id] == card_name, f"Karte: {card_name} wurde nicht korrekt an ID: {id} eingefügt"
                id += 1
                for i in range(amount):
                    deck.append(card_name)
                for group in group_list:
                    card_groups.setdefault(group, []).append(card_name)
            elif reading_step == Color.PLAYABAL_HANDS:
                continue
            elif reading_step == Color.GAMBA_EFFECTS:
                break

def main():
    print("Hello World!")

if __name__ == "__main__":
    main()